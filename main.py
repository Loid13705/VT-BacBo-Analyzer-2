
#!/usr/bin/env python3
"""
VT BacBo Analyzer - Main Entry Point
Aplicativo profissional para análise de tendências do Bac Bo
"""
import tkinter as tk
from gui import BacBoAnalyzerApp

def main():
    """Função principal que inicia a aplicação"""
    try:
        root = tk.Tk()
        app = BacBoAnalyzerApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
