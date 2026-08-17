from datetime import datetime, timedelta
import pytest
from src.domain.statistical_audit import (
    BrazilianProbabilisticAuditEngine,
    TransactionPayload,
    AnomalyReport
)

def test_benford_law_extraction():
    engine = BrazilianProbabilisticAuditEngine()
    # Test digits extraction
    assert engine._extract_first_digit(124.50) == 1
    assert engine._extract_first_digit(9.99) == 9
    assert engine._extract_first_digit(0.0045) == 4
    assert engine._extract_first_digit(-12.0) is None
    assert engine._extract_first_digit(0) is None

def test_benford_law_conformance():
    engine = BrazilianProbabilisticAuditEngine()
    
    # Generate numbers following Benford's Law distribution
    # P(d) = log10(1 + 1/d)
    import math
    benford_values = []
    # Let's mock a dataset of 1000 items following Benford distributions
    for d in range(1, 10):
        prob = math.log10(1.0 + 1.0 / d)
        count = int(1000 * prob)
        for _ in range(count):
            benford_values.append(float(f"{d}52.40"))
            
    p_value = engine.test_benford_law(benford_values)
    # Since they match Benford distribution perfectly, p_value should be relatively high (conforming, not suspicious)
    assert p_value > 0.05

def test_z_score_pricing():
    engine = BrazilianProbabilisticAuditEngine()
    
    values = [10.0, 10.5, 9.8, 10.2, 11.0, 10.1, 45.0] # 45.0 is a clear outlier
    z_score_normal = engine.calculate_z_score_price(10.0, values)
    z_score_outlier = engine.calculate_z_score_price(45.0, values)
    
    assert abs(z_score_normal) < 1.0
    assert z_score_outlier > 2.0 # Clearly high Z-Score

def test_poisson_frequency_anomaly():
    engine = BrazilianProbabilisticAuditEngine()
    
    # Average of 1.5 events per day
    hist_avg = 1.5
    
    # Normal day (2 events) should have a high p-value (not anomalous)
    p_normal = engine.calculate_poisson_anomaly(2, hist_avg)
    # Severe day (12 events) should have a very low p-value (highly anomalous)
    p_anomalous = engine.calculate_poisson_anomaly(12, hist_avg)
    
    assert p_normal > 0.05
    assert p_anomalous < 0.01

def test_evaluate_transaction_under_brazilian_legislation():
    engine = BrazilianProbabilisticAuditEngine()
    
    base_time = datetime(2026, 8, 17, 10, 0, 0)
    
    # Dataset simulation for employee overtimes (CLT Audit)
    transactions = []
    # Employee 1 behaves normally: registers 1 overtime log on average per week (over 20 weeks)
    for i in range(1, 21): # start at 1 to avoid overlapping base_time
        transactions.append(TransactionPayload(
            id=f"tx-norm-{i}",
            value=150.0,
            unit_price=50.0, # valor da hora extra
            category_key="HE_50_CLT",
            timestamp=base_time - timedelta(days=i * 7),
            entity_id="colab-normal"
        ))
        
    # Target transaction: Employee 1 suddenly has a cluster of 15 overtime logs on the SAME day (base_time)
    fraud_group = []
    for k in range(15):
        fraud_group.append(TransactionPayload(
            id=f"tx-fraud-clt-{k}",
            value=150.0,
            unit_price=50.0,
            category_key="HE_50_CLT",
            timestamp=base_time + timedelta(minutes=k * 10), # same day, different times
            entity_id="colab-normal"
        ))
    
    # Let's add target to complete list
    all_txs = transactions + fraud_group
    
    # We analyze the first transaction of the fraud group
    report = engine.evaluate_transaction(fraud_group[0], all_txs, "hr")
    
    assert report.risk_score > 0.50 # Anomaly should be captured
    assert "CLT" in report.legal_framing
    assert report.severity in ["high", "critical"]
    
    # Dataset simulation for overpriced purchases (Procurement/Fiscal Audit - NCM standard)
    fiscal_txs = []
    for i in range(50):
        fiscal_txs.append(TransactionPayload(
            id=f"tx-fisc-{i}",
            value=2000.0,
            unit_price=20.0, # pre?o unit?rio normal da caneta/papel (NCM 9608.10.00)
            category_key="NCM_9608.10.00",
            timestamp=base_time - timedelta(days=i),
            entity_id="vendor-abc"
        ))
        
    target_fiscal_fraud = TransactionPayload(
        id="tx-fraud-fisc",
        value=50000.0,
        unit_price=500.0, # Caneta superfaturada por R$ 500,00!
        category_key="NCM_9608.10.00",
        timestamp=base_time,
        entity_id="vendor-abc"
    )
    
    all_fiscal = fiscal_txs + [target_fiscal_fraud]
    
    report_fisc = engine.evaluate_transaction(target_fiscal_fraud, all_fiscal, "fiscal")
    
    assert report_fisc.risk_score > 0.50
    assert "ICMS" in report_fisc.legal_framing or "SPED" in report_fisc.legal_framing
    assert report_fisc.z_score_price > 3.0 # Price is an extreme outlier
