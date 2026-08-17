from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from src.domain.statistical_audit import BrazilianProbabilisticAuditEngine, TransactionPayload
from src.domain.resource_efficiency import ResourceEfficiencyProfiler, ActivityRecord

@dataclass
class HAQLAnalysisResult:
    id: str
    target_id: str
    eqi_score: float             # Score unificado de vazamento (0.0 a 1.0)
    risk_level: str              # low, medium, high, critical
    annual_waste_estimate: float # Vazamento projetado acumulado em R$
    breakdown: Dict[str, float]  # Detalhamento de pesos dos vetores
    explanation: str

class HAQLUnifiedEngine:
    """
    Hyper-Audit Quantum Leakage (HAQL) Unified Engine.
    Funde os motores de estat?stica forense de Benford/Z-Score/Poisson com
    o perfilamento comparativo de rendimento de ativos e recursos para gerar
    o ?ndice de Evapora??o Qu?ntica (EQI) unificado.
    """

    def __init__(self):
        self.stats_engine = BrazilianProbabilisticAuditEngine()
        self.profile_engine = ResourceEfficiencyProfiler()

    def calculate_quantum_leakage(
        self,
        target_tx: TransactionPayload,
        all_txs: List[TransactionPayload],
        associated_activity: Optional[ActivityRecord],
        all_activities: List[ActivityRecord],
        domain: str
    ) -> HAQLAnalysisResult:
        """
        Executa a fus?o dos 4 vetores matem?ticos para calcular o EQI e projetar
        o desperd?cio anual em R$.
        """
        # 1. Avalia Vetores Estat?sticos (Benford, Z-Score, Poisson)
        stats_report = self.stats_engine.evaluate_transaction(target_tx, all_txs, domain)
        
        v_b = 1.0 - stats_report.benford_p_value if stats_report.benford_p_value < 0.1 else 0.0
        # Z-Score normalizado entre 0.0 e 1.0 (onde desvios > 3 desviam ao limite 1.0)
        v_z = min(1.0, abs(stats_report.z_score_price) / 3.0)
        v_p = 1.0 - stats_report.poisson_p_value if stats_report.poisson_p_value < 0.1 else 0.0

        # 2. Avalia Vetor de Inefici?ncia de Ativo/Recurso (MPE-IR)
        v_e = 0.0
        annual_resource_waste = 0.0
        
        if associated_activity and all_activities:
            profiles = self.profile_engine.profile_resources(all_activities)
            target_profile = next((p for p in profiles if p.resource_id == associated_activity.resource_id and p.context_key == associated_activity.context_key), None)
            if target_profile:
                v_e = 1.0 - target_profile.relative_efficiency
                annual_resource_waste = target_profile.annual_waste_estimate

        # 3. Pondera??o de Pesos baseada no Dom?nio (Normalizada)
        if domain == "hr":
            # CLT foca pesadamente em horas extras an?malas (Poisson) e rendimento ocioso (MPE-IR)
            w1, w2, w3, w4 = 0.15, 0.15, 0.40, 0.30
        elif domain == "fiscal":
            # Fiscal foca no pre?o unit?rio discrepante (Z-Score) e fraudes de numera??o (Benford)
            w1, w2, w3, w4 = 0.35, 0.45, 0.10, 0.10
        elif domain == "fleet":
            # Frota foca na efici?ncia de consumo de combust?vel e quilometragem do ativo (MPE-IR)
            w1, w2, w3, w4 = 0.10, 0.20, 0.20, 0.50
        else:
            # Padr?o equilibrado
            w1, w2, w3, w4 = 0.25, 0.25, 0.25, 0.25

        # 4. C?lculo do EQI (?ndice de Evapora??o Qu?ntica)
        eqi_score = (w1 * v_b) + (w2 * v_z) + (w3 * v_p) + (w4 * v_e)
        eqi_score = round(max(0.0, min(1.0, eqi_score)), 4)

        # 5. C?lculo do Impacto Anual Projetado Integrado
        # Soma o impacto direto do desvio do documento com a inefici?ncia do ativo projetada ao ano
        direct_saving = stats_report.financial_impact if stats_report.risk_score > 0.4 else 0.0
        total_annual_waste = direct_saving + annual_resource_waste

        # N?vel de risco consolidado
        if eqi_score >= 0.85:
            risk_level = "critical"
        elif eqi_score >= 0.60:
            risk_level = "high"
        elif eqi_score >= 0.35:
            risk_level = "medium"
        else:
            risk_level = "low"

        explanation = (
            f"An?lise HAQL unificada gerou um ?ndice de Evapora??o Qu?ntica (EQI) de {eqi_score:.2%}. "
            f"Vetor de Inconformidade de Benford: {v_b:.2%}, Vetor de Dispers?o de Pre?os Z-Score: {v_z:.2%}, "
            f"Vetor Temporal de Poisson: {v_p:.2%}, Vetor de Inefici?ncia de Ativo/Pares: {v_e:.2%}. "
            f"Impacto de vazamento anual cumulativo estimado em R$ {total_annual_waste:,.2f}."
        )

        return HAQLAnalysisResult(
            id=f"haql-{target_tx.id}",
            target_id=target_tx.id,
            eqi_score=eqi_score,
            risk_level=risk_level,
            annual_waste_estimate=round(total_annual_waste, 2),
            breakdown={
                "benford_vector": round(v_b, 4),
                "z_score_vector": round(v_z, 4),
                "poisson_vector": round(v_p, 4),
                "efficiency_vector": round(v_e, 4)
            },
            explanation=explanation
        )
