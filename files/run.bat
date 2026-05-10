@echo off
REM MediScript Pro - Быстрый запуск приложения
REM Скрипт для Windows

setlocal enabledelayedexpansion

echo.
echo ===================================================
echo  ^<img=26A0^> MediScript Pro - Система управления лекарствами
echo ===================================================
echo.

REM Проверка Python
echo ^<img=1F50D^> Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ^<img=274C^> Python не установлен. Пожалуйста, установите Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ^<img=2705^> Python %PYTHON_VERSION% найден
echo.

REM Создание виртуального окружения
echo ^<img=1F4E6^> Создание виртуального окружения...
if not exist "venv" (
    python -m venv venv
    echo ^<img=2705^> Виртуальное окружение создано
) else (
    echo ^<img=2705^> Виртуальное окружение уже существует
)
echo.

REM Активация виртуального окружения
echo ^<img=1F680^> Активация виртуального окружения...
call venv\Scripts\activate.bat
echo ^<img=2705^> Виртуальное окружение активировано
echo.

REM Установка зависимостей
echo ^<img=1F4E5^> Установка зависимостей...
python -m pip install --upgrade pip setuptools wheel > nul 2>&1
pip install -r requirements.txt > nul 2>&1
echo ^<img=2705^> Зависимости установлены
echo.

REM Запуск приложения
echo ^<img=1F389^> Запуск приложения...
echo ===================================================
echo.
echo Приложение откроется в браузере по адресу:
echo ^<img=1F449^> http://localhost:8501
echo.
echo Для остановки приложения нажмите Ctrl+C
echo.
echo ===================================================
echo.

streamlit run app.py

pause
