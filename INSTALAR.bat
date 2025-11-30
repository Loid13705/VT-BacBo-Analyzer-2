@echo off
echo ========================================
echo    VT BACBO ANALYZER - INSTALADOR
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo Baixe em: https://www.python.org/downloads/
    echo Instale Python e execute novamente.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
echo.

echo Instalando dependências...
pip install -r requirements.txt

echo.
echo Criando logo do aplicativo...
python scripts/create_logo.py

echo.
echo Compilando aplicativo...
python scripts/compile.py

echo.
if exist "dist\VT_BacBo_Analyzer.exe" (
    echo ✅ INSTALAÇÃO CONCLUÍDA!
    echo.
    echo 📁 Seu aplicativo está em: dist\VT_BacBo_Analyzer.exe
    echo.
    echo 🚀 Deseja executar agora? (S/N)
    set /p choice=
    if /i "%choice%"=="S" (
        start dist\VT_BacBo_Analyzer.exe
    )
) else (
    echo ❌ Erro na instalação!
)

pause
