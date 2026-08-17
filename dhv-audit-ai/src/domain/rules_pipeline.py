import math
import uuid
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class TaskType(str, Enum):
    HOTFIX = "hotfix"
    SMALL_FEATURE = "small_feature"
    LARGE_FEATURE = "large_feature"
    REFACTOR = "refactor"
    RESEARCH = "research"

class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ESCALATED = "escalated"

@dataclass
class TaskRequest:
    id: str
    description: str
    target_files: List[str]
    complexity_score: float # 0.0 to 1.0

@dataclass
class SubTask:
    id: str
    title: str
    assigned_agent: str
    code_diff: str = ""
    is_completed: bool = False
    tests_passed: bool = False

@dataclass
class PipelineContext:
    task_id: str
    task_type: TaskType
    autonomy_level: float # threshold for confidence (0.0 to 1.0)
    staged_changes: Dict[str, str] = field(default_factory=dict) # filepath -> code diff
    plan: List[str] = field(default_factory=list)
    subtasks: List[SubTask] = field(default_factory=list)
    qa_score: float = 0.0
    security_score: float = 0.0
    confidence_score: float = 0.0
    self_verification_passed: bool = False
    review_approved: bool = False
    is_integrated: bool = False
    changelog: str = ""
    telemetry_logged: bool = False
    memory_updated: bool = False
    escalation_reason: Optional[str] = None
    status: TaskStatus = TaskStatus.NOT_STARTED

class HumanEscalationNeeded(Exception):
    """Exce??o levantada quando o gate de confian?a falha e exige interven??o humana."""
    def __init__(self, message: str):
        super().__init__(message)

class QuantumRulesPipeline:
    """
    Orquestrador Unificado do Quantum Rules Pipeline.
    Implementa um fluxo de desenvolvimento e verifica??o de regras e tarefas estruturado em 13 fases,
    apoiando-se em decis?es probabil?sticas, execu??o paralela, gates de qualidade e autocorre??o.
    """

    def __init__(self, default_autonomy_threshold: float = 0.85):
        self.default_autonomy_threshold = default_autonomy_threshold

    # --- FASE 0: Intake & Triage ---
    def intake_and_triage(self, req: TaskRequest) -> PipelineContext:
        """
        Classifica e define a rota ideal da tarefa, pulando fases irrelevantes 
        e definindo o threshold de autonomia.
        """
        # Regra de roteamento inteligente
        if req.complexity_score >= 0.8:
            task_type = TaskType.LARGE_FEATURE
            autonomy_level = 0.90 # Exige confian?a alt?ssima
        elif req.complexity_score >= 0.4:
            task_type = TaskType.SMALL_FEATURE
            autonomy_level = 0.80
        elif "fix" in req.description.lower() or "hotfix" in req.description.lower():
            task_type = TaskType.HOTFIX
            autonomy_level = 0.75 # R?pido e pr?tico, mais aut?nomo para emerg?ncias
        elif "refactor" in req.description.lower():
            task_type = TaskType.REFACTOR
            autonomy_level = 0.85
        else:
            task_type = TaskType.RESEARCH
            autonomy_level = 0.70

        ctx = PipelineContext(
            task_id=req.id,
            task_type=task_type,
            autonomy_level=autonomy_level,
            status=TaskStatus.IN_PROGRESS
        )
        return ctx

    # --- FASE 1: Discovery ---
    def execute_discovery(self, ctx: PipelineContext) -> List[str]:
        """
        L? hist?rico, decision logs e indexa??es anteriores para contextualizar a tarefa.
        """
        discovered_contexts = [f"Loaded architectural logs for task_type: {ctx.task_type}"]
        if ctx.task_type == TaskType.LARGE_FEATURE:
            discovered_contexts.append("Memory retrieved: similar decisions made on ADR-0005.")
        else:
            discovered_contexts.append("Fast discovery mode activated.")
        return discovered_contexts

    # --- FASE 2: Planning & Architecture ---
    def execute_planning(self, ctx: PipelineContext, discovered_context: List[str]) -> List[str]:
        """
        Gera um plano de to-do list vis?vel antes de tocar no c?digo.
        """
        # Hotfixes e pesquisas pulam planejamento pesado
        if ctx.task_type == TaskType.HOTFIX:
            plan = ["Apply immediate source fix", "Verify build status"]
        else:
            plan = [
                f"Analyze dependencies based on: {discovered_context[-1]}",
                "Draft changes under Clean Architecture modules",
                "Add core unit tests validating Brazilian business logic"
            ]
        ctx.plan = plan
        return plan

    # --- FASE 3: Task Decomposition ---
    def execute_task_decomposition(self, ctx: PipelineContext) -> List[SubTask]:
        """
        Quebra o plano em tarefas at?micas para subagentes especializados.
        """
        if ctx.task_type in [TaskType.HOTFIX, TaskType.RESEARCH]:
            # Decomposi??o simples
            subtasks = [SubTask("sub-1", "Apply single-file code patch", "Backend_Agent")]
        else:
            subtasks = [
                SubTask("sub-1", "Implement domain logic structures", "Backend_Agent"),
                SubTask("sub-2", "Add validation rules in interface routers", "QA_Agent"),
                SubTask("sub-3", "Review authentication schemas", "Security_Agent")
            ]
        ctx.subtasks = subtasks
        return subtasks

    # --- FASE 4: Implementation Loop (Loop de Autocorre??o) ---
    def execute_implementation_loop(self, ctx: PipelineContext, filepath: str, mock_code_generator) -> Dict[str, str]:
        """
        Executa o loop interativo de escrita de c?digo -> teste local -> corre??o autom?tica.
        """
        attempts = 0
        max_attempts = 3
        local_test_passed = False
        staged_code = ""

        while not local_test_passed and attempts < max_attempts:
            attempts += 1
            staged_code = mock_code_generator(filepath, attempts)
            # Simula a valida??o de teste local: na ?ltima tentativa ou com sorte, o teste local passa
            if attempts == max_attempts or "valid" in staged_code.lower():
                local_test_passed = True

        ctx.staged_changes[filepath] = staged_code
        # Atualiza o status das subtasks associadas ao arquivo
        for sub in ctx.subtasks:
            sub.is_completed = True
            sub.tests_passed = local_test_passed
            sub.code_diff = staged_code

        return ctx.staged_changes

    # --- FASE 5: QA + Security (Execu??o Paralela) ---
    def execute_qa_and_security_parallel(self, ctx: PipelineContext, mock_qa_runner, mock_sec_runner) -> Dict[str, float]:
        """
        Executa os testes de QA e varredura de Seguran?a de forma paralela.
        Mede o Score de Confian?a agregado.
        """
        # Simula paralelismo rodando ambos e recebendo scores independentes
        qa_score = mock_qa_runner(ctx)
        sec_score = mock_sec_runner(ctx)

        ctx.qa_score = qa_score
        ctx.security_score = sec_score
        
        # O score de confian?a agregado depende do tipo de tarefa
        if ctx.task_type == TaskType.HOTFIX:
            # Em hotfixes, a seguran?a tem peso cr?tico
            ctx.confidence_score = (qa_score * 0.4) + (sec_score * 0.6)
        else:
            ctx.confidence_score = (qa_score * 0.5) + (sec_score * 0.5)
            
        return {"qa_score": qa_score, "security_score": sec_score, "confidence_score": ctx.confidence_score}

    # --- FASE 6: Gate de Confian?a ---
    def execute_confidence_gate(self, ctx: PipelineContext) -> bool:
        """
        Garante que se a confian?a agregada estiver abaixo do threshold, 
        o sistema pausa e escala para o humano (Human-in-the-Loop).
        """
        if ctx.confidence_score < ctx.autonomy_level:
            ctx.status = TaskStatus.ESCALATED
            ctx.escalation_reason = (
                f"Confidence score {ctx.confidence_score:.2f} is below "
                f"required autonomy threshold of {ctx.autonomy_level:.2f}."
            )
            raise HumanEscalationNeeded(ctx.escalation_reason)
        return True

    # --- FASE 7: Self-Verification Loop ---
    def execute_self_verification(self, ctx: PipelineContext, mock_integration_test_runner) -> bool:
        """
        Roda o build completo, linter e testes de integra??o.
        """
        success = mock_integration_test_runner(ctx)
        ctx.self_verification_passed = success
        if not success:
            # Rollback das mudan?as
            ctx.staged_changes.clear()
            ctx.status = TaskStatus.FAILED
        return success

    # --- FASE 8: Code Review ---
    def execute_code_review(self, ctx: PipelineContext, mock_reviewer_agent) -> bool:
        """
        Garante uma revis?o de c?digo por agente independente ou humano (granular).
        """
        approved = mock_reviewer_agent(ctx)
        ctx.review_approved = approved
        return approved

    # --- FASE 9: Integration ---
    def execute_integration(self, ctx: PipelineContext) -> str:
        """
        Realiza o merge e gera a commit message formatada.
        """
        if ctx.review_approved and ctx.self_verification_passed:
            ctx.is_integrated = True
            commit_msg = f"feat: integrate changes for task {ctx.task_id} under {ctx.task_type} flow"
            return commit_msg
        return ""

    # --- FASE 10: Documentation & Changelog ---
    def execute_documentation_and_changelog(self, ctx: PipelineContext) -> str:
        """
        Auto-gera o changelog de documenta??o e cria ADR se aplic?vel.
        """
        changelog = f"## Task {ctx.task_id} Changelog\n"
        changelog += f"Type: {ctx.task_type}\n"
        for filepath in ctx.staged_changes.keys():
            changelog += f"- Modified: {filepath}\n"
        ctx.changelog = changelog
        return changelog

    # --- FASE 11: Release ---
    def execute_release(self, ctx: PipelineContext) -> Dict[str, Any]:
        """
        Simula o staged rollout ou ativa??o de feature flag.
        """
        if ctx.task_type == TaskType.LARGE_FEATURE:
            strategy = "canary_rollout_5_percent"
        else:
            strategy = "direct_deployment"
        return {"task_id": ctx.task_id, "strategy": strategy, "status": "deployed"}

    # --- FASE 12: Feedback Loop ---
    def execute_feedback_loop(self, ctx: PipelineContext) -> bool:
        """
        Injeta telemetria e atualiza a mem?ria de projeto.
        """
        ctx.telemetry_logged = True
        ctx.memory_updated = True
        ctx.status = TaskStatus.SUCCESS
        return True

    def run_full_pipeline(
        self,
        req: TaskRequest,
        mock_code_gen,
        mock_qa,
        mock_sec,
        mock_integration_tests,
        mock_reviewer
    ) -> PipelineContext:
        """
        Orquestra a execu??o ponta a ponta do Quantum Rules Pipeline.
        """
        # Fase 0
        ctx = self.intake_and_triage(req)
        
        # Fase 1
        discovery_ctx = self.execute_discovery(ctx)
        
        # Fase 2
        self.execute_planning(ctx, discovery_ctx)
        
        # Fase 3
        self.execute_task_decomposition(ctx)
        
        # Fase 4
        for file in req.target_files:
            self.execute_implementation_loop(ctx, file, mock_code_gen)
            
        # Fase 5
        self.execute_qa_and_security_parallel(ctx, mock_qa, mock_sec)
        
        # Fase 6: Confidence Gate (Pode dar Raise na exce??o)
        self.execute_confidence_gate(ctx)
        
        # Fase 7
        self.execute_self_verification(ctx, mock_integration_tests)
        
        # Fase 8
        self.execute_code_review(ctx, mock_reviewer)
        
        # Fase 9
        self.execute_integration(ctx)
        
        # Fase 10
        self.execute_documentation_and_changelog(ctx)
        
        # Fase 11
        self.execute_release(ctx)
        
        # Fase 12
        self.execute_feedback_loop(ctx)
        
        return ctx
