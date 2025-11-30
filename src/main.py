#!/usr/bin/env python3
"""
VT BacBo Analyzer - Main Entry Point
"""
import tkinter as tk
from gui import BacBoAnalyzerApp
import os
import sys

# Adiciona o diretório atual ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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
