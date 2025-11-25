@echo off

echo Iniciando o BACKEND...

echo Criando ambiente virtual...

if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

echo Ativando o ambiente virtual...
call venv\Scripts\activate

echo Instalando dependencias do backend...
pip install -r requirements.txt

echo Iniciando o servidor Flask...
python app.py

pause