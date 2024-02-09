import csv
import os.path
import re
from test import new_old_terms
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from analysis_done_text import check_key_value_in_text
from morpg_words import replace_terms_with_nlp, adapt_new_term,  \
    replace_and_adapt_text_multiprocessing

SCOPES = ["https://www.googleapis.com/auth/documents", "https://www.googleapis.com/auth/drive"]

DOCUMENT_ID = "1BJOEFZMU160Wgdik9ca_RVgDkXP5mu8gNRJlGJABTq0"

dict_words = new_old_terms
#     {
#     'ложная статистика': 'ложная метрика',
#     'ЦКП': 'продукт'
# }

def read_doc(id: str):
    doc_url = f'https://docs.google.com/document/d/{id}/edit'
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build("docs", "v1", credentials=creds)
    document = service.documents().get(documentId=id).execute()
    content = document['body']['content']
    document_title = document.get('title')
    text_old = clear_text(content)

    replacement_tittle: dict = replace_and_adapt_text_multiprocessing(document_title, dict_words)


    if not replacement_tittle:
        replacement_tittle = 'изменений нет'

    else:


        replacement_tittle = update_tittle_doc(id,creds, replacement_tittle)
        if replacement_tittle is False:
            replacement_tittle = 'изменений нет'


    replacements: dict = replace_and_adapt_text_multiprocessing(text_old, dict_words)
    if not replacements:
        replacements = 'изменений нет'
    else:
        replacements = doc_edit(id, replacements, creds, content)


    log_dict = [{
        'url': doc_url,
        'tittle': str(replacement_tittle),
        'changes': str(replacements[0]),
        'потенциальные замены':str(replacements[1])
    }]
    return save_log(log_dict)


    print(replacements)
    if doc_edit(id, replacements, creds, content):
        print('done')
    else:
        print('err')


def clear_text(content):
    document_text = ""
    for element in content:
        if 'paragraph' in element:
            for para_element in element['paragraph']['elements']:
                if 'textRun' in para_element and 'content' in para_element['textRun']:
                    document_text += para_element['textRun']['content']
    return document_text



def doc_edit(doc_id: str,replacements: dict, creds, content ):
    try:
        unique_keys = set()
        done_obj = []
        requests = []
        for old_sent, new_sent in replacements.items():

            words = check_key_value_in_text(dict_words, old_sent, new_sent)


            if not words:
                continue
            for word in words:
                word = update_value_case(word)
                for key, value in word.items():
                    if key not in unique_keys:
                        unique_keys.add(key)
                        if word not in done_obj:
                            done_obj.append(word)

        print(done_obj)
        for word in done_obj:
            for k,v in word.items():


            # Применяем регистр из old_sent к соответствующим словам в new_sent


                    requests.append({
                        'replaceAllText': {

                            'containsText': {
                                'text': k,
                                'matchCase': True  # или False, в зависимости от необходимости соблюдения регистра
                            },

                            'replaceText': v,
                            # 'startIndex': startIndex,
                            # 'endIndex': endIndex
                        }
                    })
        requests = [{'replaceAllText': {'containsText': {'text': 'Tonnus', 'matchCase': True}, 'replaceText': 'Business booster platform'}}]
        docs_service = build("docs", "v1", credentials=creds)
        res = docs_service.documents().batchUpdate(documentId=doc_id, body={'requests': requests}).execute()
        print(res)
        return done_obj, done_obj
    except Exception as e:

        return e, done_obj




def update_value_case(d):

    updated_dict = {}
    for key, value in d.items():
        # Проверяем, является ли ключ аббревиатурой (все буквы заглавные)
        if key.isupper():
            # Делаем все буквы значения заглавными
            updated_value = value.upper()
        # Проверяем, является ли первая буква ключа заглавной
        elif key[0].isupper():
            # Делаем первую букву значения заглавной
            updated_value = value.capitalize()
        else:
            updated_value = value
        updated_dict[key] = updated_value
    return updated_dict

def update_tittle_doc(id, creds, replacements_tittle ):
    try:
        for key, value in replacements_tittle.items():

            service = build('drive', 'v3', credentials=creds)
            file_metadata = {
                'name': value
            }
            service.files().update(fileId=id, body=file_metadata, fields='name', supportsAllDrives=True).execute()
            return value
    except:
        return False

def save_log(list_of_dicts):
    print(list_of_dicts)
    headers = list_of_dicts[0].keys()
    with open('log.csv', mode='a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        file.seek(0, 2)
        if file.tell() == 0:  # Если указатель файла находится в начале, файл пустой
            writer.writeheader()  # Пишем заголовки столбцов

            # Записываем словари в CSV файл
        writer.writerows(list_of_dicts)
# if __name__ == "__main__":
#
#     read_doc(DOCUMENT_ID)