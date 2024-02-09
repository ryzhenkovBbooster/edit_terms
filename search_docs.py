def extract_document_id_from_url(url):
    """
    Функция для извлечения идентификатора документа Google Docs из URL.

    Параметры:
    - url (str): URL документа Google Docs.

    Возвращает:
    - str: Идентификатор документа, если URL корректный, иначе None.
    """
    import re

    # Регулярное выражение для поиска ID документа в URL
    pattern = r'/d/(.*?)/'
    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None


urls = ["https://docs.google.com/document/d/1GqWL5H6ytdubCFIyOYQQ-nnFENnZzFCsKxE1FF0lVks/edit?usp=drive_link", "https://docs.google.com/document/d/1mbxh-UH6GrSZ2Ni4fj9Rl_wxRlIsc6XutMGrrHZ7SRE/edit?usp=drive_link", "https://docs.google.com/document/d/10S45wkhw805cEkES1UuE6h86hD6XhzWYGdHMxqllN5w/edit?usp=drive_link", "https://docs.google.com/document/d/1_lZ7lWJ-httxRh5ZgtxkQhD8sqP9nkbihrkW4GQW-Ac/edit?usp=drive_link", "https://docs.google.com/document/d/12gs-Du8RK-lsjN5l4dn-PMuNEq3eAmLCQS6BO9equhE/edit?usp=drive_link", "https://docs.google.com/document/d/1zDllc8oNsETgJ75Mgv2GOPF3Zy5h8yACdIZwlQKhaDs/edit?usp=drive_link", "https://docs.google.com/document/d/1tWf2a48bRCHH6ZFUuvHpH3B8RXKzLB7l_FarlZRjfY4/edit?usp=drive_link", "https://docs.google.com/document/d/1Wkxhv_4Zte7UDsfV85IstayXuXb55UqFJ9gPW_x259Q/edit?usp=drive_link", "https://docs.google.com/document/d/1KpOkp2zxTzHu7MELr2Zh324X7z1D76Ib_qFtPsJlwCM/edit?usp=drive_link", "https://docs.google.com/document/d/1z12qS7Ne557L8GB444oDHuYCGEWpdTArpz24gEL8pXA/edit?usp=drive_link", "https://docs.google.com/document/d/140wbu1ec9xv_dIU1EgKqnAMJZt1qiOxjtaSOUsLr9Rc/edit?usp=drive_link", "https://docs.google.com/document/d/1zSMgwievoiWV0PF5F_T1Hl-QQdRWBLglmGEi2DOOM_Q/edit?usp=drive_link", "https://docs.google.com/document/d/1I5Bwud9EG3fy3xzGgEGXnNahMq1FcYPseUZat_i1z70/edit?usp=drive_link", "https://docs.google.com/document/d/1r5nPdMNwrts66VjrweyoNzg8yW2Hq_s6CDwpa54RFec/edit?usp=drive_link", "https://docs.google.com/document/d/1uyomPq5pxmTJqE1AOCX3o2KdkNw6GDSQ7PN-OdKmuMU/edit?usp=drive_link", "https://docs.google.com/document/d/1ed6jcVmtY7zGl9KbW6D8VZIDEgWdvwY5vZrzXTsFKcE/edit?usp=drive_link", "https://docs.google.com/document/d/1RWqaB0EVtKZrc7PzD1ZW71CJjChXJN0YAYjEPc9B-as/edit?usp=drive_link", "https://docs.google.com/document/d/1oxv-E1TY35-CKYYCHLuXuq-FVAo4m3MhboUhNusCnuo/edit?usp=drive_link", "https://docs.google.com/document/d/1YKb3-zemURBNHCViMxHPOZIOZr6QUwE0ywXoSnpo4nc/edit?usp=drive_link", "https://docs.google.com/document/d/1n2fbqLi5gn58jSTwev3DRLzqs0t0CLBzVln5z98iCas/edit?usp=drive_link", "https://docs.google.com/document/d/15GYIfQmHYXblGcZEBl372Puwux8bG5pn43_vF7onFPA/edit?usp=drive_link", "https://docs.google.com/document/d/12z2Phuw2EnlIzshC26pkOenUNThUMyz1fIQY9dieK8U/edit?usp=drive_link", "https://docs.google.com/document/d/1mqa95btOcClkfPo-l5c4wXXBEBjdnfOhzCOkhuFu-5c/edit?usp=drive_link", "https://docs.google.com/document/d/1Pw5aZWiK9ydkB20Evja8FnC_EYNEf62dmzsDg0HpyZk/edit?usp=drive_link", "https://docs.google.com/document/d/1w-VcxP2MP75Q78anF8AO4qa0RmwlNDV2VkEGY-mol0o/edit?usp=drive_link", "https://docs.google.com/document/d/1-dk4nhCcxOwWf3X-BqS1UUL1c7oOB4CeUC2RFVsJM5k/edit?usp=drive_link", "https://docs.google.com/document/d/16KD7wvtpA32i-7W1Ftyl_-UMsS1N_D3sq6e9W8rCZfo/edit?usp=drive_link", "https://docs.google.com/document/d/1j82qTjNvlaB2i81MdZDBeMB9tfpsg9dUoI9qyhv1jL8/edit?usp=drive_link", "https://docs.google.com/document/d/1OnF46lpWd2kpShE3MX1H_k-jqwt-f-Tz86FY84ugNKI/edit?usp=drive_link", "https://docs.google.com/document/d/1yMHTFquekrVtZ4y5E8bNQDurQjnOX1JOoPQcG7aOcNE/edit?usp=drive_link", "https://docs.google.com/document/d/1Oo10CjOKHLPkl8IZwp4OftI37cyo0L4lNTPEotVBwpk/edit?usp=drive_link", "https://docs.google.com/document/d/1SoG7q8Bsj3nUyPCeYjzNuqe8WnJh2AmxE83a0_MmdMM/edit?usp=drive_link", "https://docs.google.com/document/d/1CuXmnFHQ3AM2-XTZ8goi9HY1caDz1xcuiZ3yNm-Y5kA/edit?usp=drive_link", "https://docs.google.com/document/d/1qnTTddX2x1tX39y4BMkoDuN9Sbjjy_7SeEk2d7zN6pI/edit?usp=drive_link", "https://docs.google.com/document/d/12N5qQih6XLNOXhA25vsnes6Ndse5vOtxyMNgcFXTVk0/edit?usp=drive_link"]
# Пример использования функции


