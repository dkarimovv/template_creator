
# EN:
# Project Title: Report Generation using Excel Data

This project is designed for automatic report processing, including generating PDF files based on Excel data. It also uses pie charts for data visualization and various filters to select data by time periods.

## Key Features:
- **Excel File Processing**: Ability to select one or more files for processing.
- **Templates**: Selection of an HTML template for report generation.
- **Time Period Filtering**: Supports filtering data by months, quarters, and years.
- **PDF Report Generation**: Integration with Jinja2 for HTML rendering and PyPDF2 for merging PDF files.
- **Pie Charts**: Visualization of transactions through pie charts created using Plotly.

## Technology Stack:
- **Python**: The main programming language for data processing logic.
- **pandas**: For working with Excel files and data manipulation.
- **Plotly**: For creating interactive pie charts.
- **Jinja2**: For rendering HTML templates.
- **PyPDF2**: For merging multiple PDFs into one.
- **asyncio and pyppeteer**: For rendering HTML content into PDF.
- **requests**: For fetching current time data via API.

## Project Structure:
-> graphs.py # Logic for creating pie charts. 
-> inputs.py # Handles user input (files, templates, periods). 
-> main.py # Entry point of the project, coordinating input and processing. 
-> process.py # Core logic for data processing, report generation, and graphs.

## How to Use:

1. Run the main script `main.py` to start the report generation process.
2. The program will prompt you to select one or more Excel files for processing.
3. After that, you will need to choose a report template.
4. Select a time period (month, quarter, or year) to filter the data.
5. Reports will be generated in PDF format with charts and saved to the `reports` directory.


# RU:
# Генерация отчетов с использованием данных из Excel

Этот проект предназначен для автоматической обработки отчетов, включая генерацию PDF-файлов на основе данных из Excel. В проекте также используются графики (пироговые диаграммы) для визуализации данных и различные фильтры для отбора данных по временным периодам.

## Основные функции:
- **Обработка Excel-файлов**: Возможность выбрать один или несколько файлов для обработки.
- **Шаблоны**: Выбор HTML-шаблона для создания отчетов.
- **Фильтрация по периодам**: Поддержка фильтрации данных по месяцам, кварталам и годам.
- **Генерация PDF отчетов**: Интеграция с Jinja2 для рендеринга HTML и PyPDF2 для объединения PDF-файлов.
- **Пироговые диаграммы**: Визуализация транзакций через графики, созданные с использованием Plotly.

## Технологический стек:
- **Python**: Язык программирования для основной логики обработки данных.
- **pandas**: Для работы с Excel-файлами и обработки таблиц.
- **Plotly**: Для создания интерактивных пироговых диаграмм.
- **Jinja2**: Для рендеринга HTML-шаблонов.
- **PyPDF2**: Для объединения нескольких PDF-файлов в один.
- **asyncio и pyppeteer**: Для рендеринга HTML-контента в PDF.
- **requests**: Для получения данных текущего времени через API.

## Структура проекта:

-> graphs.py # Логика создания пироговых диаграмм. 
-> inputs.py # Обработка ввода от пользователя (файлы, шаблоны, периоды). 
-> main.py # Точка входа в проект, координирует ввод и обработку. 
-> process.py # Основная логика обработки данных, генерация отчетов и графиков.

## Как использовать:

1. Запустите главный скрипт `main.py`, чтобы начать процесс обработки отчетов.
2. Программа предложит выбрать Excel-файл(ы) для обработки.
3. Затем вам нужно будет выбрать шаблон отчета.
4. Выберите период (месяц, квартал или год) для фильтрации данных.
5. Отчеты будут сгенерированы в формате PDF с графиками и сохранены в директорию `reports`.
