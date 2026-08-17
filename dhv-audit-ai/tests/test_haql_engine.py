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
