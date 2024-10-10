import os
import requests as re

def get_inputs():
    clear()
    # Choose files
    xlsx_files = [f for f in os.listdir() if f.endswith('.xlsx') or f.endswith('.xls')] # All xlsx files

    print('Выберите файл для обработки')

    for i in range(len(xlsx_files)):
        print(f'{i+1}. {xlsx_files[i]}')
    
    print('0. Выбрать все файлы')
    print(' ')
    file_responce = input('')
    
    if file_responce:
        clear()



    # Choose template
    print('Выберите шаблон')

    # Choose template. Temp template -> templates
    templates = [f for f in os.listdir('./templates') if f.endswith('.html')]
    for i in range(len(templates)):
        print(f'{i+1}. {templates[i].replace(".txt" , "")}')
    print(' ')
    template_responce = input('')
    
    if template_responce:
        clear()
    # Choose time 
    print('Выберите период \n Можно выбрать несколько через пробел!!! 3 4')
    print('''
          1. Текущий месяц
          2. Прошлый месяц
          3. Текущий квартал
          4. Прошлый квартал
          5. Текущий год
          ''')
    period_responce = input('') # Use global time server

    if period_responce:
        clear()
    
    return file_responce , template_responce, period_responce


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')