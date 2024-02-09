from functools import lru_cache
from multiprocessing import Pool

from transformers import AutoTokenizer, AutoModel
import torch

import pymorphy2
import re
import spacy
from tqdm import tqdm


# tokenizer = AutoTokenizer.from_pretrained("DeepPavlov/rubert-base-cased")
# model = AutoModel.from_pretrained("DeepPavlov/rubert-base-cased")

nlp = spacy.load("ru_core_news_sm")
morph = pymorphy2.MorphAnalyzer()

# Исправленная функция для замены с учетом падежей


# def replace_and_adapt_text(text, replacement_dict):
#     # Разбиваем текст на предложения
#     doc = nlp(text)
#     sentences = list(doc.sents)
#     updated_sentences = []
#
#     for sentence in sentences:
#         original_sentence_text = sentence.text
#         # Применяем функцию замены терминов
#         replaced_text, replaced = replace_terms_with_nlp(original_sentence_text, replacement_dict)
#
#         # Проверяем, была ли произведена замена
#         if replaced :
#             # Применяем функцию адаптации
#             print(original_sentence_text)
#             adapted_sentence = adapt_new_term(original_sentence_text, replaced_text)
#             updated_sentences.append(adapted_sentence)
#         else:
#             updated_sentences.append(original_sentence_text)
#
#     # Собираем текст обратно
#     updated_text = " ".join(updated_sentences)
#     return updated_text
def replace_and_adapt_sentence(sentence_text, replacement_dict):
    # Применяем функцию замены терминов
    replaced_text, replaced, old_terms = replace_terms_with_nlp(sentence_text, replacement_dict)

    # Проверяем, была ли произведена замена
    if replaced:
        # Применяем функцию адаптации
        adapted_sentence, obj_new_term = adapt_new_term(sentence_text, replaced_text)

        return (adapted_sentence, True, sentence_text)
        # return (str(obj_new_term), True, str(old_terms))
    else:
        return (sentence_text, False)

def worker(args):
    return replace_and_adapt_sentence(*args)

def replace_and_adapt_text_multiprocessing(text, replacement_dict):
    doc = nlp(text)
    sentences = [(sentence.text, replacement_dict) for sentence in doc.sents]

    # Определите количество процессов в зависимости от вашей системы
    with Pool(processes=8) as pool:
        updated_sentences = pool.map(worker, sentences)


    # Собираем текст обратно
    updates_dict = {result[2]: result[0] for result in updated_sentences if result[1]}

    return updates_dict
def replace_terms_with_nlp(text, replacement_dict):
    doc = nlp(text)
    original_forms = []
    # Получаем лемматизированный текст как список лемм
    lemmas = [token.lemma_ for token in doc]
    # Соединяем леммы обратно в строку для упрощения поиска словосочетаний
    lemmatized_text = " ".join(lemmas)

    replaced = False
    # Замена слов и словосочетаний из словаря
    for old, new in replacement_dict.items():
        # Лемматизируем старое словосочетание из словаря замен
        old_lemma = " ".join([token.lemma_ for token in nlp(old)])

        new_lemma = " ".join([token.lemma_ for token in nlp(new)])
        if old_lemma in lemmatized_text:
            for token in doc:
                if token.lemma_ == old_lemma:
                    original_forms.append(token.text)

        # Заменяем старое словосочетание новым, используя лемматизированные формы
            lemmatized_text = lemmatized_text.replace(old_lemma, new_lemma)
            replaced = True


    # Возвращаем обратно в исходный текст (здесь может потребоваться дополнительная обработка для восстановления исходного форматирования)

    return lemmatized_text, replaced, original_forms

@lru_cache(maxsize=None)
def morph_parse_cached(word):
    return morph.parse(word)[0]

@lru_cache(maxsize=None)
def nlp_cached(word):
    return nlp(word)


def adapt_new_term(original_text, new_term):
    # print("new: ", new_term)
    # Разбираем исходный текст на токены
    doc = nlp(original_text)
    adapted_phrase = []
    adapted_new_term = []
    exclude_words = ['мочь']

    # Для каждого слова в новом термине находим ближайшее слово в исходном тексте
    # и адаптируем новое слово под его грамматические характеристики
    for new_word in tqdm(new_term.split(), desc=f'Обработка текста на верхнем уровне'):

        max_similarity = 0
        target_form = None
            # Пропускаем токены, которые не несут значимой семантической нагрузки
        for token in doc:
            # Используем pymorphy2 для анализа каждого слова в исходном тексте
            # morph_info_original = morph.parse(token.text)[0]
            # Пытаемся определить, какая форма нового слова будет наиболее подходящей
            # На основе семантического сходства и грамматических характеристик
            for form in morph_parse_cached(new_word).lexeme:
                similarity = nlp_cached(form.word).similarity(token)  # Оцениваем сходство
                if similarity > max_similarity:
                    max_similarity = similarity
                    target_form = form
        if target_form:
            adapted_phrase.append(target_form.word)
            adapted_new_term.append(target_form.word)
        else:
            adapted_phrase.append(new_word)
            adapted_new_term.append(new_word)# Если адаптация не удалась, используем исходное слово

    return ' '.join(adapted_phrase), adapted_new_term
# def get_embedding(text):
#     inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
#     outputs = model(**inputs)
#     embeddings = outputs.last_hidden_state.mean(dim=1)
#     return embeddings
#
# def adapt_new_term(original_text, new_text):
#     adapted_phrase = []
#     exclude_words = []
#
#     original_tokens = original_text.split()
#     new_tokens = new_text.split()
#
#     # Замените этот порог сходства на более низкий (например, 0.5) и настройте его при необходимости
#     similarity_threshold = 0.2
#
#     for original_word, new_word in tqdm(zip(original_tokens, new_tokens), total=len(original_tokens),
#                                         desc='Adapting words'):
#         if new_word in exclude_words:
#             adapted_phrase.append(original_word)
#             continue
#
#         # Получаем эмбеддинги для оригинального и нового слова
#         original_embedding = get_embedding(original_word)
#         new_embedding = get_embedding(new_word)
#
#         # Вычисляем косинусное сходство между эмбеддингами
#         similarity = torch.nn.functional.cosine_similarity(original_embedding, new_embedding)
#
#         # Учет контекста: рассматриваем не только текущее слово, но и соседние
#         context_words = original_tokens[max(0, original_tokens.index(original_word) - 2):
#                                        min(len(original_tokens), original_tokens.index(original_word) + 3)]
#
#         # Если сходство превышает порог и слово в контексте, заменяем его
#         if similarity.item() > similarity_threshold and original_word in context_words:
#             # Адаптируем новое слово, используя морфологический анализ
#             original_form = morph.parse(original_word)[0]
#             new_form = morph.parse(new_word)[0]
#             adapted_form = new_form.inflect(
#                 {tag for tag in original_form.tag.grammemes if tag in new_form.tag.grammemes})
#             if adapted_form:
#                 adapted_phrase.append(adapted_form.word)
#             else:
#                 adapted_phrase.append(new_word)  # Используем новое слово, если адаптация невозможна
#         else:
#             adapted_phrase.append(original_word)  # Оставляем оригинальное слово
#
#     return ' '.join(adapted_phrase)
replacement_dict = {
    "": "новый термин",
    "старое словосочетание": "новое словосочетание",
    'велосипед': "машина",
    "ценообразование": "Скорректированный Валовой Доход (сокр. СВД)"
    # Добавьте сюда свои термины
}

# text = 'Здесь ваш текст с использованием старых терминов и словосочетаний в разных формах и велосипеды.'
text = "Много ценообразования"

# new_text = replace_terms_with_nlp(text, replacement_dict)
#
# print(adapt_new_term(text, new_text))