"""
Модуль генерации и управления базой данных пациентов
50+ примеров пациентов с полной информацией
"""

import random
from typing import List, Dict
from datetime import datetime, timedelta

# ============================================================================
# СПРАВОЧНЫЕ ДАННЫЕ
# ============================================================================

FIRST_NAMES = {
    "М": ["Иван", "Петр", "Сергей", "Александр", "Виктор", "Дмитрий", "Павел", 
          "Андрей", "Владимир", "Николай", "Михаил", "Анатолий", "Валерий", "Аркадий"],
    "Ж": ["Анна", "Мария", "Елена", "Ольга", "Юлия", "Наталья", "Татьяна", 
          "Галина", "Валентина", "Светлана", "Людмила", "Нина", "Раиса", "Вера"]
}

LAST_NAMES = [
    "Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Волков", "Морозов",
    "Орлов", "Павлов", "Федоров", "Степанов", "Александров", "Никитин", "Соколов",
    "Васильев", "Новиков", "Фомин", "Герасимов", "Лавров", "Панов", "Гавриков",
    "Козлов", "Лобанов", "Раков", "Леонов", "Климов", "Миронов", "Эмелин"
]

DIAGNOSES = [
    "Гипертоническая болезнь II стадии",
    "Ишемическая болезнь сердца, стенокардия напряжения",
    "Сахарный диабет 2 типа, компенсированный",
    "Фибрилляция предсердий, постоянная форма",
    "Гастроэзофагеальная рефлюксная болезнь",
    "Остеоартроз коленных суставов",
    "Остеопороз постменопаузальный",
    "Депрессивное расстройство",
    "Тромбоз глубоких вен в анамнезе",
    "Инфаркт миокарда в анамнезе (3 года назад)",
    "Хроническое обструктивное заболевание легких, легкой степени",
    "Нарушение сердечного ритма (экстрасистолия)",
    "Головные боли напряжения",
    "Гиперлипидемия",
    "Ожирение II степени",
    "Гиперурикемия, подагра",
    "Панкреатит хронический в ремиссии",
    "Синдром раздраженного кишечника",
    "Атеросклероз артерий нижних конечностей",
    "Аритмия сердца, мерцательная аритмия"
]

ALLERGIES = [
    None,  # Нет аллергии
    "Пенициллин",
    "Аспирин",
    "Сульфаниламиды",
    "Йод",
    "Аллергия на морепродукты",
    "Лактоза",
    "Глютен",
    "Цефалоспорины",
    "Анестетики местные"
]

# ЛЕКАРСТВА С ПОЛНОЙ ИНФОРМАЦИЕЙ
MEDICATIONS_CATALOG = [
    {
        "name": "Аспирин",
        "group": "НПВС/Антиагрегант",
        "indication": "Профилактика тромбоза, боль, воспаление",
        "active_substance": "Ацетилсалициловая кислота",
        "typical_dosage": "100 мг",
        "typical_frequency": "1 раз в день",
        "contraindications": ["Язва ЖКТ", "Кровотечение"],
        "notes": "Принимать во время еды"
    },
    {
        "name": "Метопролол",
        "group": "Бета-блокатор",
        "indication": "Артериальная гипертензия, аритмия",
        "active_substance": "Метопролола тартрат",
        "typical_dosage": "50-100 мг",
        "typical_frequency": "2 раза в день",
        "contraindications": ["Брадикардия", "Бронхиальная астма"],
        "notes": "Нельзя резко отменять"
    },
    {
        "name": "Амлодипин",
        "group": "Антагонист кальция",
        "indication": "Артериальная гипертензия, стенокардия",
        "active_substance": "Амлодипина безилат",
        "typical_dosage": "5-10 мг",
        "typical_frequency": "1 раз в день",
        "contraindications": ["Шок", "Критическое снижение давления"],
        "notes": "Прием в любое время суток"
    },
    {
        "name": "Эналаприл",
        "group": "АПФ ингибитор",
        "indication": "Артериальная гипертензия, сердечная недостаточность",
        "active_substance": "Эналаприла малеат",
        "typical_dosage": "10-20 мг",
        "typical_frequency": "2 раза в день",
        "contraindications": ["Ангионевротический отек", "Беременность"],
        "notes": "Контролировать уровень калия"
    },
    {
        "name": "Аторвастатин",
        "group": "Статин",
        "indication": "Гиперхолестеринемия, профилактика ИБС",
        "active_substance": "Аторвастатина кальция триатриватт",
        "typical_dosage": "10-40 мг",
        "typical_frequency": "1 раз в день",
        "contraindications": ["Активное заболевание печени", "Беременность"],
        "notes": "Принимать вечером, могут быть спазмы мышц"
    },
    {
        "name": "Омепразол",
        "group": "Ингибитор протонной помпы",
        "indication": "ГЭРБ, язва желудка, профилактика язв при НПВС",
        "active_substance": "Омепразола магния триатриватт",
        "typical_dosage": "20 мг",
        "typical_frequency": "1 раз в день",
        "contraindications": ["Непереносимость", "Дефицит витамина B12"],
        "notes": "Принимать за 30 мин до еды, натощак"
    },
    {
        "name": "Варфарин",
        "group": "Антикоагулянт",
        "indication": "Профилактика тромбоза, фибрилляция предсердий",
        "active_substance": "Варфарина натрия",
        "typical_dosage": "2.5-5 мг",
        "typical_frequency": "1 раз в день",
        "contraindications": ["Кровотечение", "Тяжелая почечная недостаточность"],
        "notes": "Требует регулярного контроля МНО"
    },
    {
        "name": "Амиодарон",
        "group": "Антиаритмик",
        "indication": "Нарушения ритма сердца",
        "active_substance": "Амиодарона гидрохлорид",
        "typical_dosage": "200-400 мг",
        "typical_frequency": "1-2 раза в день",
        "contraindications": ["Синус-брадикардия", "АВ блокада"],
        "notes": "Требует частого контроля ЭКГ"
    },
    {
        "name": "Метформин",
        "group": "Бигуанид",
        "indication": "Сахарный диабет 2 типа",
        "active_substance": "Метформина гидрохлорид",
        "typical_dosage": "500-1000 мг",
        "typical_frequency": "2-3 раза в день",
        "contraindications": ["Почечная недостаточность", "Печеночная недостаточность"],
        "notes": "Принимать во время или после еды"
    },
    {
        "name": "Парацетамол",
        "group": "Анальгетик",
        "indication": "Боль, лихорадка",
        "active_substance": "Парацетамол",
        "typical_dosage": "500-1000 мг",
        "typical_frequency": "3-4 раза в день",
        "contraindications": ["Тяжелые заболевания печени"],
        "notes": "Максимум 4000 мг в сутки"
    },
    {
        "name": "Ибупрофен",
        "group": "НПВС",
        "indication": "Боль, воспаление, лихорадка",
        "active_substance": "Ибупрофен",
        "typical_dosage": "200-400 мг",
        "typical_frequency": "3 раза в день",
        "contraindications": ["Язва ЖКТ", "Астма"],
        "notes": "Принимать во время еды"
    },
    {
        "name": "Фуросемид",
        "group": "Диуретик петлевой",
        "indication": "Отеки, артериальная гипертензия",
        "active_substance": "Фуросемид",
        "typical_dosage": "20-40 мг",
        "typical_frequency": "1-2 раза в день",
        "contraindications": ["Анурия", "Электролитные нарушения"],
        "notes": "Контролировать уровень электролитов"
    },
    {
        "name": "Спиронолактон",
        "group": "Диуретик калийсберегающий",
        "indication": "Артериальная гипертензия, отеки, сердечная недостаточность",
        "active_substance": "Спиронолактон",
        "typical_dosage": "25-50 мг",
        "typical_frequency": "1-2 раза в день",
        "contraindications": ["Гиперкалиемия", "Почечная недостаточность"],
        "notes": "Контролировать уровень калия"
    },
    {
        "name": "Глибенкламид",
        "group": "Сульфонилмочевина",
        "indication": "Сахарный диабет 2 типа",
        "active_substance": "Глибенкламид",
        "typical_dosage": "2.5-5 мг",
        "typical_frequency": "1-2 раза в день",
        "contraindications": ["Диабетический кетоацидоз", "Почечная недостаточность"],
        "notes": "Риск гипогликемии, прием перед едой"
    },
    {
        "name": "Симвастатин",
        "group": "Статин",
        "indication": "Гиперхолестеринемия",
        "active_substance": "Симвастатин",
        "typical_dosage": "10-40 мг",
        "typical_frequency": "1 раз в день",
        "contraindications": ["Активное заболевание печени"],
        "notes": "Сильный эффект взаимодействий, вечерний прием"
    },
    {
        "name": "Эритромицин",
        "group": "Макролидный антибиотик",
        "indication": "Бактериальные инфекции",
        "active_substance": "Эритромицин",
        "typical_dosage": "250-500 мг",
        "typical_frequency": "3-4 раза в день",
        "contraindications": ["Непереносимость", "Заболевания печени"],
        "notes": "Принимать за час до еды или спустя 2 часа после"
    },
    {
        "name": "Флуоксетин",
        "group": "СИОЗС (Антидепрессант)",
        "indication": "Депрессия, тревожные расстройства",
        "active_substance": "Флуоксетина гидрохлорид",
        "typical_dosage": "20 мг",
        "typical_frequency": "1 раз в день",
        "contraindications": ["Ингибиторы МАО", "Острая мания"],
        "notes": "Может потребоваться 2-4 недели для эффекта"
    },
]

# ============================================================================
# ФУНКЦИИ ГЕНЕРАЦИИ ДАННЫХ
# ============================================================================

def generate_patient_id() -> str:
    """Генерирует уникальный ID пациента"""
    return f"PAT-{datetime.now().year}-{random.randint(10000, 99999)}"

def generate_patients_database() -> List[Dict]:
    """Генерирует базу данных 50+ пациентов с полной информацией"""
    
    patients = []
    
    for i in range(55):
        # Случайные характеристики
        gender = random.choice(["М", "Ж"])
        age = random.randint(35, 85)
        
        # Выбираем случайные диагнозы (1-3)
        num_diagnoses = random.randint(1, 3)
        diagnoses = random.sample(DIAGNOSES, num_diagnoses)
        
        # На основе возраста и диагнозов выбираем препараты
        medications = select_medications_for_patient(age, diagnoses)
        
        # Выбираем аллергию (с вероятностью 30%)
        allergies = random.choice([None] + [a for a in ALLERGIES if a is not None] * 30) if random.random() < 0.3 else None
        
        # Симуляция показателей крови
        creatinine = random.uniform(0.7, 2.5) if random.random() < 0.1 else random.uniform(0.7, 1.2)
        
        patient = {
            "id": generate_patient_id(),
            "first_name": random.choice(FIRST_NAMES[gender]),
            "last_name": random.choice(LAST_NAMES),
            "gender": gender,
            "age": age,
            "date_of_birth": (datetime.now() - timedelta(days=age * 365)).strftime("%d.%m.%Y"),
            "diagnosis": diagnoses,
            "allergies": allergies,
            "medications": medications,
            "creatinine": round(creatinine, 2),  # мг/дл
            "liver_disease": random.random() < 0.05,  # 5% вероятность
            "kidney_disease": creatinine > 1.5,
            "created_at": datetime.now() - timedelta(days=random.randint(1, 365)),
            "last_visit": datetime.now() - timedelta(days=random.randint(1, 30)),
            "visit_history": generate_visit_history(10),
            "blood_pressure": f"{random.randint(110, 160)}/{random.randint(70, 100)}",
            "heart_rate": random.randint(60, 100),
            "notes": generate_patient_notes()
        }
        
        patients.append(patient)
    
    return patients

def select_medications_for_patient(age: int, diagnoses: List[str]) -> List[Dict]:
    """Выбирает подходящие препараты для пациента на основе возраста и диагнозов"""
    
    selected_medications = []
    
    # Логика выбора препаратов
    medication_mapping = {
        "Гипертоническая болезнь": ["Метопролол", "Амлодипин", "Эналаприл", "Фуросемид"],
        "Ишемическая болезнь": ["Аспирин", "Аторвастатин", "Метопролол"],
        "Сахарный диабет": ["Метформин", "Глибенкламид"],
        "Фибрилляция предсердий": ["Варфарин", "Амиодарон", "Метопролол"],
        "Гастроэзофагеальная рефлюксная": ["Омепразол"],
        "Остеоартроз": ["Ибупрофен", "Парацетамол"],
        "Депрессия": ["Флуоксетин"],
        "Тромбоз": ["Варфарин", "Аспирин"],
        "Инфаркт миокарда": ["Аспирин", "Метопролол", "Аторвастатин", "Эналаприл"],
    }
    
    # Собираем препараты по диагнозам
    for diagnosis in diagnoses:
        for key, meds in medication_mapping.items():
            if key in diagnosis:
                selected_medications.extend(meds)
    
    # Убираем дубликаты
    selected_medications = list(set(selected_medications))
    
    # Возрастная категория
    if age >= 75:
        # Добавляем витамины для пожилых
        if random.random() < 0.7:
            selected_medications.append("Парацетамол")  # Вместо активных НПВС
    elif age >= 65:
        if random.random() < 0.5:
            selected_medications.append("Спиронолактон")
    
    # Перемешиваем и ограничиваем количество
    random.shuffle(selected_medications)
    selected_medications = selected_medications[:6]  # Максимум 6 препаратов
    
    # Если нет препаратов, добавляем стандартный набор
    if not selected_medications:
        selected_medications = random.sample(["Парацетамол", "Аспирин", "Омепразол"], 1)
    
    # Конвертируем в полные данные лекарства
    result = []
    for med_name in selected_medications:
        med_info = next((m for m in MEDICATIONS_CATALOG if m["name"] == med_name), None)
        if med_info:
            result.append({
                "name": med_info["name"],
                "group": med_info["group"],
                "dosage": med_info["typical_dosage"],
                "frequency": med_info["typical_frequency"],
                "duration": f"{random.randint(1, 12)} месяцев",
                "notes": med_info.get("notes", "")
            })
    
    return result

def generate_visit_history(num_visits: int) -> List[Dict]:
    """Генерирует историю визитов пациента"""
    
    visits = []
    for i in range(min(num_visits, random.randint(3, 10))):
        visit_date = datetime.now() - timedelta(days=random.randint(1, 180))
        visits.append({
            "date": visit_date.strftime("%d.%m.%Y"),
            "doctor": random.choice(["Петров И.И.", "Волков В.В.", "Смирнова М.А.", "Козлов А.В."]),
            "diagnosis": random.choice(DIAGNOSES),
            "notes": f"Плановый осмотр. Состояние {'хорошее' if random.random() < 0.7 else 'удовлетворительное'}."
        })
    
    return sorted(visits, key=lambda x: x["date"], reverse=True)

def generate_patient_notes() -> str:
    """Генерирует заметки о пациенте"""
    
    notes_templates = [
        "Пациент соблюдает назначения, приверженность к лечению хорошая.",
        "Регулярно посещает врача, необходимо наблюдение.",
        "Требуется коррекция дозы препаратов в связи с побочными эффектами.",
        "Пациент жалуется на нарушение сна, проведена коррекция терапии.",
        "Анализы в норме, состояние стабильное.",
        "Требуется консультация узкого специалиста.",
    ]
    
    return random.choice(notes_templates)

# ============================================================================
# ФУНКЦИИ ПОИСКА И ФИЛЬТРАЦИИ
# ============================================================================

def search_patients(patients_db: List[Dict], query: str) -> List[Dict]:
    """Поиск пациентов по ФИО или ID"""
    
    query_lower = query.lower()
    results = []
    
    for patient in patients_db:
        full_name = f"{patient['last_name']} {patient['first_name']}".lower()
        patient_id = patient['id'].lower()
        
        if query_lower in full_name or query_lower in patient_id:
            results.append(patient)
    
    return results

def get_patient_by_id(patients_db: List[Dict], patient_id: str) -> Dict:
    """Получает пациента по ID"""
    
    for patient in patients_db:
        if patient['id'] == patient_id:
            return patient
    
    return None

def get_high_risk_patients(patients_db: List[Dict]) -> List[Dict]:
    """Возвращает пациентов высокого риска (5+ препаратов или возраст 75+)"""
    
    high_risk = [
        p for p in patients_db
        if len(p['medications']) >= 5 or p['age'] >= 75
    ]
    
    return high_risk
