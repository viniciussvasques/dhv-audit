import math
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ActivityRecord:
    """
    Representa o registro detalhado de uma atividade executada por um recurso 
    (colaborador, motorista, sistema de software, filial).
    """
    id: str
    resource_id: str          # Identificador do colaborador/motorista/sistema (ex: "motorista-A")
    activity_type: str        # Tipo de atividade (ex: "delivery_route", "invoice_parsing")
    context_key: str          # Contexto espec?fico para homogeneidade (ex: rota "SP-RJ", tipo de nota "NFS-e")
    cost_incurred: float      # Custo associado ? atividade (ex: combust?vel em R$, horas extras pagas)
    units_produced: float     # Output gerado (ex: Km rodados, notas digitadas, entregas feitas)
    duration_hours: float     # Tempo decorrido em horas
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class ResourceProfile:
    """
    Perfil consolidado de efici?ncia individual e diagn?stico do recurso.
    """
    resource_id: str
    activity_type: str
    context_key: str
    total_cost: float
    total_units: float
    total_hours: float
    unit_cost: float          # Custo por unidade produzida (R$ / unidade)
    hourly_yield: float       # Rendimento por hora (unidades / hora)
    relative_efficiency: float # Score de efici?ncia comparativa com os pares (0.0 a 1.0)
    annual_waste_estimate: float # Estimativa anual de vazamento financeiro (R$) se mantido o rendimento atual vs. a mediana dos pares

@dataclass
class CohortBenchmark:
    """
    M?tricas de refer?ncia (benchmark) para um grupo de controle id?ntico (mesma atividade e contexto).
    """
    activity_type: str
    context_key: str
    mean_unit_cost: float
    median_unit_cost: float
    mean_hourly_yield: float
    median_hourly_yield: float
    best_unit_cost: float
    total_records: int

class ResourceEfficiencyProfiler:
    """
    Motor original de Perfilamento e Efici?ncia Individual de Recursos (MPE-IR).
    Compara de forma justa colaboradores, ativos e sistemas operando sob as mesmas
    circunst?ncias (ex: Motorista A vs. Motorista B na mesma rota), quantificando o
    desperd?cio oculto e projetando a perda anual acumulada centavo a centavo.
    """

    def calculate_benchmarks(self, records: List[ActivityRecord]) -> Dict[str, CohortBenchmark]:
        """
        Agrupa os registros por coorte (activity_type + context_key) e calcula
        as m?tricas de tend?ncia central e melhores pr?ticas de mercado.
        """
        cohorts: Dict[str, List[ActivityRecord]] = {}
        for r in records:
            key = f"{r.activity_type}||{r.context_key}"
            cohorts.setdefault(key, []).append(r)

        benchmarks: Dict[str, CohortBenchmark] = {}
        for key, r_list in cohorts.items():
            act_type, ctx_key = key.split("||")
            
            # Consolida por recurso na coorte para evitar vi?s de frequ?ncia de viagem
            resource_data: Dict[str, Dict[str, float]] = {}
            for r in r_list:
                res = r.resource_id
                resource_data.setdefault(res, {"cost": 0.0, "units": 0.0, "hours": 0.0})
                resource_data[res]["cost"] += r.cost_incurred
                resource_data[res]["units"] += r.units_produced
                resource_data[res]["hours"] += r.duration_hours

            unit_costs: List[float] = []
            yields: List[float] = []
            
            for res, metrics in resource_data.items():
                units = metrics["units"]
                hours = metrics["hours"]
                cost = metrics["cost"]
                
                if units > 0:
                    unit_costs.append(cost / units)
                if hours > 0:
                    yields.append(units / hours)

            if not unit_costs:
                continue

            unit_costs.sort()
            yields.sort()

            n_costs = len(unit_costs)
            n_yields = len(yields)

            # C?lculo de mediana de custos
            if n_costs % 2 == 1:
                median_cost = unit_costs[n_costs // 2]
            else:
                median_cost = (unit_costs[(n_costs // 2) - 1] + unit_costs[n_costs // 2]) / 2.0

            # C?lculo de mediana de rendimento
            if n_yields % 2 == 1:
                median_yield = yields[n_yields // 2]
            else:
                median_yield = (yields[(n_yields // 2) - 1] + yields[n_yields // 2]) / 2.0

            mean_cost = sum(unit_costs) / n_costs
            mean_yield = sum(yields) / n_yields
            best_cost = unit_costs[0]

            benchmarks[key] = CohortBenchmark(
                activity_type=act_type,
                context_key=ctx_key,
                mean_unit_cost=round(mean_cost, 4),
                median_unit_cost=round(median_cost, 4),
                mean_hourly_yield=round(mean_yield, 4),
                median_hourly_yield=round(median_yield, 4),
                best_unit_cost=round(best_cost, 4),
                total_records=len(r_list)
            )

        return benchmarks

    def profile_resources(self, records: List[ActivityRecord]) -> List[ResourceProfile]:
        """
        Gera o perfilamento de efici?ncia individual comparativo de cada recurso em seus respectivos contextos.
        Estima a perda anual com base em um ano operacional padr?o (ex: 250 dias ?teis ou 2.000h de trabalho).
        """
        benchmarks = self.calculate_benchmarks(records)
        
        # Consolida hist?rico de cada recurso por coorte
        resource_profiles: Dict[str, Dict[str, float]] = {}
        for r in records:
            key = f"{r.resource_id}||{r.activity_type}||{r.context_key}"
            resource_profiles.setdefault(key, {"cost": 0.0, "units": 0.0, "hours": 0.0, "count": 0})
            resource_profiles[key]["cost"] += r.cost_incurred
            resource_profiles[key]["units"] += r.units_produced
            resource_profiles[key]["hours"] += r.duration_hours
            resource_profiles[key]["count"] += 1

        profiles: List[ResourceProfile] = []
        for key, metrics in resource_profiles.items():
            res_id, act_type, ctx_key = key.split("||")
            cohort_key = f"{act_type}||{ctx_key}"
            
            if cohort_key not in benchmarks:
                continue
                
            bench = benchmarks[cohort_key]
            cost = metrics["cost"]
            units = metrics["units"]
            hours = metrics["hours"]

            if units <= 0 or hours <= 0:
                continue

            unit_cost = cost / units
            hourly_yield = units / hours

            # C?lculo de Efici?ncia Relativa (0.0 a 1.0)
            # 1.0 significa que o recurso est? no topo de efici?ncia (menor custo unit?rio).
            if unit_cost <= bench.best_unit_cost:
                relative_efficiency = 1.0
            else:
                # O score decai ? medida que o custo unit?rio se afasta do melhor custo da coorte
                relative_efficiency = bench.best_unit_cost / unit_cost

            # Estimativa de Desperd?cio Anual Acumulado (R$) vs. Mediana dos Pares
            # Representa o "vazamento invis?vel" se o recurso continuar performando abaixo do par mediano
            annual_waste = 0.0
            if unit_cost > bench.median_unit_cost:
                # Diferen?a de custo por unidade produzida
                delta_cost = unit_cost - bench.median_unit_cost
                # Projeta para um ano operacional. Vamos estimar a produ??o anual replicando a taxa hist?rica
                # para uma m?dia de 1.800 horas produtivas por ano.
                annual_projected_units = (units / hours) * 1800.0
                annual_waste = delta_cost * annual_projected_units

            profiles.append(ResourceProfile(
                resource_id=res_id,
                activity_type=act_type,
                context_key=ctx_key,
                total_cost=round(cost, 2),
                total_units=round(units, 2),
                total_hours=round(hours, 2),
                unit_cost=round(unit_cost, 4),
                hourly_yield=round(hourly_yield, 4),
                relative_efficiency=round(relative_efficiency, 4),
                annual_waste_estimate=round(annual_waste, 2)
            ))

        return profiles
