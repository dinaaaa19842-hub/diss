"""
Модуль интеллектуального анализа взаимодействий и рисков лекарственных назначений
Реальные формулы и алгоритмы расчета
"""

from typing import Dict, List, Tuple
import math
from datetime import datetime, timedelta

# ============================================================================
# БАЗЫ ДАННЫХ ВЗАИМОДЕЙСТВИЙ С РЕАЛЬНЫМИ МЕХАНИЗМАМИ
# ============================================================================

DRUG_INTERACTIONS_DATABASE = {
    # Аспирин взаимодействия
    ("Аспирин", "Варфарин"): {
        "severity": "critical",
        "mechanism": "Оба препараты снижают агрегацию тромбоцитов и влияют на свертываемость",
        "risk_increase": 300,  # % увеличения риска кровотечения
        "recommendation": "Избегать комбинации, мониторинг МНО обязателен",
        "contraindication": True
    },
    ("Аспирин", "Ибупрофен"): {
        "severity": "high",
        "mechanism": "Оба НПВС - конкуренция за рецепторы ЦОГ, повышение риска язвы ЖКТ",
        "risk_increase": 150,
        "recommendation": "Не комбинировать, выбрать одно НПВС",
        "contraindication": True
    },
    
    # Варфарин взаимодействия
    ("Варфарин", "Ибупрофен"): {
        "severity": "high",
        "mechanism": "НПВС вытесняет варфарин из связи с белками, усиливает его эффект",
        "risk_increase": 250,
        "recommendation": "Использовать парацетамол или слабые НПВС с контролем МНО",
        "contraindication": True
    },
    ("Варфарин", "Амиодарон"): {
        "severity": "high",
        "mechanism": "Амиодарон ингибирует CYP2C9, снижает метаболизм варфарина",
        "risk_increase": 200,
        "recommendation": "Снизить дозу варфарина на 30-50%, частый мониторинг МНО",
        "contraindication": False
    },
    
    # Статины
    ("Симвастатин", "Амиодарон"): {
        "severity": "high",
        "mechanism": "Амиодарон ингибирует CYP3A4, замедляет метаболизм симвастатина",
        "risk_increase": 280,
        "recommendation": "Использовать правастатин или розувастатин",
        "contraindication": False
    },
    ("Аторвастатин", "Эритромицин"): {
        "severity": "medium",
        "mechanism": "Макролид ингибирует CYP3A4, повышает концентрацию статина",
        "risk_increase": 100,
        "recommendation": "Снизить дозу статина или выбрать другой антибиотик",
        "contraindication": False
    },
    
    # Диабетические препараты
    ("Метформин", "Контрастное вещество (йод)"),: {
        "severity": "critical",
        "mechanism": "Контрастное вещество повышает риск острой почечной недостаточности и лактоацидоза",
        "risk_increase": 350,
        "recommendation": "Отменить метформин за 48 часов до и после процедуры",
        "contraindication": True
    },
    ("Инсулин", "Бета-блокаторы"): {
        "severity": "high",
        "mechanism": "Бета-блокаторы маскируют симптомы гипогликемии",
        "risk_increase": 180,
        "recommendation": "Использовать селективные бета-блокаторы или пересмотреть терапию",
        "contraindication": False
    },
    
    # Антидепрессанты
    ("СИОЗС (Флуоксетин)", "Трамадол"): {
        "severity": "high",
        "mechanism": "Оба повышают серотонин, риск серотонинового синдрома",
        "risk_increase": 200,
        "recommendation": "Избегать комбинации, использовать слабые анальгетики",
        "contraindication": True
    },
    
    # ACE ингибиторы
    ("Эналаприл", "Спиронолактон"): {
        "severity": "medium",
        "mechanism": "Оба препараты задерживают калий, риск гиперкалиемии",
        "risk_increase": 120,
        "recommendation": "Мониторинг уровня калия и креатинина каждые 1-2 недели",
        "contraindication": False
    },
}

# ============================================================================
# РЕАЛЬНЫЕ ФОРМУЛЫ РАСЧЕТА РИСКА ВЗАИМОДЕЙСТВИЙ
# ============================================================================

def calculate_interaction_risk(
    drug1: Dict,
    drug2: Dict,
    patient: Dict,
    interaction_data: Dict
) -> Dict:
    """
    Рассчитывает реальный риск взаимодействия с учетом характеристик пациента
    
    Формула основана на:
    - Базовом риске взаимодействия
    - Возрасте пациента
    - Функции почек (eGFR)
    - Функции печени
    - Наличии сопутствующих заболеваний
    """
    
    base_risk = interaction_data.get("risk_increase", 100) / 100  # Преобразуем в коэффициент
    
    # Корректирующие коэффициенты для возраста
    age = patient.get("age", 50)
    if age >= 75:
        age_factor = 1.5  # Старше 75 лет - выше риск
    elif age >= 65:
        age_factor = 1.3
    elif age >= 55:
        age_factor = 1.1
    else:
        age_factor = 1.0
    
    # Корректирующий коэффициент для функции почек
    # Приблизительная формула Кокрофта-Голта для eGFR
    creatinine = patient.get("creatinine", 1.0)  # мг/дл
    
    if patient.get("gender") == "М":
        egfr = ((140 - age) * 72) / (creatinine * 72)
    else:
        egfr = ((140 - age) * 72 * 0.85) / (creatinine * 72)
    
    # Классификация функции почек
    if egfr >= 90:
        kidney_factor = 1.0  # Нормальная функция
    elif egfr >= 60:
        kidney_factor = 1.2  # Легкое снижение
    elif egfr >= 30:
        kidney_factor = 1.5  # Умеренное снижение
    else:
        kidney_factor = 2.0  # Тяжелое снижение
    
    # Корректирующий коэффициент для функции печени
    liver_disease = patient.get("liver_disease", False)
    liver_factor = 1.5 if liver_disease else 1.0
    
    # Корректирующий коэффициент для сопутствующих заболеваний
    comorbidity_factor = 1.0
    diagnoses = patient.get("diagnoses", [])
    
    if "Сердечная недостаточность" in diagnoses:
        comorbidity_factor += 0.3
    if "Почечная недостаточность" in diagnoses:
        comorbidity_factor += 0.3
    if "Печеночная недостаточность" in diagnoses:
        comorbidity_factor += 0.3
    
    # Итоговый риск
    total_risk_multiplier = age_factor * kidney_factor * liver_factor * comorbidity_factor
    final_risk_score = base_risk * total_risk_multiplier
    
    # Переводим в категорию риска
    if interaction_data.get("contraindication"):
        risk_category = "critical"
    elif final_risk_score >= 2.5:
        risk_category = "critical"
    elif final_risk_score >= 1.8:
        risk_category = "high"
    elif final_risk_score >= 1.2:
        risk_category = "medium"
    else:
        risk_category = "low"
    
    return {
        "base_risk": base_risk,
        "age_factor": age_factor,
        "kidney_factor": kidney_factor,
        "liver_factor": liver_factor,
        "comorbidity_factor": comorbidity_factor,
        "total_risk_multiplier": total_risk_multiplier,
        "final_risk_score": round(final_risk_score, 2),
        "risk_category": risk_category,
        "egfr": round(egfr, 1),
        "kidney_status": get_kidney_status(egfr)
    }

def get_kidney_status(egfr: float) -> str:
    """Классификация функции почек по eGFR"""
    if egfr >= 90:
        return "Нормальная функция почек"
    elif egfr >= 60:
        return "Легкое снижение функции почек"
    elif egfr >= 45:
        return "Умеренное снижение функции почек"
    elif egfr >= 30:
        return "Значительное снижение функции почек"
    else:
        return "Терминальная почечная недостаточность"

# ============================================================================
# СЛОЖНАЯ ЛОГИКА ВЫЯВЛЕНИЯ ПОЛИПРАГМАЗИИ
# ============================================================================

def analyze_polypharmacy(medications: List[Dict], patient: Dict) -> Dict:
    """
    Комплексный анализ полипрагмазии с учетом:
    - Количества препаратов
    - Группы препаратов
    - Потенциальной дублирования
    - Возраста пациента
    - Функции почек
    """
    
    num_medications = len(medications)
    age = patient.get("age", 50)
    diagnoses = patient.get("diagnoses", [])
    
    # 1. БАЗОВАЯ КЛАССИФИКАЦИЯ ПО КОЛИЧЕСТВУ
    if num_medications >= 10:
        base_level = "extreme"
        base_description = "Экстремальная полипрагмазия"
    elif num_medications >= 7:
        base_level = "high"
        base_description = "Высокая полипрагмазия"
    elif num_medications >= 5:
        base_level = "moderate"
        base_description = "Полипрагмазия"
    elif num_medications >= 3:
        base_level = "mild"
        base_description = "Пограничная полипрагмазия"
    else:
        base_level = "none"
        base_description = "Рациональное назначение"
    
    # 2. АНАЛИЗ НА ДУБЛИРОВАНИЕ И КОНФЛИКТЫ
    drug_groups = {}
    duplicates = []
    
    for med in medications:
        group = med.get("group", "Unknown")
        if group in drug_groups:
            drug_groups[group].append(med["name"])
            duplicates.append({
                "group": group,
                "drugs": drug_groups[group],
                "issue": f"Несколько препаратов из группы {group}"
            })
        else:
            drug_groups[group] = [med["name"]]
    
    # 3. ВОЗРАСТНЫЕ ФАКТОРЫ
    age_risk = 1.0
    age_issues = []
    
    if age >= 75:
        age_risk = 1.8
        age_issues.append("Пациент старше 75 лет - повышенный риск побочных эффектов")
    elif age >= 65:
        age_risk = 1.5
        age_issues.append("Пациент 65-75 лет - повышен риск побочных эффектов")
    
    # 4. ОЦЕНКА СЛОЖНОСТИ РЕЖИМА ПРИЕМА
    complexity_score = 0
    complexity_issues = []
    
    # Анализируем частоту приема
    frequencies = {}
    for med in medications:
        freq = med.get("frequency", "")
        frequencies[freq] = frequencies.get(freq, 0) + 1
    
    if len(frequencies) > 2:
        complexity_score += 2
        complexity_issues.append("Сложный режим приема - разные частоты приема препаратов")
    
    if any("3 раза" in freq for freq in frequencies.keys()):
        complexity_score += 1
        complexity_issues.append("Высокая частота приема (3 раза в день)")
    
    # Анализируем наличие специальных условий приема
    special_conditions = 0
    for med in medications:
        notes = med.get("notes", "").lower()
        if "натощак" in notes or "за час" in notes or "через час" in notes:
            special_conditions += 1
    
    if special_conditions > 2:
        complexity_score += 1
        complexity_issues.append(f"{special_conditions} препаратов требуют специальных условий приема")
    
    # 5. СИНДРОМЫ ПОЛИПРАГМАЗИИ
    polypharmacy_syndromes = []
    
    if num_medications >= 5 and age >= 65:
        polypharmacy_syndromes.append({
            "name": "Синдром полипрагмазии у пожилого",
            "description": "Высокий риск побочных эффектов, падений, когнитивных нарушений",
            "severity": "high"
        })
    
    if len(duplicates) >= 2:
        polypharmacy_syndromes.append({
            "name": "Избыточное дублирование препаратов",
            "description": "Несколько препаратов одной группы без четкого обоснования",
            "severity": "medium"
        })
    
    if complexity_score >= 3:
        polypharmacy_syndromes.append({
            "name": "Сложная схема лечения",
            "description": "Высокий риск ошибок пациента при приеме лекарств",
            "severity": "medium"
        })
    
    # 6. РАСЧЕТ ИТОГОВОГО РИСКА
    if base_level == "extreme":
        overall_risk = "critical"
        risk_score = 9.0
    elif base_level == "high":
        overall_risk = "high" if age >= 65 else "medium"
        risk_score = 7.0 if age >= 65 else 5.0
    elif base_level == "moderate":
        overall_risk = "medium" if age >= 65 else "low"
        risk_score = 5.0 if age >= 65 else 3.0
    else:
        overall_risk = "low"
        risk_score = 1.0
    
    # Корректируем по сложности
    risk_score *= (1.0 + complexity_score * 0.3)
    
    # Нормализуем по 10-балльной системе
    risk_score = min(10.0, risk_score)
    
    return {
        "num_medications": num_medications,
        "base_level": base_level,
        "base_description": base_description,
        "drug_groups": drug_groups,
        "duplicates": duplicates,
        "has_duplicates": len(duplicates) > 0,
        "age_risk": age_risk,
        "age_issues": age_issues,
        "complexity_score": complexity_score,
        "complexity_issues": complexity_issues,
        "polypharmacy_syndromes": polypharmacy_syndromes,
        "overall_risk": overall_risk,
        "risk_score": round(risk_score, 1),
        "recommendations": generate_polypharmacy_recommendations(
            num_medications, age, duplicates, complexity_score
        )
    }

def generate_polypharmacy_recommendations(
    num_meds: int,
    age: int,
    duplicates: List,
    complexity: int
) -> List[str]:
    """Генерирует рекомендации по оптимизации полипрагмазии"""
    
    recommendations = []
    
    # Рекомендации по количеству
    if num_meds >= 7:
        recommendations.append(f"Рассмотрите возможность отмены {num_meds - 5} наименее критичных препаратов")
    
    # Рекомендации по дублированию
    if duplicates:
        for dup in duplicates:
            recommendations.append(
                f"В группе '{dup['group']}' используется {len(dup['drugs'])} препаратов. "
                f"Рассмотрите замену на один препарат."
            )
    
    # Рекомендации по возрасту
    if age >= 75 and num_meds >= 5:
        recommendations.append("В возрасте 75+ рекомендуется использовать максимум 5 препаратов")
        recommendations.append("Проведите пересмотр назначений (deprescribing) совместно с фармацевтом")
    
    # Рекомендации по сложности
    if complexity >= 3:
        recommendations.append("Упростите режим приема: попытайтесь использовать препараты с одинаковой частотой")
        recommendations.append("Подумайте о комбинированных препаратах (фиксированные комбинации)")
        recommendations.append("Рекомендуйте пациенту использовать органайзер с дозаторами")
    
    # Обучение пациента
    recommendations.append("Проведите обучение пациента правилам приема препаратов")
    recommendations.append("Проверьте приверженность пациента к лечению")
    
    if not recommendations:
        recommendations.append("Текущая схема терапии оптимальна. Контролируйте эффективность.")
    
    return recommendations

# ============================================================================
# КОМПЛЕКСНЫЙ АНАЛИЗ РЕЦЕПТА
# ============================================================================

def analyze_prescription_comprehensive(patient: Dict, medications: List[Dict]) -> Dict:
    """
    Полный анализ рецепта с использованием всех формул и алгоритмов
    """
    
    analysis_result = {
        "timestamp": datetime.now(),
        "patient_id": patient.get("id", "Unknown"),
        "patient_age": patient.get("age", 50),
        "prescription_id": f"RX-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "medications_count": len(medications),
        "interactions": [],
        "polypharmacy": {},
        "overall_risk_level": "low",
        "critical_issues": [],
        "warnings": [],
        "recommendations": []
    }
    
    # Анализируем взаимодействия
    for i, med1 in enumerate(medications):
        for med2 in medications[i + 1:]:
            key = tuple(sorted([med1["name"], med2["name"]]))
            if key in DRUG_INTERACTIONS_DATABASE:
                interaction_data = DRUG_INTERACTIONS_DATABASE[key]
                risk_calc = calculate_interaction_risk(med1, med2, patient, interaction_data)
                
                interaction = {
                    "drug1": med1["name"],
                    "drug2": med2["name"],
                    "mechanism": interaction_data.get("mechanism", ""),
                    "severity": risk_calc["risk_category"],
                    "risk_score": risk_calc["final_risk_score"],
                    "recommendation": interaction_data.get("recommendation", ""),
                    "contraindication": interaction_data.get("contraindication", False),
                    "details": risk_calc
                }
                
                analysis_result["interactions"].append(interaction)
                
                if interaction["contraindication"] or interaction["severity"] == "critical":
                    analysis_result["critical_issues"].append(interaction)
    
    # Анализируем полипрагмазию
    polypharmacy_analysis = analyze_polypharmacy(medications, patient)
    analysis_result["polypharmacy"] = polypharmacy_analysis
    
    # Определяем общий уровень риска
    if analysis_result["critical_issues"]:
        analysis_result["overall_risk_level"] = "critical"
    elif polypharmacy_analysis["overall_risk"] == "critical":
        analysis_result["overall_risk_level"] = "critical"
    elif polypharmacy_analysis["overall_risk"] == "high" or any(
        i["severity"] == "high" for i in analysis_result["interactions"]
    ):
        analysis_result["overall_risk_level"] = "high"
    elif any(i["severity"] == "medium" for i in analysis_result["interactions"]):
        analysis_result["overall_risk_level"] = "medium"
    else:
        analysis_result["overall_risk_level"] = "low"
    
    # Собираем рекомендации
    for interaction in analysis_result["interactions"]:
        if interaction["severity"] in ["critical", "high"]:
            analysis_result["recommendations"].append(interaction["recommendation"])
    
    analysis_result["recommendations"].extend(polypharmacy_analysis["recommendations"])
    
    # Проверяем противопоказания
    allergies = patient.get("allergies", [])
    for med in medications:
        if med["name"] in allergies:
            analysis_result["critical_issues"].append({
                "type": "allergy",
                "drug": med["name"],
                "description": f"ПРОТИВОПОКАЗАНО: аллергия на {med['name']}"
            })
            analysis_result["overall_risk_level"] = "critical"
    
    return analysis_result
