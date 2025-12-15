import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import lightgbm as lgb
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import log_loss, roc_auc_score, brier_score_loss

# 1. CARICAMENTO DATI
df_train = pd.read_csv("train.csv")
df_test = pd.read_csv("test.csv")

# 2. FEATURE ENGINEERING (PARTE 1: Feature Base e Intermedie)
# È fondamentale eseguire prima queste, altrimenti ottieni KeyError

# Physical Inactivity
df_train["physical_inactivity"] = 1.0 / (df_train["physical_activity_minutes_per_week"] + 0.0000001)
df_test["physical_inactivity"] = 1.0 / (df_test["physical_activity_minutes_per_week"] + 0.0000001)

# Pressione Sanguigna Base
df_train['pulse_pressure'] = df_train['systolic_bp'] - df_train['diastolic_bp']
df_test['pulse_pressure'] = df_test['systolic_bp'] - df_test['diastolic_bp']

df_train['mean_arterial_pressure'] = (df_train['systolic_bp'] + 2*df_train['diastolic_bp']) / 3
df_test['mean_arterial_pressure'] = (df_test['systolic_bp'] + 2*df_test['diastolic_bp']) / 3

df_train['map'] = df_train['diastolic_bp'] + (df_train['pulse_pressure'] / 3)
df_test['map'] = df_test['diastolic_bp'] + (df_test['pulse_pressure'] / 3)

# Rapporti Colesterolo
df_train['total_hdl_ratio'] = df_train['cholesterol_total'] / (df_train['hdl_cholesterol'] + 0.0001)
df_test['total_hdl_ratio'] = df_test['cholesterol_total'] / (df_test['hdl_cholesterol'] + 0.0001)

df_train['ldl_hdl_ratio'] = df_train['ldl_cholesterol'] / (df_train['hdl_cholesterol'] + 0.0001)
df_test['ldl_hdl_ratio'] = df_test['ldl_cholesterol'] / (df_test['hdl_cholesterol'] + 0.0001)

df_train['tg_hdl_ratio'] = df_train['triglycerides'] / (df_train['hdl_cholesterol'] + 0.0001)
df_test['tg_hdl_ratio'] = df_test['triglycerides'] / (df_test['hdl_cholesterol'] + 0.0001)

df_train['cholesterol_ratio'] = df_train['cholesterol_total'] / df_train['hdl_cholesterol']
df_test['cholesterol_ratio'] = df_test['cholesterol_total'] / df_test['hdl_cholesterol']

df_train['triglyceride_hdl_ratio'] = df_train['triglycerides'] / df_train['hdl_cholesterol']
df_test['triglyceride_hdl_ratio'] = df_test['triglycerides'] / df_test['hdl_cholesterol']

df_train['non_hdl_cholesterol'] = df_train['cholesterol_total'] - df_train['hdl_cholesterol']
df_test['non_hdl_cholesterol'] = df_test['cholesterol_total'] - df_test['hdl_cholesterol']

# Rischi Metabolici e Stile di Vita
df_train['bmi_high'] = (df_train['bmi'] > 30).astype(int)
df_test['bmi_high'] = (df_test['bmi'] > 30).astype(int)

df_train['whr_high_risk'] = (df_train['waist_to_hip_ratio'] > 0.9).astype(int)
df_test['whr_high_risk'] = (df_test['waist_to_hip_ratio'] > 0.9).astype(int)

df_train['sedentary_score'] = df_train['screen_time_hours_per_day'] * df_train['physical_inactivity']
df_test['sedentary_score'] = df_test['screen_time_hours_per_day'] * df_test['physical_inactivity']

df_train['lifestyle_risk'] = ((df_train['sleep_hours_per_day'] < 6) | (df_train['diet_score'] < 5)).astype(int)
df_test['lifestyle_risk'] = ((df_test['sleep_hours_per_day'] < 6) | (df_test['diet_score'] < 5)).astype(int)

df_train['physical_activity_150_plus'] = (df_train['physical_activity_minutes_per_week'] >= 150).astype(int)
df_test['physical_activity_150_plus'] = (df_test['physical_activity_minutes_per_week'] >= 150).astype(int)

df_train['high_triglyceride_diabetes_risk'] = (df_train['triglycerides'] >= 150).astype(int)
df_test['high_triglyceride_diabetes_risk'] = (df_test['triglycerides'] >= 150).astype(int)

# Interazioni Base
df_train['bmi_age_interaction'] = df_train['bmi'] * df_train['age']
df_test['bmi_age_interaction'] = df_test['bmi'] * df_test['age']

df_train['visceral_fat_proxy'] = df_train['bmi'] * df_train['waist_to_hip_ratio']
df_test['visceral_fat_proxy'] = df_test['bmi'] * df_test['waist_to_hip_ratio']


# 3. FEATURE ENGINEERING (PARTE 2: Log Transforms e Avanzate - dal tuo codice)

# Log Transforms & AIP Index
df_train['log_triglycerides'] = np.log1p(df_train['triglycerides'])
df_test['log_triglycerides'] = np.log1p(df_test['triglycerides'])

df_train['aip_index'] = np.log1p(df_train['triglycerides'] / (df_train['hdl_cholesterol'] + 0.0001))
df_test['aip_index'] = np.log1p(df_test['triglycerides'] / (df_test['hdl_cholesterol'] + 0.0001))

# Blood Pressure Categories
def categorize_bp(row):
    if row['systolic_bp'] < 120 and row['diastolic_bp'] < 80:
        return 0 # Normal
    elif 120 <= row['systolic_bp'] < 130 and row['diastolic_bp'] < 80:
        return 1 # Elevated
    elif 130 <= row['systolic_bp'] < 140 or 80 <= row['diastolic_bp'] < 90:
        return 2 # Hypertension Stage 1
    else:
        return 3 # Hypertension Stage 2

df_train['bp_category'] = df_train.apply(categorize_bp, axis=1)
df_test['bp_category'] = df_test.apply(categorize_bp, axis=1)

# Interactions (Family History)
df_train['family_bmi_interaction'] = df_train['family_history_diabetes'] * df_train['bmi']
df_test['family_bmi_interaction'] = df_test['family_history_diabetes'] * df_test['bmi']

df_train['family_age_interaction'] = df_train['family_history_diabetes'] * df_train['age']
df_test['family_age_interaction'] = df_test['family_history_diabetes'] * df_test['age']

df_train['age_systolic_interaction'] = df_train['age'] * df_train['systolic_bp']
df_test['age_systolic_interaction'] = df_test['age'] * df_test['systolic_bp']


# 4. DEFINIZIONE LISTA FEATURES COMPLETA
features = [
    # Originali numeriche
    "age", "alcohol_consumption_per_week", "diet_score", "sleep_hours_per_day", 
    "screen_time_hours_per_day", "waist_to_hip_ratio", "systolic_bp", "diastolic_bp",
    "hdl_cholesterol", "triglycerides", "bmi", "heart_rate", "cholesterol_total",
    "ldl_cholesterol", "physical_activity_minutes_per_week",
    # Originali categoriche
    "gender", "employment_status", "income_level", "smoking_status",
    "family_history_diabetes", "hypertension_history", "cardiovascular_history",
    # Generate Parte 1
    "physical_inactivity", "pulse_pressure", "mean_arterial_pressure", "map",
    "total_hdl_ratio", "ldl_hdl_ratio", "tg_hdl_ratio", "cholesterol_ratio",
    "triglyceride_hdl_ratio", "non_hdl_cholesterol",
    "bmi_high", "whr_high_risk", "sedentary_score", "lifestyle_risk",
    "physical_activity_150_plus", "high_triglyceride_diabetes_risk",
    "bmi_age_interaction", "visceral_fat_proxy",
    # Generate Parte 2 (Nuove)
    "log_triglycerides", "aip_index", "bp_category",
    "family_bmi_interaction", "family_age_interaction", "age_systolic_interaction"
]

print(f"Totale features utilizzate: {len(features)}")


# 5. ONE HOT ENCODING & ALLINEAMENTO
print("Esecuzione One-Hot Encoding...")
X = pd.get_dummies(df_train[features], drop_first=True)
test = pd.get_dummies(df_test[features], drop_first=True)

# Align columns (Fondamentale)
X, test = X.align(test, join='inner', axis=1)
print(f"Shape finale -> Train: {X.shape}, Test: {test.shape}")


# 6. VALIDAZIONE MODELLO (Il tuo codice)
def validate_model(X_training, y, **kwargs):
    n_splits = 5
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    oof_preds = np.zeros(len(y), dtype=float)

    for fold, (tr_idx, val_idx) in enumerate(skf.split(X_training, y), start=1):
        X_tr, X_val = X_training.iloc[tr_idx], X_training.iloc[val_idx]
        y_tr, y_val = y[tr_idx], y[val_idx]
        
        # Aggiorna random_state per fold
        fold_kwargs = kwargs.copy()
        fold_kwargs['random_state'] = 42 + fold
        
        m = lgb.LGBMClassifier(**fold_kwargs)
        m.fit(X_tr, y_tr, eval_set=[(X_val, y_val)])
        oof_preds[val_idx] = m.predict_proba(X_val)[:, 1]
        
    auc = roc_auc_score(y, oof_preds)
    logloss = log_loss(y, oof_preds)
    brier = brier_score_loss(y, oof_preds)
    return auc, logloss, brier

print("\n--- Inizio Validazione ---")
# Parametri del modello
params = {
    "n_estimators": 2000, "learning_rate": 0.04, "num_leaves": 50,
    "max_depth": 6, "min_child_samples": 57, "subsample": 0.8,
    "colsample_bytree": 0.2, "reg_alpha": 9.5, "reg_lambda": 1e-08,
    "n_jobs": -1, "verbosity": -1
}

auc, logloss, brier = validate_model(X, df_train["diagnosed_diabetes"], **params)
print(f"AUC: {auc:.5f}")
print(f"LogLoss: {logloss:.5f}")
print(f"Brier Score: {brier:.5f}")


print("\n--- Addestramento Finale e Generazione Submission ---")
final_model = lgb.LGBMClassifier(**params, random_state=42)
final_model.fit(X, df_train["diagnosed_diabetes"])

predictions = final_model.predict_proba(test)[:, 1]
df_test["diagnosed_diabetes"] = predictions

submission = df_test[["id", "diagnosed_diabetes"]]
submission.to_csv("submission_final.csv", index=False)
print("✅ File 'submission_final.csv' salvato con successo!")

