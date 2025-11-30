"""
Módulo de análise do Bac Bo - Lógica do jogo e cálculos estatísticos
"""
import random
from typing import List, Dict, Any

class BacBoAnalyzer:
    def __init__(self):
        self.results_history = []
        
    def simulate_game(self) -> Dict[str, Any]:
        """
        Simula uma jogada do Bac Bo
        
        Returns:
            Dict com resultados da jogada
        """
        # Gera dois dados de 1 a 6
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        total = dado1 + dado2
        
        # Determina resultado (PAR/ÍMPAR)
        resultado = "PAR" if total % 2 == 0 else "ÍMPAR"
        
        result = {
            'dado1': dado1,
            'dado2': dado2,
            'total': total,
            'resultado': resultado
        }
        
        self.results_history.append(result)
        return result
    
    def calculate_statistics(self, results: List[Dict]) -> Dict[str, float]:
        """
        Calcula estatísticas dos resultados
        
        Args:
            results: Lista de resultados das jogadas
            
        Returns:
            Dict com estatísticas calculadas
        """
        if not results:
            return {}
            
        total_jogadas = len(results)
        pares = sum(1 for r in results if r['resultado'] == 'PAR')
        impares = total_jogadas - pares
        soma_totais = sum(r['total'] for r in results)
        
        return {
            'total_jogadas': total_jogadas,
            'pares': pares,
            'impares': impares,
            'perc_pares': (pares / total_jogadas) * 100,
            'perc_impares': (impares / total_jogadas) * 100,
            'media_total': soma_totais / total_jogadas
        }
    
    def analyze_trends(self, results: List[Dict], window_size: int = 5) -> List[Dict]:
        """
        Analisa tendências em janelas deslizantes
        
        Args:
            results: Lista de resultados
            window_size: Tamanho da janela para análise
            
        Returns:
            Lista com tendências calculadas
        """
        trends = []
        
        for i in range(len(results) - window_size + 1):
            window = results[i:i + window_size]
            stats = self.calculate_statistics(window)
            
            trend = {
                'window_start': i + 1,
                'window_end': i + window_size,
                'pares_in_window': stats['pares'],
                'impares_in_window': stats['impares'],
                'trend': 'PAR' if stats['pares'] > stats['impares'] else 'ÍMPAR'
            }
            trends.append(trend)
            
        return trends
    
    def get_last_results(self, count: int = None) -> List[Dict]:
        """
        Retorna os últimos resultados
        
        Args:
            count: Quantidade de resultados (None para todos)
            
        Returns:
            Lista de resultados
        """
        if count is None:
            return self.results_history.copy()
        return self.results_history[-count:]
    
    def reset_history(self):
        """Limpa o histórico de resultados"""
        self.results_history.clear()
