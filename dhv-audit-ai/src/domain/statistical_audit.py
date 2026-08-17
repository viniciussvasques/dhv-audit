import math
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TransactionPayload:
    """
    Payload estruturado contendo dados operacionais e fiscais de uma transa??o 
    no contexto da legisla??o brasileira (NF-e, CT-e, CLT, NCM, etc.).
    """
    id: str
    value: float              # Valor financeiro da transa??o
    unit_price: float         # Pre?o unit?rio do item (produto ou servi?o)
    category_key: str         # NCM (fiscal), rubrica (CLT), ou placa de ve?culo (Frota)
    timestamp: datetime       # Data/hora do evento
    entity_id: str            # Colaborador (CLT), Fornecedor (Procurement) ou Transportadora (Log?stica)

@dataclass
class AnomalyReport:
    """
    Relat?rio consolidado de anomalias estat?sticas contendo scores probabil?sticos 
    e enquadramento legal conforme a legisla??o brasileira.
    """
    id: str
    risk_score: float         # Pontua??o final de risco compilado (0.0 a 1.0)
    benford_p_value: float    # p-valor do teste Chi-Quadrado de Benford
    z_score_price: float      # Z-Score de pre?o/valor
    poisson_p_value: float    # p-valor da distribui??o de frequ?ncia temporal
    severity: str             # low, medium, high, critical
    legal_framing: str        # Enquadramento legal brasileiro (CLT, SPED, ICMS, etc.)
    justification: str        # Detalhamento matem?tico explicativo para o consultor

class BrazilianProbabilisticAuditEngine:
    """
    Motor original de Auditoria Probabil?stica Multi-Vetor (BMV-PAE).
    Aplica testes de Benford, Z-Score e Distribui??o de Poisson de forma integrada,
    cruzando resultados com o arcabou?o fiscal e trabalhista brasileiro.
    """

    @staticmethod
    def _extract_first_digit(val: float) -> Optional[int]:
        """Extrai o primeiro d?gito significativo de um n?mero real."""
        if val <= 0:
            return None
        # Remove casas decimais e nota??o cient?fica
        s = f"{val:.10f}".replace(".", "").lstrip("0")
        if not s:
            return None
        return int(s[0])

    @staticmethod
    def _chi_squared_cdf(x: float, df: int) -> float:
        """
        Calcula a Fun??o de Distribui??o Acumulada (CDF) aproximada para Chi-Quadrado.
        DF = Graus de Liberdade. Usado para determinar o p-valor.
        """
        if x <= 0:
            return 0.0
        # Aproxima??o de Wilson-Hilferty para Chi-Quadrado com df > 2
        a = 1.0 - (2.0 / (9.0 * df))
        b = (x / df) ** (1.0 / 3.0)
        c = math.sqrt(2.0 / (9.0 * df))
        z = (b - a) / c
        # CDF Normal Padr?o aproximado para Z
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

    def test_benford_law(self, values: List[float]) -> float:
        """
        Aplica o teste Chi-Quadrado de Benford para o Primeiro D?gito.
        Retorna o p-valor. Um p-valor baixo (ex: < 0.05) indica que os dados
        n?o seguem a distribui??o natural, sugerindo fabrica??o manual ou desvios sistem?ticos.
        """
        digits = [self._extract_first_digit(v) for v in values]
        valid_digits = [d for d in digits if d is not None]
        n = len(valid_digits)

        if n < 30: # Amostra m?nima estat?stica recomendada para Benford
            return 1.0

        # Frequ?ncias esperadas de Benford para primeiro d?gito (1 a 9)
        expected_prob = {d: math.log10(1.0 + 1.0 / d) for d in range(1, 10)}
        expected_freq = {d: n * expected_prob[d] for d in range(1, 10)}

        # Contagem observada
        observed_freq = {d: 0 for d in range(1, 10)}
        for d in valid_digits:
            if d in observed_freq:
                observed_freq[d] += 1

        # Estat?stica Chi-Quadrado
        chi_stat = 0.0
        for d in range(1, 10):
            o = observed_freq[d]
            e = expected_freq[d]
            chi_stat += ((o - e) ** 2) / e

        # 8 graus de liberdade (9 classes - 1)
        cdf = self._chi_squared_cdf(chi_stat, 8)
        p_value = 1.0 - cdf
        return max(0.0, min(1.0, p_value))

    @staticmethod
    def calculate_z_score_price(value: float, values_list: List[float]) -> float:
        """
        Calcula o Z-Score para um valor espec?fico em rela??o a um hist?rico do mesmo grupo.
        Indica o qu?o distante o pre?o unit?rio ou valor est? da m?dia.
        """
        n = len(values_list)
        if n < 2:
            return 0.0
        
        mean = sum(values_list) / n
        variance = sum((x - mean) ** 2 for x in values_list) / (n - 1)
        std_dev = math.sqrt(variance)

        if std_dev == 0:
            return 0.0

        return (value - mean) / std_dev

    @staticmethod
    def _poisson_probability(k: int, lamb: float) -> float:
        """Mede a probabilidade de ocorrerem exatamente k eventos dada uma m?dia lamb."""
        if lamb <= 0:
            return 0.0
        try:
            return (lamb ** k) * math.exp(-lamb) / math.factorial(k)
        except OverflowError:
            # Prote??o contra n?meros muito grandes no c?lculo de fatorial/exponencial
            return 0.0

    def calculate_poisson_anomaly(self, event_count: int, historical_average: float) -> float:
        """
        Calcula a probabilidade de ocorr?ncia acumulada de pelo menos 'event_count' 
        eventos temporais com base na m?dia hist?rica (Poisson).
        p-valores muito baixos indicam surtos an?malos de atividade.
        """
        if historical_average <= 0:
            return 1.0
        
        # Probabilidade acumulada P(X < k)
        prob_less = 0.0
        for i in range(event_count):
            prob_less += self._poisson_probability(i, historical_average)
            if prob_less >= 1.0:
                break
        
        p_value = 1.0 - prob_less
        return max(0.0, min(1.0, p_value))

    def evaluate_transaction(
        self,
        target: TransactionPayload,
        all_transactions: List[TransactionPayload],
        domain: str
    ) -> AnomalyReport:
        """
        Analisa uma transa??o de forma hol?stica cruzando os tr?s vetores probabil?sticos.
        Gera enquadramento legal com base na legisla??o brasileira.
        """
        # Filtra transa??es do mesmo subgrupo para an?lise de Z-Score (mesmo NCM/Servi?o ou mesma Entidade)
        same_category_vals = [t.unit_price for t in all_transactions if t.category_key == target.category_key]
        
        # 1. Teste de Pre?o Relativo (Z-Score)
        z_score = self.calculate_z_score_price(target.unit_price, same_category_vals)
        z_prob = 1.0 - (0.5 * (1.0 + math.erf(abs(z_score) / math.sqrt(2.0))))
        
        # 2. Teste de Fraude Num?rica Geral (Benford)
        all_vals = [t.value for t in all_transactions]
        benford_p = self.test_benford_law(all_vals)

        # 3. Teste de Frequ?ncia Temporal An?mala (Poisson)
        # Conta quantos eventos essa mesma entidade realizou no mesmo dia da transa??o alvo
        target_date_str = target.timestamp.strftime("%Y-%m-%d")
        daily_events_for_entity = sum(
            1 for t in all_transactions 
            if t.entity_id == target.entity_id and t.timestamp.strftime("%Y-%m-%d") == target_date_str
        )
        # Calcula a m?dia hist?rica di?ria de eventos para essa entidade
        all_dates_count = {}
        for t in all_transactions:
            if t.entity_id == target.entity_id:
                d_str = t.timestamp.strftime("%Y-%m-%d")
                all_dates_count[d_str] = all_dates_count.get(d_str, 0) + 1
        
        total_days = len(all_dates_count)
        hist_avg = sum(all_dates_count.values()) / total_days if total_days > 0 else 1.0
        
        poisson_p = self.calculate_poisson_anomaly(daily_events_for_entity, hist_avg)

        # Compila??o ponderada do Risk Score (0.0 a 1.0)
        # Z-Score de Pre?o: Altos Z-Scores reduzem a probabilidade normal, aumentando o risco.
        risk_vector_z = min(1.0, abs(z_score) / 3.0) 
        # Benford: Se p-valor ? muito baixo (< 0.05), a improbabilidade de conformidade aumenta.
        risk_vector_b = 1.0 - benford_p if benford_p < 0.1 else 0.0
        # Poisson: P-valores baixos indicam anomalias na repeti??o di?ria de eventos.
        risk_vector_p = 1.0 - poisson_p if poisson_p < 0.1 else 0.0

        # Pesos de acordo com o dom?nio analisado
        if domain == "hr":
            # CLT foca pesadamente em horas extras an?malas (Poisson) e arredondamentos de verbas (Benford)
            risk_score = (risk_vector_p * 0.5) + (risk_vector_b * 0.3) + (risk_vector_z * 0.2)
            legal_framing = "CLT (Consolida??o das Leis do Trabalho) - Art. 59 (Limite de Horas Extras e Fraude de Ponto Brit?nico)."
        elif domain == "fiscal":
            # Fiscal foca no pre?o unit?rio aberrante por NCM (Z-Score) e omiss?es/fraudes de notas (Benford)
            risk_score = (risk_vector_z * 0.5) + (risk_vector_b * 0.4) + (risk_vector_p * 0.1)
            legal_framing = "Regulamento do ICMS / Decreto Federal do SPED - Diverg?ncia de Al?quota, Classifica??o de NCM e Superfaturamento Fiscal."
        elif domain == "procurement":
            # Compras foca em fracionamento de pedidos (Poisson) e desvios de pre?os contratados (Z-Score)
            risk_score = (risk_vector_p * 0.4) + (risk_vector_z * 0.4) + (risk_vector_b * 0.2)
            legal_framing = "Lei de Licita??es (Lei 14.133) / Governan?a Corporativa - Fracionamento Indevido de Despesa e Direcionamento de Sourcing."
        else:
            # Padr?o balanceado
            risk_score = (risk_vector_z * 0.33) + (risk_vector_b * 0.33) + (risk_vector_p * 0.34)
            legal_framing = "Lei Federal 12.846/2013 (Lei Anticorrup??o) e Matriz de Riscos Operacionais Corporativos."

        # Atribui??o de severidade
        if risk_score >= 0.85:
            severity = "critical"
        elif risk_score >= 0.60:
            severity = "high"
        elif risk_score >= 0.35:
            severity = "medium"
        else:
            severity = "low"

        # Detalhamento explicativo amig?vel
        justification = (
            f"Anomalia detectada com Score de Risco de {risk_score:.2%}. "
            f"Pre?o unit?rio com desvio padr?o Z-Score de {z_score:.2f} (Probabilidade de mercado: {z_prob:.4%}). "
            f"Volume di?rio de {daily_events_for_entity} eventos para a entidade possui improbabilidade de Poisson de {1.0 - poisson_p:.2%}. "
            f"O comportamento geral dos d?gitos significativos apresenta conformidade de Benford de p-valor {benford_p:.4f}."
        )

        return AnomalyReport(
            id=f"rep-{target.id}",
            risk_score=round(risk_score, 4),
            benford_p_value=round(benford_p, 4),
            z_score_price=round(z_score, 2),
            poisson_p_value=round(poisson_p, 4),
            severity=severity,
            legal_framing=legal_framing,
            justification=justification
        )
