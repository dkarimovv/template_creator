import os
import asyncio
import secrets
import string
import warnings

import pandas as pd
import requests as re


from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from pyppeteer import launch
from PyPDF2 import PdfMerger

from graphs import create_pie_chart

def current_time():
    headers = {
        'X-Api-Key' : 'YOURTOKEN'
    }
    responce  = re.get('https://api.api-ninjas.com/v1/worldtime?timezone=Europe/Moscow', headers=headers)
    datetime = responce.json()
    return datetime


# Прописать разграничитель между разными типами пероидов. (Месяц, год, квартал)
    # ? = period 


def process_inputs(file_responce , template_responce, period_responce ):
    # Process files input
    all_files = [f for f in os.listdir() if f.endswith('.xlsx') or f.endswith('.xls')]
    file_responce = int(file_responce)
    if file_responce == 0:
        file_to_work = all_files
    else:
        file_to_work = all_files[file_responce-1]
    
    
    # Process templates

    all_templates = [f for f in os.listdir('./templates/') if f.endswith('.html')]
    template_responce = int(template_responce)
    if template_responce == 0:
        print('Error was choosed wrong template')
    else:
        template_to_work = all_templates[template_responce-1]  # temp decision. waiting for templates

    # Process period 
    period_to_work = ''
    if len(period_responce) == 1:
        period_to_work = period_lcs(period_responce)
    else:
        if ',' in period_responce:
            args = period_responce.split(' ')
            for arg in args:
                period_to_work += f'{period_lcs(arg)}?'
            period_to_work = period_to_work[:-1]
        elif ' ' in period_responce:
            args = period_responce.split(' ')
            for arg in args:
                period_to_work += f'{period_lcs(arg)}?'
            period_to_work = period_to_work[:-1]

    return file_to_work , template_to_work , period_to_work

def period_lcs(period_responce):
    quarts ={
        ('one') : '08 09 10',
        ('two') : '11 12 01',
        ('three') : '02 03 04',
        ('four') : '05 06 07'
    }
    
    match period_responce:
        case '1':
            # Current month
            return current_time()['month']
        case '2':
            curm  = current_time()['month']
            if curm != '10' and curm != '01':
                pastm = f'{int(curm)//10}{(int(curm)%10)-1}'
            else:
                if curm == '10':
                    pastm = '09'
                else:
                    pastm = '12'
            return pastm
        case '3':
            curm  = current_time()['month']
            if curm in quarts['one']:
                return str(quarts['one'])
            elif curm in quarts['two']:
                return str(quarts['two'])
            elif curm in quarts['three']:
                return str(quarts['three'])
            elif curm in quarts['four']:
                return str(quarts['four'])
            else:
                print('Error. Data not in quarters')
            return []
        case '4':
            curm  = current_time()['month']
            if curm in quarts['one']:
                return str(quarts['four'])
            elif curm in quarts['two']:
                return str(quarts['one'])
            elif curm in quarts['three']:
                return str(quarts['two'])
            elif curm in quarts['four']:
                return str(quarts['three'])
            else:
                print('Error. Data not in quarters')
            return []
        case '5':
            return str(current_time()['year'])
        
def start(file_to_prepare , template: str, period: str):
    if type(file_to_prepare) == list:
        for file in file_to_prepare:
            generate_report(str(file), template, period)
    else:
        generate_report(file_to_prepare, template, period)

def generate_report(file_to_prepare: str, template: str, period: str):

    file_name = prepare_table(file_to_prepare)
    # Загружаем данные из Excel файла
    df = pd.read_excel(file_name, engine='openpyxl')

    # Приводим названия компаний к единому виду в столбцах Наименование/ФИО и Наименование
    replacements = {
        '''
            REPLACMENTS PLACE
        '''
    }

    df['Наименование/ФИО'] = df['Наименование/ФИО'].replace(replacements, regex=True)
    df['Наименование'] = df['Наименование.1'].replace(replacements, regex=True)

    # Преобразование столбца с датой операции к типу datetime
    df['Дата операции'] = pd.to_datetime(df['Дата операции'], errors='coerce')

    # Фильтрация данных по периоду
    filtered_df = pd.DataFrame()
    if '?' in period:
        periods = period.split('?')
        for p in periods:
            if len(p) == 2:  # Проверяем только по месяцу
                target_month = int(p)
                filtered_df = pd.concat([filtered_df, df[df['Дата операции'].dt.month == target_month]])
            elif len(p) == 8:  # Проверяем по кварталу (перечень месяцев)
                target_months = [int(m) for m in p.split()]
                filtered_df = pd.concat([filtered_df, df[df['Дата операции'].dt.month.isin(target_months)]])
            elif len(p) == 4:  # Проверяем по году
                target_year = int(p)
                filtered_df = pd.concat([filtered_df, df[df['Дата операции'].dt.year == target_year]])
            else:
                print("Неверный формат периода. Ожидается длина 2, 8 или 4.")
                return
    else:
        if len(period) == 2:  # Проверяем только по месяцу
            target_month = int(period)
            filtered_df = df[df['Дата операции'].dt.month == target_month]
        elif len(period) == 8:  # Проверяем по кварталу (перечень месяцев)
            target_months = [int(m) for m in period.split()]
            filtered_df = df[df['Дата операции'].dt.month.isin(target_months)]
        elif len(period) == 4:  # Проверяем по году
            target_year = int(period)
            filtered_df = df[df['Дата операции'].dt.year == target_year]
        else:
            print("Неверный формат периода. Ожидается длина 2, 8 или 4.")
            return

    # Проверка на пустой DataFrame после фильтрации
    if filtered_df.empty:
        print("Нет данных для заданного периода.")
        os.remove(file_name)
        return

    # Проверка на пустые значения в колонке "Наименование"
    empty_names = filtered_df[filtered_df['Наименование'].isna()]
    if not empty_names.empty:
        print(f"Есть строки с пустыми наименованиями:\n{empty_names}")

    # Проверка ИНН/КИО на длину
    filtered_df['ИНН/КИО'] = filtered_df['ИНН/КИО'].astype(str)
    incorrect_inn_kpo = filtered_df[~filtered_df['ИНН/КИО'].str.len().isin([9, 12])]
    if not incorrect_inn_kpo.empty:
        print(f"Есть строки с некорректным ИНН/КИО:\n{incorrect_inn_kpo}")

    filtered_df = filtered_df[filtered_df['По кредиту (руб)'] > 0]

    if filtered_df.empty:
        print("Нет данных для компаний с ненулевыми дебетами.")
        os.remove(file_name)
        return

    # Группировка данных и расчет сумм
    report = filtered_df.groupby(['Наименование', 'ИНН/КИО']).agg({
        'Дата операции': 'first',  # Можно заменить на 'min' для получения первой даты
        # 'По дебету (руб)': 'sum',
        'По кредиту (руб)': lambda x: round(x.sum(), 2),
        'Назначение платежа': '<br><br>'.join
    }).reset_index()
    
    # Проверка, чтобы убедиться, что есть данные для названия компании
    if not filtered_df['Наименование/ФИО'].empty:
        company_name = filtered_df['Наименование/ФИО'].iloc[0]
    else:
        company_name = "НеизвестнаяКомпания"
    transactions = []
    intermediary_companies = report['Наименование'].unique().tolist()

    for _, row in report.iterrows():
        transactions.append({
            'date': row['Дата операции'].strftime('%Y-%m-%d'),
            'company_name': row['Наименование'],
            'company_inn': row['ИНН/КИО'],
            'debit': row['По кредиту (руб)'],
            'payment_description': row['Назначение платежа']
        })

    # Сохраняем в новый Excel файл
    today_date = datetime.now().strftime("%Y%m%d")
    output_file_name = f'Отчет_{company_name}_{today_date}_{create_password()}'

    # Вызываем templates_handler для создания PDF
    pdf_path = templates_handler(template, company_name, transactions, intermediary_companies, output_file_name)

    intermediary_output_file = f'companies_{output_file_name}'
    intermediary_pdf_path = templates_handler('test.html', company_name, [], intermediary_companies, intermediary_output_file)

    graph_output_file = f'graph_{output_file_name}'
    graph_pdf_path = templates_handler('graph.html' , company_name, transactions, intermediary_companies, graph_output_file)
    merge_pdf(pdf_path, intermediary_pdf_path, graph_pdf_path)

    os.remove(file_name)
    print(f"Генерация отчета завершена: {pdf_path}")


def templates_handler(template_type: str, company_name: str, transactions: list, intermediary_companies: list, output_file_name: str):
    # Загружаем шаблон
    env = Environment(loader=FileSystemLoader('./templates/'))
    template = env.get_template(f'{template_type}')

    # Создаем данные для графика в формате JSON
    graph_data = create_pie_chart(transactions)

    # Рендерим HTML контент на основе шаблона
    rendered_content = template.render(
        company_name=company_name,
        transactions=transactions,
        intermediary_companies=intermediary_companies,
        graph_data=graph_data
    )

    # Если требуется HTML-отчет, сохраняем его
    html_output_path = f'{output_file_name}.html'
    if 'html' in template_type:
        with open(html_output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)

    # Генерация PDF-отчета
    pdf_output_path = f"./reports/{output_file_name}.pdf"
    asyncio.get_event_loop().run_until_complete(render_pdf(rendered_content, pdf_output_path))


    # Удаляем временный HTML файл
    os.remove(html_output_path)

    return pdf_output_path


async def render_pdf(html_content: str, output_pdf_path: str):
    browser = await launch(headless=True)
    page = await browser.newPage()
    
    # Открытие HTML контента в браузере
    await page.setContent(html_content)

    await asyncio.sleep(4)
    
    # Сохранение страницы как PDF
    await page.pdf({
        'path': output_pdf_path,
        'format': 'A4',
        'printBackground': True,
        'landscape': True,
        'margin': {
            'top': '5mm',   
            'bottom': '5mm',
        }
    })
    
    await browser.close()


def prepare_table(file_path : str) -> str:
    output_path = f'prepared_{file_path}'
    warnings.simplefilter("ignore", UserWarning)
    # Чтение таблицы
    df = pd.read_excel(file_path, header=None)

    df = df.drop(df.index[13])

    # 1. Удаление первых 7 столбцов
    df = df.iloc[:, 11:]

    # 2. Удаление первых 9 строчек
    df = df.iloc[10:, :]

    df.columns = df.iloc[0]  # Используем вторую строку (с индексом 1) как заголовок
    df = df.drop(df.index[0])
    df = df.drop(df.index[1])

    df = df.drop(df.columns[8:10], axis=1)

    df = df.dropna(how='all')
    # Сохранение в новый файл
    df.to_excel(output_path, index=False)
    print(f"Таблица успешно обработана и сохранена в {output_path}")

    return output_path


def merge_pdf(file_table, file_companies, file_graphs):
    merger = PdfMerger()

    title_list = 'title-page.pdf'

    merger.append(title_list)
    merger.append(file_table)
    merger.append(file_companies)
    merger.append(file_graphs)

    merger.write(file_table)
    merger.close()

    os.remove(file_companies)
    os.remove(file_graphs)

def create_password() -> str:
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(5))
    return password