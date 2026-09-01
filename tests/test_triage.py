import pytest
import pandas as pd
from src.triage import AfyaTriageEngine

@pytest.fixture
def engine():
    return AfyaTriageEngine()

def test_normal_vitals_level_4(engine):
    """Normal vitals should yield Level 4 (Non-urgent) with no overrides."""
    df = pd.DataFrame([{
        'systolic_bp': 120,
        'heart_rate': 72,
        'respiratory_rate': 16,
        'oxygen_saturation': 98,
        'temperature': 36.6
    }])
    levels, overrides = engine.classify(df)
    assert levels[0] == 4
    assert overrides[0] == False

def test_hypoxia_safety_override(engine):
    """SpO2 < 88% MUST trigger Level 1 (Critical) safety override."""
    df = pd.DataFrame([{
        'systolic_bp': 118,
        'heart_rate': 70,
        'respiratory_rate': 14,
        'oxygen_saturation': 85,
        'temperature': 36.5
    }])
    levels, overrides = engine.classify(df)
    assert levels[0] == 1
    assert overrides[0] == True

def test_multi_vital_critical_score(engine):
    """Multiple elevated vitals achieving high risk score should map to Level 1 without override."""
    df = pd.DataFrame([{
        'systolic_bp': 170,
        'heart_rate': 130,
        'respiratory_rate': 30,
        'oxygen_saturation': 90,
        'temperature': 39.5
    }])
    levels, overrides = engine.classify(df)
    assert levels[0] == 1
    assert overrides[0] == False
