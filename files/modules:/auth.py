"""
Модуль аутентификации пользователей
Поддерживает три роли: врач, фармацевт, пациент
"""

import hashlib
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta

# ============================================================================
# ДЕМО АККАУНТЫ
# ============================================================================

DEMO_USERS = {
    # ВРАЧИ
    "doctor1": {
        "password": "doctor123",
        "name": "Петр Иванович Петров",
        "role": "doctor",
        "specialization": "Кардиолог",
        "clinic": "МЦ 'Здоровье'",
        "license": "ЛР-001234",
        "patients_count": 45,
    },
    "doctor2": {
        "password": "doctor123",
        "name": "Иван Сергеевич Волков",
        "role": "doctor",
        "specialization": "Терапевт",
        "clinic": "МЦ 'Здоровье'",
        "license": "ЛР-005678",
        "patients_count": 52,
    },
    "doctor3": {
        "password": "doctor123",
        "name": "Мария Александровна Сидорова",
        "role": "doctor",
        "specialization": "Невролог",
        "clinic": "МЦ 'Здоровье'",
        "license": "ЛР-009012",
        "patients_count": 38,
    },
    
    # ФАРМАЦЕВТЫ
    "pharmacist1": {
        "password": "pharma123",
        "name": "Елена Викторовна Кузнецова",
        "role": "pharmacist",
        "pharmacy": "Аптека №1 'Здоровье'",
        "license": "АЛ-001234",
        "experience_years": 8,
    },
    "pharmacist2": {
        "password": "pharma123",
        "name": "Олег Николаевич Смирнов",
        "role": "pharmacist",
        "pharmacy": "Аптека №1 'Здоровье'",
        "license": "АЛ-005678",
        "experience_years": 12,
    },
    
    # ПАЦИЕНТЫ
    "patient1": {
        "password": "patient123",
        "name": "Иван Иванович Иванов",
        "role": "patient",
        "patient_id": "PAT-2026-00001",
        "insurance": "Полис № 1234567890",
        "doctor": "Петров П.И.",
    },
    "patient2": {
        "password": "patient123",
        "name": "Анна Сергеевна Волкова",
        "role": "patient",
        "patient_id": "PAT-2026-00002",
        "insurance": "Полис № 9876543210",
        "doctor": "Волков И.С.",
    },
    
    # АДМИНИСТРАТОР
    "admin": {
        "password": "admin123",
        "name": "Администратор системы",
        "role": "admin",
        "access_level": "full",
    }
}

# ============================================================================
# ФУНКЦИИ АУТЕНТИФИКАЦИИ
# ============================================================================

def hash_password(password: str) -> str:
    """Хеширует пароль (для демонстрации)"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
    """
    Аутентифицирует пользователя
    
    Returns:
        (успех, данные пользователя, сообщение об ошибке)
    """
    
    if not username or not password:
        return False, None, "Пожалуйста, введите имя пользователя и пароль"
    
    if username not in DEMO_USERS:
        return False, None, f"Пользователь '{username}' не найден"
    
    user = DEMO_USERS[username]
    
    if user["password"] != password:
        return False, None, "Неверный пароль"
    
    # Успешная аутентификация
    user_data = {
        "username": username,
        "name": user["name"],
        "role": user["role"],
        "login_time": datetime.now(),
        "session_timeout": datetime.now() + timedelta(hours=8),
    }
    
    # Добавляем специфичные для роли данные
    if user["role"] == "doctor":
        user_data.update({
            "specialization": user.get("specialization"),
            "clinic": user.get("clinic"),
            "license": user.get("license"),
            "patients_count": user.get("patients_count"),
        })
    elif user["role"] == "pharmacist":
        user_data.update({
            "pharmacy": user.get("pharmacy"),
            "license": user.get("license"),
            "experience_years": user.get("experience_years"),
        })
    elif user["role"] == "patient":
        user_data.update({
            "patient_id": user.get("patient_id"),
            "insurance": user.get("insurance"),
            "doctor": user.get("doctor"),
        })
    
    return True, user_data, None

def validate_session(user_data: Dict) -> Tuple[bool, Optional[str]]:
    """Проверяет валидность сессии"""
    
    if not user_data:
        return False, "Сессия не существует"
    
    if datetime.now() > user_data["session_timeout"]:
        return False, "Сессия истекла, требуется повторная аутентификация"
    
    return True, None

def get_demo_credentials() -> Dict[str, list]:
    """Возвращает учетные данные для демо"""
    
    credentials = {
        "doctor": [],
        "pharmacist": [],
        "patient": [],
        "admin": []
    }
    
    for username, user in DEMO_USERS.items():
        role = user["role"]
        credentials[role].append({
            "username": username,
            "name": user["name"],
            "password": user["password"]
        })
    
    return credentials

# ============================================================================
# ИНФОРМАЦИОННЫЕ ФУНКЦИИ
# ============================================================================

def get_role_description(role: str) -> str:
    """Возвращает описание роли"""
    
    descriptions = {
        "doctor": "Врач - выписывает рецепты, проводит анализ лекарственных взаимодействий",
        "pharmacist": "Фармацевт - проверяет рецепты, отпускает лекарства, контролирует безопасность",
        "patient": "Пациент - просматривает свои рецепты, историю лечения, получает рекомендации",
        "admin": "Администратор - управляет системой, аналитика, отчеты"
    }
    
    return descriptions.get(role, "Неизвестная роль")

def get_role_icon(role: str) -> str:
    """Возвращает иконку для роли"""
    
    icons = {
        "doctor": "👨‍⚕️",
        "pharmacist": "💊",
        "patient": "🧑‍⚕️",
        "admin": "⚙️"
    }
    
    return icons.get(role, "👤")

def get_role_color(role: str) -> str:
    """Возвращает цвет для роли"""
    
    colors = {
        "doctor": "#3B82F6",      # Синий
        "pharmacist": "#4FD1C5",   # Голубой
        "patient": "#22C55E",      # Зеленый
        "admin": "#8B5CF6"         # Фиолетовый
    }
    
    return colors.get(role, "#6B7280")
