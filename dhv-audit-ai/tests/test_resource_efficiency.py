from datetime import datetime, timedelta
import pytest
from src.domain.resource_efficiency import (
    ResourceEfficiencyProfiler,
    ActivityRecord,
    ResourceProfile,
    CohortBenchmark
)

def test_calculate_benchmarks():
    profiler = ResourceEfficiencyProfiler()
    
    # Mock data comparing drivers on the same route "SP-RJ" using diesel (cost in R$, output in Km)
    # Driver A: 400Km, cost R$ 800 (R$ 2.00 / Km)
    # Driver B: 400Km, cost R$ 600 (R$ 1.50 / Km) -- More efficient
    # Driver C: 400Km, cost R$ 1000 (R$ 2.50 / Km)
    records = [
        ActivityRecord("r1", "driver-A", "delivery_route", "SP-RJ", 800.0, 400.0, 8.0),
        ActivityRecord("r2", "driver-B", "delivery_route", "SP-RJ", 600.0, 400.0, 8.0),
        ActivityRecord("r3", "driver-C", "delivery_route", "SP-RJ", 1000.0, 400.0, 8.0),
    ]
    
    benchmarks = profiler.calculate_benchmarks(records)
    cohort_key = "delivery_route||SP-RJ"
    
    assert cohort_key in benchmarks
    bench = benchmarks[cohort_key]
    
    assert bench.best_unit_cost == 1.50   # Driver B is the best
    assert bench.median_unit_cost == 2.00 # Driver A is the median (1.50, 2.00, 2.50)
    assert bench.mean_unit_cost == 2.00   # (1.50 + 2.0 + 2.5) / 3 = 2.0

def test_resource_profiling_and_waste_projection():
    profiler = ResourceEfficiencyProfiler()
    
    # 3 clerks processing "NFS-e" manuals (cost in R$ - hours paid, units in processed invoices)
    # Clerk-A: 10 hours, cost R$ 300, processed 100 invoices (Cost per invoice: R$ 3.00, Yield: 10 inv/h)
    # Clerk-B: 10 hours, cost R$ 300, processed 150 invoices (Cost per invoice: R$ 2.00, Yield: 15 inv/h) -- Median & Best
    # Clerk-C: 10 hours, cost R$ 300, processed 50 invoices  (Cost per invoice: R$ 6.00, Yield: 5 inv/h) -- Wasteful
    records = [
        ActivityRecord("1", "clerk-A", "invoice_entry", "NFSe_manual", 300.0, 100.0, 10.0),
        ActivityRecord("2", "clerk-B", "invoice_entry", "NFSe_manual", 300.0, 150.0, 10.0),
        ActivityRecord("3", "clerk-C", "invoice_entry", "NFSe_manual", 300.0, 50.0, 10.0),
    ]
    
    profiles = profiler.profile_resources(records)
    
    # Index profiles by resource id
    profile_dict = {p.resource_id: p for p in profiles}
    
    assert "clerk-A" in profile_dict
    assert "clerk-B" in profile_dict
    assert "clerk-C" in profile_dict
    
    p_a = profile_dict["clerk-A"]
    p_b = profile_dict["clerk-B"]
    p_c = profile_dict["clerk-C"]
    
    # Clerk B is the best (relative efficiency 1.0)
    assert p_b.relative_efficiency == 1.0
    assert p_b.annual_waste_estimate == 0.0
    
    # Clerk A unit cost (R$ 3.0) is higher than the median of the cohort (which is R$ 3.0? No, let's look at sorted list: 2.0, 3.0, 6.0. Median is 3.0)
    # So Clerk A is exactly on the median, hence no waste estimate
    assert p_a.unit_cost == 3.0
    assert p_a.annual_waste_estimate == 0.0
    
    # Clerk C unit cost (R$ 6.0) is higher than the median (R$ 3.0)
    assert p_c.unit_cost == 6.0
    # Annual waste projection for Clerk C (processes 5 units/hour * 1800h = 9000 units/year. Delta cost is 6.0 - 3.0 = 3.0. Annual waste: 3 * 9000 = 27000.00 R$)
    assert p_c.annual_waste_estimate == 27000.00
    assert p_c.relative_efficiency < 0.50 # Less than 50% efficiency compared to the best
