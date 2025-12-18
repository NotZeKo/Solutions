import matplotlib.pyplot as plt
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss, roc_auc_score, accuracy_score, classification_report
from sklearn.preprocessing import OrdinalEncoder
import lightgbm
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import StratifiedKFold

# Toggle flags
run_validation = False
run_submission = True

def load_data():
    print("Starting to load data...")
    df_train = pd.read_csv("train.csv")
    df_test = pd.read_csv("test.csv")
    Original = pd.read_csv("diabetes_dataset.csv")
    extras = ['glucose_fasting','glucose_postprandial','insulin_level','hba1c','diabetes_risk_score','diabetes_stage']
    Original = Original.drop(columns=extras)
    df_train = pd.concat([df_train.drop(columns=['id']), Original], ignore_index=True)
    return df_train, df_test

def check_missing_values(df):
    print("Starting to check missing values...")
    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]
    if not missing_values.empty:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=missing_values.index, y=missing_values.values, palette='viridis')
        plt.xticks(rotation=90)
        plt.xlabel('Features')
        plt.ylabel('Missing Values')
        plt.title('Missing Values per Feature')
        plt.tight_layout()
        plt.show()
    else:
        print("✅ No missing values found in the dataset.")

def extract_target(df_train):
    print("Starting to extract target...")
    y = df_train["diagnosed_diabetes"]
    return y

def engineer_features(df_train, df_test):
    print("Starting to engineer features...")
    df_train["physical_inactivity"] = 1.0 / (df_train["physical_activity_minutes_per_week"] + 0.0000001)
    df_test["physical_inactivity"] = 1.0 / (df_test["physical_activity_minutes_per_week"] + 0.0000001)
    # 1. Mean arterial pressure (strong diabetes predictor)
    df_train['mean_arterial_pressure'] = (df_train['systolic_bp'] + 2 * df_train['diastolic_bp']) / 3
    df_test['mean_arterial_pressure'] = (df_test['systolic_bp'] + 2 * df_test['diastolic_bp']) / 3
    # 2. Pulse pressure
    df_train['pulse_pressure'] = df_train['systolic_bp'] - df_train['diastolic_bp']
    df_test['pulse_pressure'] = df_test['systolic_bp'] - df_test['diastolic_bp']
    # 3. Total/HDL ratio (higher = worse)
    df_train['total_hdl_ratio'] = df_train['cholesterol_total'] / (df_train['hdl_cholesterol'] + 0.0001)
    df_test['total_hdl_ratio'] = df_test['cholesterol_total'] / (df_test['hdl_cholesterol'] + 0.0001)
    # 4. LDL/HDL ratio
    df_train['ldl_hdl_ratio'] = df_train['ldl_cholesterol'] / (df_train['hdl_cholesterol'] + 0.0001)
    df_test['ldl_hdl_ratio'] = df_test['ldl_cholesterol'] / (df_test['hdl_cholesterol'] + 0.0001)
    # 5. Triglyceride/HDL (insulin resistance marker)
    df_train['tg_hdl_ratio'] = df_train['triglycerides'] / (df_train['hdl_cholesterol'] + 0.0001)
    df_test['tg_hdl_ratio'] = df_test['triglycerides'] / (df_test['hdl_cholesterol'] + 0.0001)
    # 6. BMI categories (non-linear effect)
    df_train['bmi_high'] = (df_train['bmi'] > 30).astype(int)
    df_test['bmi_high'] = (df_test['bmi'] > 30).astype(int)
    # 7. Waist-to-hip extremes
    df_train['whr_high_risk'] = (df_train['waist_to_hip_ratio'] > 0.9).astype(int) # Women >0.85, Men >0.9
    df_test['whr_high_risk'] = (df_test['waist_to_hip_ratio'] > 0.9).astype(int)
    # 8. Sedentary lifestyle score
    df_train['sedentary_score'] = df_train['screen_time_hours_per_day'] * df_train['physical_inactivity']
    df_test['sedentary_score'] = df_test['screen_time_hours_per_day'] * df_test['physical_inactivity']
    # 9. Poor sleep + poor diet
    df_train['lifestyle_risk'] = ((df_train['sleep_hours_per_day'] < 6) | (df_train['diet_score'] < 5)).astype(int)
    df_test['lifestyle_risk'] = ((df_test['sleep_hours_per_day'] < 6) | (df_test['diet_score'] < 5)).astype(int)
    # 10. Cholesterol
    df_train['cholesterol_ratio'] = df_train['cholesterol_total'] / df_train['hdl_cholesterol']
    df_test['cholesterol_ratio'] = df_test['cholesterol_total'] / df_test['hdl_cholesterol']
    df_train['triglyceride_hdl_ratio'] = df_train['triglycerides'] / df_train['hdl_cholesterol']
    df_test['triglyceride_hdl_ratio'] = df_test['triglycerides'] / df_test['hdl_cholesterol']
    # 11. activity
    # Physical activity category (meets WHO guideline)
    df_train['physical_activity_150_plus'] = (
            df_train['physical_activity_minutes_per_week'] >= 150
    ).astype(int)
    df_test['physical_activity_150_plus'] = (
            df_test['physical_activity_minutes_per_week'] >= 150
    ).astype(int)
    # Triglyceride-based metabolic risk (ordinal)
    df_train['high_triglyceride_diabetes_risk'] = (
            df_train['triglycerides'] >= 150
    ).astype(int)
    df_test['high_triglyceride_diabetes_risk'] = (
            df_test['triglycerides'] >= 150
    ).astype(int)
    # coffee
    df_train['log_triglycerides'] = np.log1p(df_train['triglycerides'])
    df_test['log_triglycerides'] = np.log1p(df_test['triglycerides'])
    df_train['aip_index'] = np.log1p(df_train['triglycerides'] / (df_train['hdl_cholesterol'] + 0.0001))
    df_test['aip_index'] = np.log1p(df_test['triglycerides'] / (df_test['hdl_cholesterol'] + 0.0001))
    def categorize_bp(row):
        if row['systolic_bp'] < 120 and row['diastolic_bp'] < 80:
            return 0
        elif 120 <= row['systolic_bp'] < 130 and row['diastolic_bp'] < 80:
            return 1
        elif 130 <= row['systolic_bp'] < 140 or 80 <= row['diastolic_bp'] < 90:
            return 2
        else:
            return 3
    df_train['bp_category'] = df_train.apply(categorize_bp, axis=1)
    df_test['bp_category'] = df_test.apply(categorize_bp, axis=1)
    df_train['bmi_age_interaction'] = df_train['bmi'] * df_train['age']
    df_test['bmi_age_interaction'] = df_test['bmi'] * df_test['age']
    df_train['visceral_fat_proxy'] = df_train['bmi'] * df_train['waist_to_hip_ratio']
    df_test['visceral_fat_proxy'] = df_test['bmi'] * df_test['waist_to_hip_ratio']
    df_train['family_bmi_interaction'] = df_train['family_history_diabetes'] * df_train['bmi']
    df_test['family_bmi_interaction'] = df_test['family_history_diabetes'] * df_test['bmi']
    df_train['family_age_interaction'] = df_train['family_history_diabetes'] * df_train['age']
    df_test['family_age_interaction'] = df_test['family_history_diabetes'] * df_test['age']
    df_train['age_systolic_interaction'] = df_train['age'] * df_train['systolic_bp']
    df_test['age_systolic_interaction'] = df_test['age'] * df_test['systolic_bp']
    df_train['non_hdl_cholesterol'] = df_train['cholesterol_total'] - df_train['hdl_cholesterol']
    df_test['non_hdl_cholesterol'] = df_test['cholesterol_total'] - df_test['hdl_cholesterol']
    df_train['map'] = df_train['diastolic_bp'] + (df_train['pulse_pressure'] / 3)
    df_test['map'] = df_test['diastolic_bp'] + (df_test['pulse_pressure'] / 3)
    df_train["diet_level"] = df_train["diet_score"].round().clip(1, 10).astype(int)
    df_test["diet_level"] = df_test["diet_score"].round().clip(1, 10).astype(int)

def define_features():
    print("Starting to define features...")
    features = [
        "age", "alcohol_consumption_per_week",
        "diet_score", "sleep_hours_per_day", "screen_time_hours_per_day",
        "waist_to_hip_ratio", "systolic_bp", "diastolic_bp",
        "hdl_cholesterol", "triglycerides", "bmi"
        , "gender", "employment_status", "income_level",
        "heart_rate", "cholesterol_total", "ldl_cholesterol", "smoking_status",
        "family_history_diabetes", "hypertension_history", "cardiovascular_history",
        "physical_activity_minutes_per_week","physical_inactivity",
    ]
    # New features
    bad_features = ["ethnicity", "education_level", "physical_activity_150_plus", "diet_score", ]
    New = [ # NEW engineered features
        "mean_arterial_pressure", "pulse_pressure",
        "total_hdl_ratio", "ldl_hdl_ratio", "tg_hdl_ratio",
        "bmi_high", "whr_high_risk",
        "sedentary_score", "lifestyle_risk", "physical_inactivity",
        "cholesterol_ratio", "triglyceride_hdl_ratio", "physical_activity_150_plus"]
    return features

def prepare_datasets(df_train, df_test, features):
    print("Starting to prepare datasets...")
    X = pd.get_dummies(df_train[features], drop_first=True)
    test = pd.get_dummies(df_test[features], drop_first=True)
    X, test = X.align(test, join='inner', axis=1)
    return X, test

def model_for_submission_lgbm(X_training, y, seeds):
    print("Starting to train LGBM models for submission...")
    # train models and keep them in a list
    models = []
    kwargs = {
        # "objective": "binary",
        # "metric": "binary_logloss",
        # "boosting_type": "gbdt",
        "n_estimators": 2000,
        "learning_rate": 0.07,
        "num_leaves": 50,
        "max_depth": 4,
        "min_child_samples": 57,
        "subsample": 0.8,
        "colsample_bytree": 0.2,
        "reg_alpha": 9.5,
        "reg_lambda": 1.0e-08,
        "random_state": 44,
        "n_jobs": -1,
        "verbosity": -1,
    }
    for s in seeds:
        X_train, _, y_train, _ = train_test_split(X_training, y, test_size=0.2, random_state=s, stratify=y)
        X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=s, stratify=y_train)
        model = lightgbm.LGBMClassifier(**kwargs)
        model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)])
        models.append(model)
    return models

def model_for_submission_xgb(X_training, y, seeds):
    print("Starting to train XGBoost models for submission...")
    models = []
    kwargs = {
        "n_estimators": 2000,
        "learning_rate": 0.07,
        "max_depth": 4,
        "min_child_weight": 57,
        "subsample": 0.8,
        "colsample_bytree": 0.2,
        "reg_alpha": 9.5,
        "reg_lambda": 1.0e-08,
        "random_state": 44,
        "n_jobs": -1,
        "verbosity": 0,
    }
    for s in seeds:
        X_train, _, y_train, _ = train_test_split(X_training, y, test_size=0.2, random_state=s, stratify=y)
        X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=s, stratify=y_train)
        model = XGBClassifier(**kwargs)
        model.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
        models.append(model)
    return models

def train_lgbm_models(X, y, seeds):
    print("Starting training LGBM models...")
    return model_for_submission_lgbm(X_training=X, y=y, seeds=seeds)

def train_xgb_models(X, y, seeds):
    print("Starting training XGBoost models...")
    return model_for_submission_xgb(X_training=X, y=y, seeds=seeds)

def validate_lgbm(X_training, y, n_estimators=None, learning_rate=None, num_leaves=None, max_depth=None, min_child_samples=None, subsample=None, colsample_bytree=None, reg_alpha=None, reg_lambda=None):
    print("Starting LGBM validation...")
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    oof_preds = np.zeros(len(y), dtype=float)
    for fold, (tr_idx, val_idx) in enumerate(skf.split(X_training, y), start=1):
        X_tr, X_val = X_training.iloc[tr_idx], X_training.iloc[val_idx]
        y_tr, y_val = y[tr_idx], y[val_idx]
        kwargs = {
            "n_estimators": n_estimators,
            "learning_rate": learning_rate,
            "num_leaves": num_leaves,
            "max_depth": max_depth,
            "min_child_samples": min_child_samples,
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
            "reg_alpha": reg_alpha,
            "reg_lambda": reg_lambda,
            "random_state": 42 + fold,
            "n_jobs": -1,
            "verbosity": -1,
        }
        m = lightgbm.LGBMClassifier(**kwargs)
        m.fit(X_tr, y_tr, eval_set=[(X_val, y_val)])
        oof_preds[val_idx] = m.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y, oof_preds)
    logloss = log_loss(y, oof_preds)
    brier = brier_score_loss(y, oof_preds)
    return auc, logloss, brier, oof_preds

def validate_xgb(X_training, y, n_estimators=None, learning_rate=None, max_depth=None, min_child_weight=None, subsample=None, colsample_bytree=None, reg_alpha=None, reg_lambda=None):
    print("Starting XGBoost validation...")
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    oof_preds = np.zeros(len(y), dtype=float)
    for fold, (tr_idx, val_idx) in enumerate(skf.split(X_training, y), start=1):
        X_tr, X_val = X_training.iloc[tr_idx], X_training.iloc[val_idx]
        y_tr, y_val = y[tr_idx], y[val_idx]
        kwargs = {
            "n_estimators": n_estimators,
            "learning_rate": learning_rate,
            "max_depth": max_depth,
            "min_child_weight": min_child_weight,
            "subsample": subsample,
            "colsample_bytree": colsample_bytree,
            "reg_alpha": reg_alpha,
            "reg_lambda": reg_lambda,
            "random_state": 42 + fold,
            "n_jobs": -1,
            "verbosity": 0,
        }
        m = XGBClassifier(**kwargs)
        m.fit(X_tr, y_tr, eval_set=[(X_val, y_val)], verbose=False)
        oof_preds[val_idx] = m.predict_proba(X_val)[:, 1]
    auc = roc_auc_score(y, oof_preds)
    logloss = log_loss(y, oof_preds)
    brier = brier_score_loss(y, oof_preds)
    return auc, logloss, brier, oof_preds

def perform_validation(X, y):
    print("Starting validation process...")
    # LGBM validation
    auc_l, logloss_l, brier_l, oof_l = validate_lgbm(
        X_training=X,
        y=y,
        n_estimators=500,
        learning_rate=0.05,
        max_depth=-1,
        num_leaves=31,
        subsample=0.8,
        colsample_bytree=0.8
    )
    print("LGBM AUC:", auc_l)
    print("LGBM LogLoss:", logloss_l)
    print("LGBM Brier Score:", brier_l)

    # XGBoost validation
    auc_x, logloss_x, brier_x, oof_x = validate_xgb(
        X_training=X,
        y=y,
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        min_child_weight=1,
        subsample=0.8,
        colsample_bytree=0.8
    )
    print("XGBoost AUC:", auc_x)
    print("XGBoost LogLoss:", logloss_x)
    print("XGBoost Brier Score:", brier_x)

    # Ensemble
    oof_ens = (oof_l + oof_x) / 2
    auc_ens = roc_auc_score(y, oof_ens)
    logloss_ens = log_loss(y, oof_ens)
    brier_ens = brier_score_loss(y, oof_ens)
    print("Ensemble AUC:", auc_ens)
    print("Ensemble LogLoss:", logloss_ens)
    print("Ensemble Brier Score:", brier_ens)

def generate_submission(models, test, df_test):
    print("Starting to generate submission...")
    X_test_final = test
    probs_list = []
    for model in models:
        p = model.predict_proba(X_test_final)[:, 1] # probability of positive class
        probs_list.append(p)
    # Average predictions across models
    probs_mean = np.mean(probs_list, axis=0)
    df_test["diagnosed_diabetes"] = probs_mean
    submission = df_test[["id", "diagnosed_diabetes"]]
    submission.to_csv("submission.csv", index=False)
    print("Saved submission.csv with shape:", submission.shape)
    print(submission.head())

def main():
    print("Starting main execution...")
    df_train, df_test = load_data()
    check_missing_values(df_train)
    y = extract_target(df_train)
    engineer_features(df_train, df_test)
    features = define_features()
    X, test = prepare_datasets(df_train, df_test, features)
    print(f"Train shape: {X.shape}, Test shape: {test.shape}")
    seeds = [i for i in range(14)]
    models_lgb = train_lgbm_models(X, y, seeds)
    models_xgb = train_xgb_models(X, y, seeds)
    all_models = models_lgb + models_xgb
    if run_validation:
        perform_validation(X, y)
    if run_submission:
        generate_submission(all_models, test, df_test)

if __name__ == "__main__":
    main()