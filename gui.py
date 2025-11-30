import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import threading
from analyzer import BacBoAnalyzer
from utils import SoundManager, FileExporter
import time

class BacBoAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.analyzer = BacBoAnalyzer()
        self.sound_manager = SoundManager()
        self.file_exporter = FileExporter()
        
        self.setup_window()
        self.create_styles()
        self.create_widgets()
        self.setup_bindings()
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("VT BacBo Analyzer - Professional Edition")
        self.root.geometry("1200x800")
        self.root.configure(bg='#0d0d0d')
        self.root.resizable(True, True)
        
        # Tentar carregar o ícone
        try:
            self.root.iconbitmap("assets/logo.ico")
        except:
            pass
        
    def create_styles(self):
        """Cria estilos personalizados para os widgets"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configurar estilos futuristas
        self.style.configure('Neon.TFrame', background='#0d0d0d')
        self.style.configure('Neon.TLabel', 
                           background='#0d0d0d', 
                           foreground='#00ffea',
                           font=('Consolas', 10, 'bold'))
        
        self.style.configure('Neon.TButton',
                           background='#1a1a1a',
                           foreground='#00ffea',
                           bordercolor='#00ffea',
                           focuscolor='none',
                           font=('Consolas', 9, 'bold'),
                           padding=(15, 8))
        
        self.style.map('Neon.TButton',
                      background=[('active', '#00ffea'), ('pressed', '#008075')],
                      foreground=[('active', '#0d0d0d'), ('pressed', '#0d0d0d')])
        
        self.style.configure('Neon.TEntry',
                           fieldbackground='#1a1a1a',
                           foreground='#00ff00',
                           insertcolor='#00ff00')
        
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        self.create_header()
        self.create_control_panel()
        self.create_results_panel()
        self.create_charts_panel()
        self.create_status_bar()
        
    def create_header(self):
        """Cria o cabeçalho com logo e título"""
        header_frame = ttk.Frame(self.root, style='Neon.TFrame')
        header_frame.pack(fill='x', padx=20, pady=10)
        
        # Título principal
        title_label = tk.Label(header_frame,
                             text="VT BACBO ANALYZER",
                             font=('Orbitron', 24, 'bold'),
                             fg='#00ffea',
                             bg='#0d0d0d')
        title_label.pack(pady=5)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame,
                                text="Professional Analysis System",
                                font=('Consolas', 12),
                                fg='#00ff00',
                                bg='#0d0d0d')
        subtitle_label.pack(pady=2)
        
        # Separador
        separator = ttk.Separator(header_frame, orient='horizontal')
        separator.pack(fill='x', pady=10)
        
    def create_control_panel(self):
        """Cria o painel de controle"""
        control_frame = ttk.Frame(self.root, style='Neon.TFrame')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Entrada para número de jogadas
        input_frame = ttk.Frame(control_frame, style='Neon.TFrame')
        input_frame.pack(fill='x', pady=5)
        
        ttk.Label(input_frame, text="Número de Jogadas:", style='Neon.TLabel').pack(side='left')
        
        self.entry_jogadas = ttk.Entry(input_frame, width=10, style='Neon.TEntry', font=('Consolas', 12))
        self.entry_jogadas.pack(side='left', padx=10)
        self.entry_jogadas.insert(0, "10")
        
        # Botões de ação
        button_frame = ttk.Frame(control_frame, style='Neon.TFrame')
        button_frame.pack(fill='x', pady=10)
        
        self.btn_analyze = ttk.Button(button_frame, 
                                    text="🎲 ANALISAR JOGADAS", 
                                    command=self.analyze_games,
                                    style='Neon.TButton')
        self.btn_analyze.pack(side='left', padx=5)
        
        self.btn_export = ttk.Button(button_frame,
                                   text="💾 EXPORTAR DADOS",
                                   command=self.export_data,
                                   style='Neon.TButton')
        self.btn_export.pack(side='left', padx=5)
        
        self.btn_clear = ttk.Button(button_frame,
                                  text="🗑️ LIMPAR",
                                  command=self.clear_results,
                                  style='Neon.TButton')
        self.btn_clear.pack(side='left', padx=5)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(control_frame, 
                                      mode='determinate',
                                      style='Neon.Horizontal.TProgressbar')
        self.progress.pack(fill='x', pady=5)
        self.progress.pack_forget()  # Escondida inicialmente
        
    def create_results_panel(self):
        """Cria o painel de resultados"""
        results_frame = ttk.Frame(self.root, style='Neon.TFrame')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Área de resultados com scroll
        self.results_text = scrolledtext.ScrolledText(results_frame,
                                                    bg='#1a1a1a',
                                                    fg='#00ff00',
                                                    insertbackground='#00ff00',
                                                    selectbackground='#00ffea',
                                                    font=('Consolas', 10),
                                                    wrap=tk.WORD,
                                                    height=15)
        self.results_text.pack(fill='both', expand=True)
        
        # Configurar tags para formatação colorida
        self.results_text.tag_configure('header', foreground='#00ffea', font=('Consolas', 11, 'bold'))
        self.results_text.tag_configure('even', foreground='#00ff00')
        self.results_text.tag_configure('odd', foreground='#ff4444')
        self.results_text.tag_configure('stats', foreground='#ffaa00')
        
    def create_charts_panel(self):
        """Cria o painel de gráficos"""
        self.charts_frame = ttk.Frame(self.root, style='Neon.TFrame')
        self.charts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Frame para os gráficos
        self.chart_container = ttk.Frame(self.charts_frame, style='Neon.TFrame')
        self.chart_container.pack(fill='both', expand=True)
        
    def create_status_bar(self):
        """Cria a barra de status"""
        self.status_var = tk.StringVar()
        self.status_var.set("Sistema Pronto - VT BacBo Analyzer")
        
        status_bar = ttk.Label(self.root, 
                             textvariable=self.status_var,
                             style='Neon.TLabel',
                             relief='sunken',
                             anchor='w')
        status_bar.pack(side='bottom', fill='x', padx=5, pady=2)
        
    def setup_bindings(self):
        """Configura bindings de teclado"""
        self.root.bind('<Return>', lambda e: self.analyze_games())
        self.entry_jogadas.bind('<FocusIn>', self.on_entry_focus)
        
    def on_entry_focus(self, event):
        """Efeito quando entrada recebe foco"""
        self.sound_manager.play_click()
        
    def analyze_games(self):
        """Analisa as jogadas em thread separada"""
        try:
            num_jogadas = int(self.entry_jogadas.get())
            if num_jogadas <= 0:
                messagebox.showwarning("Entrada Inválida", "Digite um número positivo de jogadas.")
                return
                
            # Desabilitar botão durante análise
            self.btn_analyze.config(state='disabled')
            self.progress.pack(fill='x', pady=5)
            self.progress['maximum'] = num_jogadas
            
            # Executar em thread separada
            thread = threading.Thread(target=self._analyze_thread, args=(num_jogadas,))
            thread.daemon = True
            thread.start()
            
        except ValueError:
            messagebox.showerror("Erro", "Digite um número válido de jogadas.")
            
    def _analyze_thread(self, num_jogadas):
        """Thread para análise das jogadas"""
        try:
            self.sound_manager.play_analyze()
            self.status_var.set("Analisando jogadas...")
            
            # Gerar jogadas
            results = []
            for i in range(num_jogadas):
                result = self.analyzer.simulate_game()
                results.append(result)
                
                # Atualizar progresso
                self.root.after(0, self.update_progress, i + 1)
                time.sleep(0.01)  # Pequeno delay para animação
                
            # Processar resultados
            self.root.after(0, self.display_results, results)
            self.root.after(0, self.display_charts, results)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Erro na análise: {str(e)}"))
        finally:
            self.root.after(0, self.analysis_complete)
            
    def update_progress(self, value):
        """Atualiza a barra de progresso"""
        self.progress['value'] = value
        
    def analysis_complete(self):
        """Finaliza a análise"""
        self.btn_analyze.config(state='normal')
        self.progress.pack_forget()
        self.status_var.set("Análise concluída!")
        
    def display_results(self, results):
        """Exibe os resultados na área de texto"""
        self.results_text.delete(1.0, tk.END)
        
        # Cabeçalho
        self.results_text.insert(tk.END, "RESULTADOS DAS JOGADAS\n", 'header')
        self.results_text.insert(tk.END, "="*50 + "\n", 'header')
        
        # Resultados individuais
        for i, result in enumerate(results, 1):
            tag = 'even' if i % 2 == 0 else 'odd'
            line = f"Jogada {i:2d}: Dados ({result['dado1']}, {result['dado2']}) | "
            line += f"Total: {result['total']:2d} | "
            line += f"Resultado: {result['resultado']}\n"
            self.results_text.insert(tk.END, line, tag)
            
        # Estatísticas
        stats = self.analyzer.calculate_statistics(results)
        self.results_text.insert(tk.END, "\n" + "="*50 + "\n", 'header')
        self.results_text.insert(tk.END, "ESTATÍSTICAS:\n", 'header')
        self.results_text.insert(tk.END, f"Total de Jogadas: {stats['total_jogadas']}\n", 'stats')
        self.results_text.insert(tk.END, f"Pares: {stats['pares']} ({stats['perc_pares']:.1f}%)\n", 'stats')
        self.results_text.insert(tk.END, f"Ímpares: {stats['impares']} ({stats['perc_impares']:.1f}%)\n", 'stats')
        self.results_text.insert(tk.END, f"Média dos Totais: {stats['media_total']:.2f}\n", 'stats')
        
    def display_charts(self, results):
        """Exibe os gráficos de análise"""
        # Limpar gráficos anteriores
        for widget in self.chart_container.winfo_children():
            widget.destroy()
            
        # Criar figura matplotlib
        fig = Figure(figsize=(12, 8), facecolor='#0d0d0d')
        
        # Gráfico 1: Distribuição de resultados
        ax1 = fig.add_subplot(221)
        totals = [r['total'] for r in results]
        ax1.hist(totals, bins=range(2, 13), alpha=0.7, color='#00ffea', edgecolor='white')
        ax1.set_title('Distribuição dos Totais', color='#00ffea', fontweight='bold')
        ax1.set_facecolor('#1a1a1a')
        ax1.tick_params(colors='#00ff00')
        
        # Gráfico 2: Proporção Par/Ímpar
        ax2 = fig.add_subplot(222)
        pares = sum(1 for r in results if r['resultado'] == 'PAR')
        impares = len(results) - pares
        ax2.pie([pares, impares], 
               labels=['PAR', 'ÍMPAR'], 
               colors=['#00ff00', '#ff4444'],
               autopct='%1.1f%%',
               textprops={'color': 'white', 'fontweight': 'bold'})
        ax2.set_title('Proporção Par/Ímpar', color='#00ffea', fontweight='bold')
        
        # Gráfico 3: Tendência ao longo do tempo
        ax3 = fig.add_subplot(223)
        acumulado_pares = [sum(1 for r in results[:i+1] if r['resultado'] == 'PAR') 
                          for i in range(len(results))]
        ax3.plot(acumulado_pares, color='#00ff00', linewidth=2, marker='o')
        ax3.set_title('Tendência de Pares (Acumulado)', color='#00ffea', fontweight='bold')
        ax3.set_facecolor('#1a1a1a')
        ax3.tick_params(colors='#00ff00')
        ax3.grid(True, alpha=0.3)
        
        # Gráfico 4: Frequência dos dados
        ax4 = fig.add_subplot(224)
        dados1 = [r['dado1'] for r in results]
        dados2 = [r['dado2'] for r in results]
        ax4.hist([dados1, dados2], bins=range(1, 8), alpha=0.7, 
                label=['Dado 1', 'Dado 2'], color=['#00ffea', '#ffaa00'])
        ax4.set_title('Distribuição dos Dados', color='#00ffea', fontweight='bold')
        ax4.set_facecolor('#1a1a1a')
        ax4.tick_params(colors='#00ff00')
        ax4.legend(facecolor='#1a1a1a', labelcolor='white')
        
        fig.tight_layout(pad=3.0)
        
        # Embed no tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def export_data(self):
        """Exporta os dados para arquivo"""
        try:
            filename = self.file_exporter.export_to_file(self.analyzer.get_last_results())
            if filename:
                messagebox.showinfo("Sucesso", f"Dados exportados para: {filename}")
                self.status_var.set(f"Dados exportados: {filename}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {str(e)}")
            
    def clear_results(self):
        """Limpa todos os resultados"""
        self.results_text.delete(1.0, tk.END)
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        self.status_var.set("Resultados limpos - Pronto para nova análise")
        self.sound_manager.play_click()
        
    def __del__(self):
        """Destrutor - limpa recursos"""
        if hasattr(self, 'sound_manager'):
            self.sound_manager.cleanup()
