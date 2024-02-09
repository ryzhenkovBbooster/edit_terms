import difflib
import string
from collections import defaultdict

import spacy
from spacy.matcher import Matcher

nlp = spacy.load("ru_core_news_sm")


def dif_text(str1, str2):
    differ = difflib.Differ()
    diff = list(differ.compare(str1.split(), str2.split()))

    differences = [item for item in diff if item.startswith('- ') or item.startswith('+ ')]

    cleaned_differences = []
    for difference in differences:
        # Удалить знаки пунктуации из выборки
        clean_difference = ''.join(filter(lambda char: char.isalnum() or char in ['+', '-'], difference))
        cleaned_differences.append(clean_difference)

    for difference in cleaned_differences:
        if difference == '+' or difference == '-':
            continue
        print(difference)

string1 = "Каждый сотрудник может указать на отклонение не только в тех аспектах, которые касаются производства его ЦКП, но и на отклонения в работе коллег любого отдела и департамента."
string2 = "Каждый сотрудник мочах указать на отклонение не только в тех аспектах , которые касаются производства его продуктах , но и на отклонение в работе коллег любого отдела и департамента ."


# dif_text(string1, string2)
def preprocess_text(text):
    """Предварительная обработка и лемматизация текста, возвращает обработанный doc объект."""
    return nlp(text)


def create_matcher_patterns(obj):
    """Создает шаблоны для Matcher, основываясь на лемматизации ключей и значений словаря."""
    patterns = []
    for key, _ in obj.items():
        doc = nlp(key)
        pattern = [{"LEMMA": token.lemma_} for token in doc]
        patterns.append((key, pattern))
    return patterns


def find_all_matches_and_texts(patterns, doc):
    """Ищет все совпадения в тексте и возвращает их вместе с исходным текстом."""
    matcher = Matcher(nlp.vocab)
    for key, pattern in patterns:
        matcher.add(key, [pattern])

    matches = matcher(doc, as_spans=True)  # Используем as_spans=True для получения Span объектов
    match_texts = defaultdict(list)
    for span in matches:
        key = span.label_
        match_texts[key].append(span.text)  # Сохраняем исходный текст совпадения

    return match_texts


def check_key_value_in_text(obj, text1, text2):
    doc1 = preprocess_text(text1)
    doc2 = preprocess_text(text2)

    patterns_key = create_matcher_patterns({k: v for k, v in obj.items()})
    patterns_value = create_matcher_patterns({v: k for k, v in obj.items()})

    # Ищем совпадения и сохраняем исходные тексты
    matches_texts1 = find_all_matches_and_texts(patterns_key, doc1)
    matches_texts2 = find_all_matches_and_texts(patterns_value, doc2)

    results = []
    for key, value in obj.items():
        if key in matches_texts1 and value in matches_texts2:
            # Итерируем по минимальному количеству вхождений между ключом и значением
            min_count = min(len(matches_texts1[key]), len(matches_texts2[value]))
            for i in range(min_count):
                # Добавляем пары исходных текстов в результаты
                results.append({matches_texts1[key][i]: matches_texts2[value][i]})

    return results