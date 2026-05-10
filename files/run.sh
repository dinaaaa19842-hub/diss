#!/bin/bash

# MediScript Pro - Быстрый запуск приложения
# Скрипт для Linux/macOS

set -e

echo "═══════════════════════════════════════════════════"
echo "💊 MediScript Pro - Система управления лекарствами"
echo "═══════════════════════════════════════════════════"
echo ""

# Проверка Python
echo "🔍 Проверка Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не установлен. Пожалуйста, установите Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION найден"
echo ""

# Создание виртуального окружения
echo "📦 Создание виртуального окружения..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "✅ Виртуальное окружение уже существует"
fi
echo ""

# Активация виртуального окружения
echo "🚀 Активация виртуального окружения..."
source venv/bin/activate
echo "✅ Виртуальное окружение активировано"
echo ""

# Установка зависимостей
echo "📥 Установка зависимостей..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Зависимости установлены"
echo ""

# Запуск приложения
echo "🎉 Запуск приложения..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Приложение откроется в браузере по адресу:"
echo "👉 http://localhost:8501"
echo ""
echo "Для остановки приложения нажмите Ctrl+C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

streamlit run app.py
