import pytest
from datetime import datetime
from src.domain.rules_pipeline import (
    QuantumRulesPipeline,
    TaskRequest,
    TaskType,
    TaskStatus,
    PipelineContext,
    SubTask,
    HumanEscalationNeeded
)

# Mock generators and runners for testing

def mock_code_generator_success(filepath: str, attempt: int) -> str:
    return "Valid clean code patch."

def mock_code_generator_retry(filepath: str, attempt: int) -> str:
    if attempt < 2:
        return "buggy code"
    return "valid clean code patch."

def mock_qa_runner_high(ctx: PipelineContext) -> float:
    return 0.95

def mock_qa_runner_low(ctx: PipelineContext) -> float:
    return 0.40

def mock_sec_runner_high(ctx: PipelineContext) -> float:
    return 0.98

def mock_sec_runner_low(ctx: PipelineContext) -> float:
    return 0.50

def mock_integration_test_passed(ctx: PipelineContext) -> bool:
    return True

def mock_integration_test_failed(ctx: PipelineContext) -> bool:
    return False

def mock_reviewer_approved(ctx: PipelineContext) -> bool:
    return True

def test_pipeline_intake_triage_routing():
    pipeline = QuantumRulesPipeline()
    
    # 1. Test Large Feature routing
    req_large = TaskRequest("t-1", "Implement huge modules", ["file.py"], 0.95)
    ctx_large = pipeline.intake_and_triage(req_large)
    assert ctx_large.task_type == TaskType.LARGE_FEATURE
    assert ctx_large.autonomy_level == 0.90
    
    # 2. Test Small Feature routing
    req_small = TaskRequest("t-2", "Add simple button", ["file.py"], 0.50)
    ctx_small = pipeline.intake_and_triage(req_small)
    assert ctx_small.task_type == TaskType.SMALL_FEATURE
    assert ctx_small.autonomy_level == 0.80
    
    # 3. Test Hotfix routing
    req_hotfix = TaskRequest("t-3", "Fix crash on line 42", ["file.py"], 0.20)
    ctx_hotfix = pipeline.intake_and_triage(req_hotfix)
    assert ctx_hotfix.task_type == TaskType.HOTFIX
    assert ctx_hotfix.autonomy_level == 0.75
    
    # 4. Test Refactor routing
    req_refactor = TaskRequest("t-4", "Refactor core loop logic", ["file.py"], 0.20)
    ctx_refactor = pipeline.intake_and_triage(req_refactor)
    assert ctx_refactor.task_type == TaskType.REFACTOR
    assert ctx_refactor.autonomy_level == 0.85

def test_discovery_and_planning_stages():
    pipeline = QuantumRulesPipeline()
    req = TaskRequest("t-1", "Build amazing engine", ["file.py"], 0.95)
    ctx = pipeline.intake_and_triage(req)
    
    discovery_ctx = pipeline.execute_discovery(ctx)
    assert len(discovery_ctx) > 0
    assert "ADR-0005" in discovery_ctx[-1]
    
    plan = pipeline.execute_planning(ctx, discovery_ctx)
    assert len(plan) == 3
    assert "Brazilian business logic" in plan[-1]
    
    # Test hotfix skips planning weight
    ctx_hot = pipeline.intake_and_triage(TaskRequest("t-2", "fix this bug", ["file.py"], 0.1))
    plan_hot = pipeline.execute_planning(ctx_hot, ["Fast"])
    assert len(plan_hot) == 2
    assert "immediate source fix" in plan_hot[0]

def test_task_decomposition():
    pipeline = QuantumRulesPipeline()
    req = TaskRequest("t-1", "Feature", ["file.py"], 0.5)
    ctx = pipeline.intake_and_triage(req)
    
    subtasks = pipeline.execute_task_decomposition(ctx)
    assert len(subtasks) == 3
    assert subtasks[0].assigned_agent == "Backend_Agent"
    
    # Hotfix decomposition is simple
    ctx_hot = pipeline.intake_and_triage(TaskRequest("t-2", "fix", ["file.py"], 0.1))
    sub_hot = pipeline.execute_task_decomposition(ctx_hot)
    assert len(sub_hot) == 1

def test_implementation_autocorrect_loop():
    pipeline = QuantumRulesPipeline()
    req = TaskRequest("t-1", "Fix", ["file.py"], 0.1)
    ctx = pipeline.intake_and_triage(req)
    pipeline.execute_task_decomposition(ctx)
    
    # Run with generator that fails first attempt, autocorrects on second
    changes = pipeline.execute_implementation_loop(ctx, "file.py", mock_code_generator_retry)
    assert "file.py" in changes
    assert "valid clean" in changes["file.py"]
    assert ctx.subtasks[0].is_completed is True
    assert ctx.subtasks[0].tests_passed is True

def test_parallel_qa_security_and_confidence_gate():
    pipeline = QuantumRulesPipeline()
    req = TaskRequest("t-1", "Refactor", ["file.py"], 0.4)
    ctx = pipeline.intake_and_triage(req)
    
    # Scenario 1: High quality -> gate passed
    pipeline.execute_qa_and_security_parallel(ctx, mock_qa_runner_high, mock_sec_runner_high)
    assert ctx.confidence_score > 0.90
    assert pipeline.execute_confidence_gate(ctx) is True
    
    # Scenario 2: Low quality -> gate failed with HumanEscalationNeeded
    pipeline.execute_qa_and_security_parallel(ctx, mock_qa_runner_low, mock_sec_runner_low)
    assert ctx.confidence_score < 0.50
    with pytest.raises(HumanEscalationNeeded):
        pipeline.execute_confidence_gate(ctx)

def test_self_verification_rollback_and_review():
    pipeline = QuantumRulesPipeline()
    req = TaskRequest("t-1", "Refactor", ["file.py"], 0.4)
    ctx = pipeline.intake_and_triage(req)
    ctx.staged_changes["file.py"] = "Code"
    
    # Failing integration tests trigger rollback
    success = pipeline.execute_self_verification(ctx, mock_integration_test_failed)
    assert success is False
    assert len(ctx.staged_changes) == 0
    assert ctx.status == TaskStatus.FAILED
    
    # Passing integration tests keep code
    ctx_pass = pipeline.intake_and_triage(req)
    ctx_pass.staged_changes["file.py"] = "Code"
    success_pass = pipeline.execute_self_verification(ctx_pass, mock_integration_test_passed)
    assert success_pass is True
    assert len(ctx_pass.staged_changes) == 1
    
    # Review Approved
    approved = pipeline.execute_code_review(ctx_pass, mock_reviewer_approved)
    assert approved is True

def test_integration_release_and_feedback():
    pipeline = QuantumRulesPipeline()
    req = TaskRequest("t-1", "Large Feature", ["file.py"], 0.95)
    ctx = pipeline.intake_and_triage(req)
    ctx.staged_changes["file.py"] = "Code"
    ctx.self_verification_passed = True
    ctx.review_approved = True
    
    commit_msg = pipeline.execute_integration(ctx)
    assert "integrate" in commit_msg
    assert ctx.is_integrated is True
    
    changelog = pipeline.execute_documentation_and_changelog(ctx)
    assert "Changelog" in changelog
    
    release_info = pipeline.execute_release(ctx)
    assert release_info["strategy"] == "canary_rollout_5_percent"
    
    # Small feature rollout strategy
    ctx_small = pipeline.intake_and_triage(TaskRequest("t-2", "Small", ["file.py"], 0.4))
    release_small = pipeline.execute_release(ctx_small)
    assert release_small["strategy"] == "direct_deployment"
    
    # Feedback loop completes SUCCESS state
    success = pipeline.execute_feedback_loop(ctx)
    assert success is True
    assert ctx.status == TaskStatus.SUCCESS

def test_full_pipeline_run_success():
    pipeline = QuantumRulesPipeline()
    req = TaskRequest("t-full-success", "Add high score metric", ["core.py"], 0.5)
    
    ctx = pipeline.run_full_pipeline(
        req=req,
        mock_code_gen=mock_code_generator_success,
        mock_qa=mock_qa_runner_high,
        mock_sec=mock_sec_runner_high,
        mock_integration_tests=mock_integration_test_passed,
        mock_reviewer=mock_reviewer_approved
    )
    
    assert ctx.status == TaskStatus.SUCCESS
    assert ctx.is_integrated is True
    assert ctx.self_verification_passed is True
    assert ctx.review_approved is True
    assert ctx.telemetry_logged is True
    assert ctx.memory_updated is True

def test_uncovered_branches_and_edges():
    pipeline = QuantumRulesPipeline()
    
    # 1. Research routing (the else block in triage)
    req_research = TaskRequest("t-res", "Investigate quantum computing", ["notes.txt"], 0.1)
    ctx_res = pipeline.intake_and_triage(req_research)
    assert ctx_res.task_type == TaskType.RESEARCH
    assert ctx_res.autonomy_level == 0.70
    
    # 2. Hotfix parallel scoring weighting
    req_hot = TaskRequest("t-hot", "Emergency hotfix patch", ["hot.py"], 0.1)
    ctx_hot = pipeline.intake_and_triage(req_hot)
    pipeline.execute_qa_and_security_parallel(ctx_hot, mock_qa_runner_high, mock_sec_runner_high)
    # hotfix weight: (qa * 0.4) + (sec * 0.6) = (0.95 * 0.4) + (0.98 * 0.6) = 0.38 + 0.588 = 0.968
    assert abs(ctx_hot.confidence_score - 0.968) < 1e-5
    
    # 3. Integration not approved/verified should return empty string
    ctx_unapproved = pipeline.intake_and_triage(req_research)
    ctx_unapproved.review_approved = False
    ctx_unapproved.self_verification_passed = True
    assert pipeline.execute_integration(ctx_unapproved) == ""

