import os
import numpy as np
import pandas as pd

def generate_synthetic_patient_data(num_samples=1000, seed=42):
    np.random.seed(seed)
    
    age = np.random.randint(1, 85, size=num_samples)
    systolic_bp = np.random.normal(120, 20, num_samples).clip(70, 210)
    diastolic_bp = np.random.normal(80, 12, num_samples).clip(40, 130)
    heart_rate = np.random.normal(78, 18, num_samples).clip(40, 180)
    respiratory_rate = np.random.normal(18, 6, num_samples).clip(8, 45)
    oxygen_saturation = np.random.normal(96, 4, num_samples).clip(70, 100)
    temperature = np.random.normal(36.8, 0.9, num_samples).clip(34.0, 41.5)

    # Risk matrix calculation
    risk_score = (
        (systolic_bp > 160).astype(int) * 2 +
        (systolic_bp < 90).astype(int) * 3 +
        (heart_rate > 120).astype(int) * 2 +
        (respiratory_rate > 28).astype(int) * 3 +
        (oxygen_saturation < 92).astype(int) * 4 +
        (temperature > 39.0).astype(int) * 2
    )

    # Map to 4-tier Triage Levels (1: Critical, 2: Emergent, 3: Urgent, 4: Non-urgent)
    triage_level = np.where(risk_score >= 6, 1,
                   np.where(risk_score >= 4, 2,
                   np.where(risk_score >= 2, 3, 4)))

    # Hard Deterministic Override: Hypoxia forces Level 1 priority
    triage_level = np.where(oxygen_saturation < 88, 1, triage_level)

    df = pd.DataFrame({
        'age': age,
        'systolic_bp': np.round(systolic_bp, 1),
        'diastolic_bp': np.round(diastolic_bp, 1),
        'heart_rate': np.round(heart_rate, 1),
        'respiratory_rate': np.round(respiratory_rate, 1),
        'oxygen_saturation': np.round(oxygen_saturation, 1),
        'temperature': np.round(temperature, 1),
        'triage_level': triage_level
    })
    
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_synthetic_patient_data()
    output_path = "data/patient_triage_data.csv"
    df.to_csv(output_path, index=False)
    print(f"[Success] Generated {len(df)} clinical records at '{output_path}'")
