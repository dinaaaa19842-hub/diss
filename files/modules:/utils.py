"""
Модуль утилит для создания UI компонентов и управления стилями
"""

import streamlit as st
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd

# ============================================================================
# ЦВЕТОВАЯ ПАЛИТРА
# ============================================================================

COLORS = {
    # Основные цвета
    "primary": "#3B82F6",           # Медицинский синий
    "accent": "#4FD1C5",            # Неоновый голубой
    "secondary": "#8B5CF6",         # Фиолетовый
    
    # Фоны
    "bg_light": "#F7FAFC",          # Светлый фон
    "bg_lighter": "#F0F4F8",        # Еще светлее
    "bg_white": "#FFFFFF",          # Белый
    "bg_dark": "#1F2937",           # Темный
    
    # Статусы
    "success": "#22C55E",           # Зелёный
    "warning": "#F59E0B",           # Жёлтый/Оранжевый
    "error": "#EF4444",             # Красный
    "info": "#06B6D4",              # Голубой
    
    # Текст
    "text_dark": "#1F2937",         # Темный текст
    "text_medium": "#6B7280",       # Средний текст
    "text_light": "#9CA3AF",        # Светлый текст
    
    # Границы
    "border": "#E5E7EB",            # Граница
    "border_dark": "#D1D5DB",       # Темная граница
}

# ============================================================================
# КАСТОМНЫЕ CSS СТИЛИ
# ============================================================================

def get_custom_css() -> str:
    """Возвращает кастомные CSS стили"""
    
    return f"""
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        /* Основные стили */
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: {COLORS['bg_light']};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        }}
        
        /* Контейнер приложения */
        [data-testid="stMainBlockContainer"] {{
            padding: 2.5rem 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        /* Заголовки */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS['text_dark']};
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 1rem;
        }}
        
        h1 {{
            font-size: 2.5rem;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        h2 {{
            font-size: 2rem;
            color: {COLORS['primary']};
        }}
        
        h3 {{
            font-size: 1.5rem;
        }}
        
        /* Метрика карточки */
        .metric-card {{
            background: {COLORS['bg_white']};
            border-radius: 16px;
            padding: 1.75rem;
            border-left: 5px solid {COLORS['primary']};
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1rem;
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.12);
            border-left-color: {COLORS['accent']};
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {COLORS['primary']};
            margin-bottom: 0.5rem;
            line-height: 1;
        }}
        
        .metric-label {{
            font-size: 0.95rem;
            color: {COLORS['text_medium']};
            font-weight: 500;
        }}
        
        /* Карточки */
        .card {{
            background: {COLORS['bg_white']};
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            margin-bottom: 2rem;
            border: 1px solid {COLORS['border']};
            transition: all 0.3s ease;
        }}
        
        .card:hover {{
            box-shadow: 0 12px 24px rgba(0,0,0,0.1);
            border-color: {COLORS['accent']};
        }}
        
        /* Бейджи статуса */
        .status-badge {{
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            margin: 0.25rem;
            white-space: nowrap;
        }}
        
        .status-low {{
            background-color: #D1FAE5;
            color: #065F46;
        }}
        
        .status-medium {{
            background-color: #FEF3C7;
            color: #92400E;
        }}
        
        .status-high {{
            background-color: #FECACA;
            color: #7C2D12;
        }}
        
        .status-critical {{
            background-color: #FEE2E2;
            color: #991B1B;
        }}
        
        /* Блоки предупреждений */
        .alert-box {{
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 5px solid;
        }}
        
        .alert-success {{
            background-color: #D1FAE5;
            border-left-color: {COLORS['success']};
            color: #065F46;
        }}
        
        .alert-warning {{
            background-color: #FEF3C7;
            border-left-color: {COLORS['warning']};
            color: #92400E;
        }}
        
        .alert-error {{
            background-color: #FEE2E2;
            border-left-color: {COLORS['error']};
            color: #991B1B;
        }}
        
        .alert-info {{
            background-color: #DBEAFE;
            border-left-color: {COLORS['info']};
            color: #1E40AF;
        }}
        
        .alert-title {{
            font-weight: 700;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }}
        
        /* Кнопки */
        .btn {{
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 1rem;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
            color: white;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
        }}
        
        /* Таблицы */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0;
        }}
        
        th {{
            background-color: {COLORS['bg_lighter']};
            color: {COLORS['text_dark']};
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid {COLORS['primary']};
            font-size: 0.95rem;
        }}
        
        td {{
            padding: 1rem;
            border-bottom: 1px solid {COLORS['border']};
            font-size: 0.95rem;
        }}
        
        tr:hover {{
            background-color: rgba(79, 209, 197, 0.05);
        }}
        
        /* Разделитель */
        .divider {{
            height: 1px;
            background: {COLORS['border']};
            margin: 2rem 0;
        }}
        
        /* Компоненты ролей */
        .role-card {{
            background: {COLORS['bg_white']};
            border: 2px solid {COLORS['border']};
            border-radius: 16px;
            padding: 2.5rem;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 1rem 0;
        }}
        
        .role-card:hover {{
            border-color: {COLORS['accent']};
            background: linear-gradient(135deg, rgba(79,209,197,0.05) 0%, rgba(59,130,246,0.05) 100%);
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        }}
        
        .role-icon {{
            font-size: 4rem;
            margin-bottom: 1rem;
        }}
        
        .role-title {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {COLORS['text_dark']};
            margin-bottom: 0.5rem;
        }}
        
        .role-description {{
            font-size: 0.95rem;
            color: {COLORS['text_medium']};
            line-height: 1.5;
        }}
        
        /* Иконки статуса */
        .risk-icon {{
            display: inline-block;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 0.5rem;
        }}
        
        .risk-low {{
            background-color: #D1FAE5;
            color: #065F46;
        }}
        
        .risk-medium {{
            background-color: #FEF3C7;
            color: #92400E;
        }}
        
        .risk-high {{
            background-color: #FECACA;
            color: #7C2D12;
        }}
        
        .risk-critical {{
            background-color: #FEE2E2;
            color: #991B1B;
        }}
    </style>
    """

# ============================================================================
# КОМПОНЕНТЫ ИНТЕРФЕЙСА
# ============================================================================

def render_metric_card(label: str, value: str, icon: str = "", 
                       color: str = "primary", sublabel: str = ""):
    """Отображает карточку метрики"""
    
    color_hex = COLORS.get(color, color)
    html = f"""
    <div class="metric-card" style="border-left-color: {color_hex};">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
        <div class="metric-value" style="color: {color_hex};">{value}</div>
        <div class="metric-label">{label}</div>
    """
    
    if sublabel:
        html += f'<div style="font-size: 0.85rem; color: {COLORS["text_light"]}; margin-top: 0.5rem;">{sublabel}</div>'
    
    html += "</div>"
    
    st.markdown(html, unsafe_allow_html=True)

def render_alert(title: str, message: str, alert_type: str = "info", icon: str = "ℹ️"):
    """Отображает блок предупреждения"""
    
    alert_map = {
        "success": ("alert-success", "✅"),
        "warning": ("alert-warning", "⚠️"),
        "error": ("alert-error", "🚨"),
        "info": ("alert-info", "ℹ️"),
    }
    
    css_class, default_icon = alert_map.get(alert_type, ("alert-info", "ℹ️"))
    icon = icon or default_icon
    
    html = f"""
    <div class="{css_class}">
        <div class="alert-title">{icon} {title}</div>
        <div>{message}</div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def render_status_badge(status: str) -> str:
    """Возвращает HTML для статус-бейджа"""
    
    status_map = {
        "low": ("✓ НИЗКИЙ РИСК", "status-low"),
        "medium": ("⚠ СРЕДНИЙ РИСК", "status-medium"),
        "high": ("🔴 ВЫСОКИЙ РИСК", "status-high"),
        "critical": ("🚨 КРИТИЧЕСКИЙ", "status-critical"),
        "none": ("✓ ОК", "status-low"),
    }
    
    text, css_class = status_map.get(status.lower(), ("UNKNOWN", "status-medium"))
    return f'<span class="status-badge {css_class}">{text}</span>'

def render_risk_indicator(risk_level: str, value: Optional[float] = None) -> str:
    """Отображает индикатор риска"""
    
    risk_map = {
        "low": ("risk-low", "🟢", "Низкий риск"),
        "medium": ("risk-medium", "🟡", "Средний риск"),
        "high": ("risk-high", "🟠", "Высокий риск"),
        "critical": ("risk-critical", "🔴", "Критический риск"),
    }
    
    css_class, emoji, label = risk_map.get(risk_level.lower(), ("risk-low", "❓", "Неизвестно"))
    
    html = f'<span class="risk-icon {css_class}">{emoji}</span><strong>{label}</strong>'
    
    if value is not None:
        html += f' <span style="color: {COLORS["text_light"]};">({value})</span>'
    
    return html

def render_medication_table(medications: List[Dict], show_actions: bool = False) -> None:
    """Отображает таблицу препаратов"""
    
    if not medications:
        st.info("Препаратов не назначено")
        return
    
    df_data = []
    for i, med in enumerate(medications):
        df_data.append({
            "№": i + 1,
            "Препарат": med.get("name", ""),
            "Группа": med.get("group", ""),
            "Дозировка": med.get("dosage", ""),
            "Частота": med.get("frequency", ""),
            "Длительность": med.get("duration", ""),
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

def render_interaction_card(drug1: str, drug2: str, severity: str, 
                           description: str, recommendation: str) -> None:
    """Отображает карточку взаимодействия"""
    
    severity_config = {
        "critical": ("🚨", "#FEE2E2", "#991B1B"),
        "high": ("⚠️", "#FECACA", "#7C2D12"),
        "medium": ("⚠️", "#FEF3C7", "#92400E"),
    }
    
    emoji, bg_color, text_color = severity_config.get(severity, ("ℹ️", "#DBEAFE", "#1E40AF"))
    
    html = f"""
    <div class="alert-box" style="background-color: {bg_color}; border-left-color: {text_color}; color: {text_color};">
        <div class="alert-title">{emoji} {drug1} + {drug2}</div>
        <div style="margin-bottom: 0.5rem;"><strong>Механизм:</strong> {description}</div>
        <div><strong>Рекомендация:</strong> {recommendation}</div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def render_header_with_subtitle(title: str, subtitle: str = "", icon: str = "") -> None:
    """Отображает заголовок с подзаголовком"""
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">
            {icon}
        </div>
        <h1 style="margin: 0 0 0.5rem 0;">
            {title}
        </h1>
        <div style="font-size: 1.1rem; color: {COLORS['text_medium']}; margin: 0;">
            {subtitle}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# УТИЛИТЫ
# ============================================================================

def format_date(date_obj) -> str:
    """Форматирует дату"""
    if hasattr(date_obj, 'strftime'):
        return date_obj.strftime("%d.%m.%Y")
    return str(date_obj)

def format_time(time_obj) -> str:
    """Форматирует время"""
    if hasattr(time_obj, 'strftime'):
        return time_obj.strftime("%H:%M")
    return str(time_obj)

def get_age_from_dob(date_of_birth: str) -> int:
    """Рассчитывает возраст из даты рождения"""
    try:
        from datetime import datetime
        dob = datetime.strptime(date_of_birth, "%d.%m.%Y")
        today = datetime.now()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except:
        return 0

def truncate_text(text: str, max_length: int = 50) -> str:
    """Обрезает текст до максимальной длины"""
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text
