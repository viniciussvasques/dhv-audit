from datetime import datetime, timedelta
import pytest
from src.domain.firm_efficiency import (
    InternalFirmEfficiencyEngine,
    AuditorTimesheet,
    SystemActivityLog
)

def test_timesheet_fidelity_crossover():
    engine = InternalFirmEfficiencyEngine()
    base_time = datetime(2026, 8, 17, 10, 0, 0)
    
    # Simulate timesheets: Auditor A declares 8 hours, Auditor B declares 4 hours
    timesheets = [
        AuditorTimesheet("t1", "auditor-A", 8.0, "project-X", "2026-08-17"),
        AuditorTimesheet("t2", "auditor-B", 4.0, "project-Y", "2026-08-17"),
    ]
    
    # Simulate passive logs
    # Auditor A has logs indicating high activity. Since each log session gives 10 minutes of active time,
    # let's write a loop to generate logs spaced by 10 minutes over a 6 hour window (36 logs total).
    logs_A = []
    for m in range(36): # 36 logs * 10 mins = 360 mins = 6 hours
        logs_A.append(SystemActivityLog(f"l-A-{m}", "auditor-A", "pdf_view", base_time + timedelta(minutes=m * 10)))
        
    # Auditor B has only 1 isolated log indicating only 10 minutes of active work
    logs_B = [
        SystemActivityLog("l-B-1", "auditor-B", "rag_query", base_time)
    ]
    
    all_logs = logs_A + logs_B
    fidelities = engine.audit_timesheet_fidelity(timesheets, all_logs)
    
    # Auditor A fidelity should be around 75% (6 hours active / 8 hours declared = 0.75)
    # Since each log is extended by 10 minutes, let's verify it gets correctly captured
    assert fidelities["auditor-A"] >= 0.70
    
    # Auditor B has low active hours (10 min active / 4 hours declared = 0.04)
    assert fidelities["auditor-B"] < 0.10

def test_firm_payroll_calculation():
    engine = InternalFirmEfficiencyEngine()
    
    # Auditor A drives R$ 200,000 in savings, has 90% timesheet fidelity, and only 5% rejection rate
    bonus_A = engine.calculate_firm_payroll(
        auditor_id="auditor-A",
        base_salary=6000.0,
        savings_driven=200000.0,
        fidelity_score=0.90,
        rejection_rate=0.05
    )
    
    # Auditor B drives R$ 200,000 in savings, but has 40% timesheet fidelity (fraudulent timesheet)
    bonus_B = engine.calculate_firm_payroll(
        auditor_id="auditor-B",
        base_salary=6000.0,
        savings_driven=200000.0,
        fidelity_score=0.40,
        rejection_rate=0.05
    )
    
    # Auditor A deserves a high bonus (~1.8k R$)
    assert bonus_A > 1500.00
    # Auditor B gets penalized to 0 b?nus for timesheet fidelity < 0.50
    assert bonus_B == 0.0
