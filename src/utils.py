"""
Módulo de utilitários - Sons, exportação, helpers
"""
import os
import csv
import json
from datetime import datetime
try:
    import winsound
except ImportError:
    winsound = None

class SoundManager:
    """Gerenciador de efeitos sonoros"""
    
    def __init__(self):
        self.sounds_enabled = True
        self.sounds_path = "assets/sounds/"
        
    def play_click(self):
        """Toca som de clique"""
        self._play_sound(1000, 50)  # Som simples para clique
        
    def play_analyze(self):
        """Toca som de análise"""
        self._play_sound(800, 100)  # Som diferente para análise
        
    def _play_sound(self, frequency, duration):
        """Toca som usando winsound (Windows) ou alternativa"""
        if not self.sounds_enabled:
            return
            
        try:
            if winsound:
                winsound.Beep(frequency, duration)
        except:
            pass  # Silencia erros de som
    
    def toggle_sounds(self, enabled: bool):
        """Ativa/desativa sons"""
        self.sounds_enabled = enabled
        
    def cleanup(self):
        """Limpa recursos de áudio"""
        pass

class FileExporter:
    """Gerencia exportação de dados"""
    
    def __init__(self):
        self.export_dir = "exports/"
        self._ensure_export_dir()
        
    def _ensure_export_dir(self):
        """Garante que o diretório de export existe"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
            
    def export_to_file(self, data: list, format_type: str = 'auto') -> str:
        """
        Exporta dados para arquivo
        
        Args:
            data: Dados a serem exportados
            format_type: 'txt', 'csv', ou 'auto'
            
        Returns:
            Caminho do arquivo exportado
        """
        if not data:
            raise ValueError("Nenhum dado para exportar")
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == 'auto':
            format_type = 'csv' if len(data) > 10 else 'txt'
            
        filename = f"{self.export_dir}bacbo_analysis_{timestamp}.{format_type}"
        
        if format_type == 'txt':
            self._export_txt(data, filename)
        elif format_type == 'csv':
            self._export_csv(data, filename)
        else:
            raise ValueError(f"Formato não suportado: {format_type}")
            
        return filename
    
    def _export_txt(self, data: list, filename: str):
        """Exporta para arquivo texto formatado"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("VT BACBO ANALYZER - RELATÓRIO DE ANÁLISE\n")
            f.write("=" * 50 + "\n")
            f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de Jogadas: {len(data)}\n\n")
            
            f.write("DETALHES DAS JOGADAS:\n")
            f.write("-" * 40 + "\n")
            
            for i, result in enumerate(data, 1):
                line = f"Jogada {i:3d}: Dados ({result['dado1']}, {result['dado2']}) | "
                line += f"Total: {result['total']:2d} | "
                line += f"Resultado: {result['resultado']}\n"
                f.write(line)
                
    def _export_csv(self, data: list, filename: str):
        """Exporta para arquivo CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Jogada', 'Dado1', 'Dado2', 'Total', 'Resultado'])
            
            for i, result in enumerate(data, 1):
                writer.writerow([
                    i,
                    result['dado1'],
                    result['dado2'],
                    result['total'],
                    result['resultado']
                ])

class AnimationHelper:
    """Helper para animações suaves"""
    
    @staticmethod
    def fade_in(widget, duration=300):
        """Efeito fade-in para widget"""
        widget.attributes('-alpha', 0.0)
        widget.update()
        
        steps = 20
        delay = duration // steps
        
        for i in range(steps + 1):
            alpha = i / steps
            widget.attributes('-alpha', alpha)
            widget.update()
            widget.after(delay)
    
    @staticmethod
    def fade_out(widget, duration=300):
        """Efeito fade-out para widget"""
        steps = 20
        delay = duration // steps
        
        for i in range(steps, -1, -1):
            alpha = i / steps
            widget.attributes('-alpha', alpha)
            widget.update()
            widget.after(delay)
