from datetime import datetime, timedelta
import pytest
from src.domain.statistical_audit import TransactionPayload
from src.domain.resource_efficiency import ActivityRecord
from src.domain.haql_engine import HAQLUnifiedEngine, HAQLAnalysisResult

def test_haql_unified_calculation_hr():
    engine = HAQLUnifiedEngine()
    base_time = datetime(2026, 8, 17, 10, 0, 0)

    # 1. Simulate Overtime Records (CLT/HR Domain)
    transactions = []
    activities = []
    
    # Colleague A is efficient and behaves normally
    for i in range(1, 21):
        transactions.append(TransactionPayload(
            id=f"clt-tx-{i}",
            value=150.0,
            unit_price=50.0,
            category_key="HE_50_CLT",
            timestamp=base_time - timedelta(days=i),
            entity_id="clerk-A"
        ))
        activities.append(ActivityRecord(
            id=f"act-A-{i}",
            resource_id="clerk-A",
            activity_type="invoice_entry",
            context_key="NFSe_manual",
            cost_incurred=300.0,
            units_produced=150.0, # Yield: 15 units/hour
            duration_hours=10.0,
            timestamp=base_time - timedelta(days=i)
        ))

    # Colleague B is highly inefficient (renders much lower yield and high costs/hours)
    for i in range(1, 21):
        activities.append(ActivityRecord(
            id=f"act-B-{i}",
            resource_id="clerk-B",
            activity_type="invoice_entry",
            context_key="NFSe_manual",
            cost_incurred=300.0,
            units_produced=50.0, # Yield: 5 units/hour (Very low!)
            duration_hours=10.0,
            timestamp=base_time - timedelta(days=i)
        ))

    # Target an anomalous transaction for Colleague B where Poisson cluster or Z-Score represents leakage
    target_tx = TransactionPayload(
        id="target-leak-tx",
        value=300.0,
        unit_price=50.0,
        category_key="HE_50_CLT",
        timestamp=base_time,
        entity_id="clerk-B"
    )
    
    target_act = ActivityRecord(
        id="target-leak-act",
        resource_id="clerk-B",
        activity_type="invoice_entry",
        context_key="NFSe_manual",
        cost_incurred=300.0,
        units_produced=50.0,
        duration_hours=10.0,
        timestamp=base_time
    )

    all_txs = transactions + [target_tx]
    all_acts = activities + [target_act]

    # Calculate HAQL
    result = engine.calculate_quantum_leakage(
        target_tx=target_tx,
        all_txs=all_txs,
        associated_activity=target_act,
        all_activities=all_acts,
        domain="hr"
    )

    # The EQI should reflect high risk because of Clerk B's extreme inefficiency in the cohort (MPE-IR)
    assert result.eqi_score >= 0.20 # Captured some leakage
    assert result.breakdown["efficiency_vector"] > 0.50 # High efficiency deficit captured
    assert result.annual_waste_estimate > 1000.00
    assert "HAQL" in result.explanation

def test_haql_unified_domains_and_severities():
    engine = HAQLUnifiedEngine()
    base_time = datetime(2026, 8, 17, 10, 0, 0)
    
    # Simple tx dataset
    txs = [
        TransactionPayload("t-1", 100.0, 10.0, "ITEM-1", base_time, "ent-1"),
        TransactionPayload("t-2", 100.0, 10.0, "ITEM-1", base_time, "ent-1"),
        TransactionPayload("t-3", 1000.0, 100.0, "ITEM-1", base_time, "ent-1") # outlier
    ]
    
    # 1. Test Fiscal Domain
    res_fiscal = engine.calculate_quantum_leakage(
        target_tx=txs[2],
        all_txs=txs,
        associated_activity=None,
        all_activities=[],
        domain="fiscal"
    )
    assert res_fiscal.eqi_score > 0.0
    
    # 2. Test Fleet Domain
    res_fleet = engine.calculate_quantum_leakage(
        target_tx=txs[0],
        all_txs=txs,
        associated_activity=None,
        all_activities=[],
        domain="fleet"
    )
    assert res_fleet.eqi_score >= 0.0
    
    # 3. Test Default Domain (Other)
    res_other = engine.calculate_quantum_leakage(
        target_tx=txs[0],
        all_txs=txs,
        associated_activity=None,
        all_activities=[],
        domain="other_unspecified"
    )
    assert res_other.eqi_score >= 0.0
    
    # 4. Validate severities mapping via monkeypatching
    from src.domain.statistical_audit import AnomalyReport
    
    # Let's mock a very high risk report to trigger critical (eqi >= 0.85)
    def mock_evaluate_critical(*args, **kwargs):
        return AnomalyReport(
            id="mock-id",
            risk_score=0.95,
            benford_p_value=0.001, # v_b = 0.999
            z_score_price=10.0,    # v_z = 1.0
            poisson_p_value=0.001, # v_p = 0.999
            severity="critical",
            legal_framing="Test",
            justification="Test"
        )
        
    engine.stats_engine.evaluate_transaction = mock_evaluate_critical
    res_crit = engine.calculate_quantum_leakage(
        target_tx=txs[0],
        all_txs=txs,
        associated_activity=None,
        all_activities=[],
        domain="fiscal"
    )
    assert res_crit.risk_level == "critical"

    # Let's mock high risk report (eqi >= 0.60)
    def mock_evaluate_high(*args, **kwargs):
        return AnomalyReport(
            id="mock-id",
            risk_score=0.70,
            benford_p_value=0.001, # v_b = 0.999
            z_score_price=4.5,     # v_z = 1.0 (since 4.5 / 3.0 > 1.0)
            poisson_p_value=0.5,   # v_p = 0.0
            severity="high",
            legal_framing="Test",
            justification="Test"
        )
    engine.stats_engine.evaluate_transaction = mock_evaluate_high
    res_high = engine.calculate_quantum_leakage(
        target_tx=txs[0],
        all_txs=txs,
        associated_activity=None,
        all_activities=[],
        domain="fiscal"
    )
    # w1=0.35, w2=0.45, w3=0.10, w4=0.10
    # eqi = (0.35 * 0.999) + (0.45 * 1.0) + (0.10 * 0.0) + (0.10 * 0.0) = 0.34965 + 0.45 = 0.79965 (high)
    assert res_high.risk_level == "high"

    # Let's mock medium risk report (eqi >= 0.35)
    def mock_evaluate_medium(*args, **kwargs):
        return AnomalyReport(
            id="mock-id",
            risk_score=0.45,
            benford_p_value=0.5,  # v_b = 0.0
            z_score_price=3.0,    # v_z = 1.0
            poisson_p_value=0.5,  # v_p = 0.0
            severity="medium",
            legal_framing="Test",
            justification="Test"
        )
    engine.stats_engine.evaluate_transaction = mock_evaluate_medium
    res_med = engine.calculate_quantum_leakage(
        target_tx=txs[0],
        all_txs=txs,
        associated_activity=None,
        all_activities=[],
        domain="fiscal"
    )
    # eqi = (0.35 * 0) + (0.45 * 1.0) + 0 + 0 = 0.45 (medium)
    assert res_med.risk_level == "medium"


