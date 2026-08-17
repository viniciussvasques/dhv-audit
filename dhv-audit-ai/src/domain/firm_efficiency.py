from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class AuditorTimesheet:
    """
    Registro manual de horas (timesheet) enviado pelo auditor.
    """
    id: str
    auditor_id: str
    hours_declared: float
    project_id: str
    date_str: str              # formato YYYY-MM-DD

@dataclass
class SystemActivityLog:
    """
    Log real de atividade passiva de uso de sistema pelo auditor.
    """
    id: str
    auditor_id: str
    action_type: str           # ex: "finding_validation", "rag_query", "pdf_view"
    timestamp: datetime

@dataclass
class InternalAuditorProfile:
    """
    Perfil consolidado de efici?ncia e fidedignidade de timesheet do pr?prio auditor da DHV Log.
    """
    auditor_id: str
    declared_hours: float
    active_system_hours: float # Horas reais registradas ativamente no sistema
    timesheet_fidelity: float  # Taxa de fidedignidade (active_system_hours / declared_hours, limit 1.0)
    validation_count: int      # N?mero de achados validados
    avg_response_time_sec: float # Tempo m?dio de valida??o por documento
    eqcr_rejection_rate: float # Taxa de rejei??o do revisor 4 olhos (0.0 a 1.0)
    base_salary: float
    savings_captured_driven: float # Savings gerados para os clientes pelo auditor (R$)
    gain_share_bonus: float    # B?nus adicional calculado com base nos savings reais capturados

class InternalFirmEfficiencyEngine:
    """
    Motor interno de auditoria de performance da consultoria (MPE-IC).
    Aplica o princ?pio "Lead-by-Example", auditando timesheets, aferindo
    efici?ncia operacional e calculando a folha de b?nus por sucesso.
    """

    def audit_timesheet_fidelity(
        self,
        timesheets: List[AuditorTimesheet],
        logs: List[SystemActivityLog]
    ) -> Dict[str, float]:
        """
        Mede a taxa de fidedignidade de timesheet de cada auditor cruzando a declara??o
        de horas com a atividade operacional detectada no workspace.
        """
        auditor_declared: Dict[str, float] = {}
        for t in timesheets:
            auditor_declared[t.auditor_id] = auditor_declared.get(t.auditor_id, 0.0) + t.hours_declared

        # Consolida horas de atividade real por auditor baseando-se em janelas de atividade (ex: sess?es de 10 min)
        # Vamos assumir que cada log garante que o auditor esteve ativo nos 10 minutos subsequentes
        auditor_active_seconds: Dict[str, set] = {}
        for l in logs:
            aud_id = l.auditor_id
            auditor_active_seconds.setdefault(aud_id, set())
            # Adiciona os segundos do minuto da atividade para agrupar janelas de forma robusta
            base_epoch = int(l.timestamp.timestamp() // 60) * 60
            for i in range(10): # Atividade estendida por 10 minutos
                auditor_active_seconds[aud_id].add(base_epoch + i * 60)

        fidelities: Dict[str, float] = {}
        for aud_id, declared in auditor_declared.items():
            if declared <= 0:
                fidelities[aud_id] = 1.0
                continue
                
            active_minutes = len(auditor_active_seconds.get(aud_id, set()))
            active_hours = active_minutes / 60.0
            
            fidelity = active_hours / declared
            fidelities[aud_id] = round(max(0.0, min(1.0, fidelity)), 4)

        return fidelities

    def calculate_firm_payroll(
        self,
        auditor_id: str,
        base_salary: float,
        savings_driven: float,
        fidelity_score: float,
        rejection_rate: float
    ) -> float:
        """
        Calcula as bonifica??es de folha de pagamento por ganho de sucesso do auditor.
        O b?nus de comiss?o cresce de acordo com o saving gerado, mas ? penalizado
        caso a fidedignidade de timesheet seja baixa ou a taxa de rejei??o de qualidade
        do EQCR seja elevada.
        """
        if fidelity_score < 0.5:
            # Penalidade severa por timesheets fraudulentos
            gain_share_multiplier = 0.0
        else:
            # Multiplicador proporcional ao comprometimento operacional
            gain_share_multiplier = fidelity_score

        # Qualidade penaliza o b?nus: se tiver 30% de rejei??o no EQCR, perde 30% do b?nus
        quality_multiplier = 1.0 - rejection_rate
        
        # O b?nus base ? 1% sobre o saving real capturado pelo auditor
        base_bonus = savings_driven * 0.01
        
        final_bonus = base_bonus * gain_share_multiplier * max(0.0, quality_multiplier)
        return round(final_bonus, 2)
