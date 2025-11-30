import os
import subprocess
import sys

def install_pyinstaller():
    """Instala o PyInstaller se não estiver instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller já está instalado")
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller instalado com sucesso!")

def compile_app():
    """Compila o aplicativo para .exe"""
    
    # Verificar se o logo existe
    if not os.path.exists("assets/logo.ico"):
        print("❌ ERRO: Arquivo assets/logo.ico não encontrado!")
        print("Execute primeiro: python create_logo.py")
        return False
    
    # Nome do arquivo principal
    main_script = "main.py"
    
    if not os.path.exists(main_script):
        print(f"❌ ERRO: {main_script} não encontrado!")
        return False
    
    print("🔨 Compilando aplicativo...")
    
    # Comando do PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",           # Cria um único arquivo .exe
        "--windowed",          # Aplicativo sem console
        f"--icon=assets/logo.ico",
        f"--name=VT_BacBo_Analyzer",
        "--clean",             # Limpa arquivos temporários
        "--noconfirm",         # Não pergunta para sobrescrever
        main_script
    ]
    
    try:
        # Executar o comando
        subprocess.run(cmd, check=True)
        print("✅ Compilação concluída com sucesso!")
        print(f"📁 Seu .exe está em: dist/VT_BacBo_Analyzer.exe")
        
        # Verificar se o arquivo foi criado
        if os.path.exists("dist/VT_BacBo_Analyzer.exe"):
            print("🎉 Aplicativo compilado com sucesso!")
            return True
        else:
            print("❌ Erro: Arquivo .exe não foi criado")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na compilação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 50)
    print("VT BACBO ANALYZER - COMPILADOR")
    print("=" * 50)
    
    # Instalar PyInstaller se necessário
    install_pyinstaller()
    
    # Compilar
    if compile_app():
        print("\n🎯 COMPILAÇÃO CONCLUÍDA!")
        print("📍 Arquivo: dist/VT_BacBo_Analyzer.exe")
        print("📏 Tamanho: Verifique o arquivo na pasta 'dist'")
    else:
        print("\n💥 COMPILAÇÃO FALHOU!")
        print("Verifique os erros acima.")

if __name__ == "__main__":
    main()
