from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
import re

# Расширенный словарь переводов английских терминов
translations = {
    # Общие термины
    'PRODUCT QUALITY CERTIFICATE': 'СЕРТИФИКАТ КАЧЕСТВА ПРОДУКЦИИ',
    'INSPECTION CERTIFICATE': 'СЕРТИФИКАТ ПРОВЕРКИ',
    'Certificate Number': 'Номер сертификата',
    'Certificate No.': 'Номер сертификата',
    'Certificate': 'Сертификат',
    
    # Компании
    'BENGANG STEEL PLATES Co., LTD': 'BENGANG STEEL PLATES Co., LTD',
    'Jiangsu Ruimao Mining Machinery Co., Ltd.': 'Jiangsu Ruimao Mining Machinery Co., Ltd.',
    'Jiangyin Hengda Metal Pressing Parts Co., Ltd.': 'Jiangyin Hengda Metal Pressing Parts Co., Ltd.',
    'Jiangsu Provincial Special Equipment Safety Supervision and Inspection Research Institute': 'Центр исследований надзорной проверки безопасности специального оборудования провинции Цзянсу',
    
    # Технические термины
    'HOT ROLLING MILL': 'ГОРЯЧЕКАТАТНЫЙ ЗАВОД',
    'AS ROLLED': 'ГОРЯЧЕКАТАНАЯ',
    'Hot rolled steel strip': 'Горячекатаная стальная полоса',
    'Actual Weight': 'Фактический вес',
    'Elliptical Head': 'Эллиптическое днище',
    
    # Поля документов
    'Manufacturing Unit': 'Изготовитель',
    'Product Name': 'Наименование продукции',
    'Product Code': 'Номер продукции',
    'Batch Number': 'Номер партии',
    'Head Type Specification': 'Тип и размеры днища',
    'Quantity': 'Количество',
    'Material': 'Материал',
    'Processing with supplied materials': 'Изготовление из предоставленного материала',
    'Manufacturing Date': 'Дата изготовления',
    'Supervision Inspection Personnel': 'Инспектор надзорной проверки',
    'Supervision Inspection Institution': 'Организация надзорной проверки',
    'Reviewer': 'Рецензент',
    'Approver': 'Утверждающий',
    'Date': 'Дата',
    'Address': 'Адрес',
    'Phone': 'Телефон',
    'Postal Code': 'Почтовый индекс',
    'Note': 'Примечание',
    'Approval Certificate No.': 'Номер разрешения',
    
    # Адреса
    'Building': 'Здание',
    'Road': 'улица',
    'City': 'город',
    
    # Другие
    'Yes': 'Да',
    'No': 'Нет',
    'Total': 'Итого',
    'Total Weight': 'Общий вес',
    'Total Pieces': 'Всего штук',
}

def translate_text(text):
    """Переводит английские фразы в тексте на русский"""
    if not text or not isinstance(text, str):
        return text
    
    result = text
    
    # Сначала заменяем длинные фразы
    for eng, rus in sorted(translations.items(), key=lambda x: -len(x[0])):
        # Заменяем точные совпадения (с учетом регистра)
        result = result.replace(eng, rus)
        # Заменяем с учетом регистра (только первая буква)
        if eng[0].isupper():
            lower_eng = eng[0].lower() + eng[1:]
            lower_rus = rus[0].lower() + rus[1:] if rus else rus
            result = result.replace(lower_eng, lower_rus)
    
    return result

def process_document(filepath):
    """Обрабатывает документ Word, переводя английские тексты"""
    print(f'Обработка файла: {filepath}')
    
    if not os.path.exists(filepath):
        print(f'Файл не найден: {filepath}')
        return False
    
    try:
        doc = Document(filepath)
        changes_made = False
        
        # Обработка всех параграфов
        for paragraph in doc.paragraphs:
            for run in paragraph.runs:
                if run.text:
                    translated = translate_text(run.text)
                    if translated != run.text:
                        run.text = translated
                        changes_made = True
        
        # Обработка таблиц
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        for run in paragraph.runs:
                            if run.text:
                                translated = translate_text(run.text)
                                if translated != run.text:
                                    run.text = translated
                                    changes_made = True
        
        # Сохранение документа
        doc.save(filepath)
        print(f'✓ Файл обновлен: {filepath}')
        if changes_made:
            print(f'  Сделаны изменения в документе')
        return True
        
    except Exception as e:
        print(f'✗ Ошибка при обработке файла {filepath}: {e}')
        return False

def translate_new_document(filepath, output_path=None):
    """
    Универсальная функция для перевода нового документа
    
    Args:
        filepath: Путь к исходному файлу
        output_path: Путь для сохранения (если None, перезаписывает исходный)
    """
    if output_path is None:
        output_path = filepath
    
    return process_document(filepath if output_path == filepath else filepath)

if __name__ == '__main__':
    # Обработка существующих документов
    base_dir = r'C:\Users\stanl\Atlas_Copco\Atlas_Copco\Сканы китайских документов\V250346'
    
    files_to_process = [
        'V250346-страница-21-产品质量证明书.doc',
        'V250346-страница-22-Сертификат надзорной проверки изготовления днищ.doc'
    ]
    
    print('Начало обработки документов...\n')
    
    for filename in files_to_process:
        filepath = os.path.join(base_dir, filename)
        process_document(filepath)
    
    print('\n✓ Все документы обработаны!')
    print('\nДля обработки новых документов используйте функцию translate_new_document()')

