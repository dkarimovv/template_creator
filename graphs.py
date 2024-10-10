import plotly.graph_objs as go

def create_pie_chart(all_info: list, threshold: float = 0.01) -> dict:
    intermediary_companies = []
    transactions = []

    # Собираем данные о компаниях и транзакциях
    for i in all_info:
        intermediary_companies.append(i['company_name'])
        transactions.append(i['debit'])

    # Обработка ошибок в данных транзакций
    if not transactions or any(t is None or not isinstance(t, (int, float)) for t in transactions):
        print("Некорректные данные транзакций, подставляем заглушки.")
        transactions = [1] * len(intermediary_companies)
    
    # Обработка ошибок в данных компаний
    if not intermediary_companies or any(c is None or not isinstance(c, str) for c in intermediary_companies):
        print("Некорректные данные компаний, подставляем заглушки.")
        intermediary_companies = [f"Company {i}" for i in range(len(transactions))]


    # Проверка на соответствие длины списков
    if len(transactions) != len(intermediary_companies):
        print("Несоответствие длин списков транзакций и компаний. Обрезаем до минимальной длины.")
        min_length = min(len(transactions), len(intermediary_companies))
        transactions = transactions[:min_length]
        intermediary_companies = intermediary_companies[:min_length]
    
    # Рассчитываем общий объем транзакций
    total_transactions = sum(transactions)
    
    # Новые списки для обновленных данных
    filtered_companies = []
    filtered_transactions = []
    other_sum = 0

    # Фильтрация компаний по порогу и объединение малых компаний
    for company, transaction in zip(intermediary_companies, transactions):
        share = transaction / total_transactions
        if share >= threshold:  # Если доля компании больше порога, оставляем её
            filtered_companies.append(company)
            filtered_transactions.append(transaction)
        else:  # Иначе добавляем сумму транзакции к "Остальным компаниям"
            other_sum += transaction
    
    # Добавляем категорию "Остальные компании", если есть компании ниже порога
    if other_sum > 0:
        filtered_companies.append("Остальные компании")
        filtered_transactions.append(other_sum)
    
    # Создаем пироговый график с использованием plotly
    pie = go.Figure(
        data=[go.Pie(labels=filtered_companies, values=filtered_transactions, hole=0.3)]
    )
    
    # Добавляем аннотацию с общей суммой транзакций
    pie.update_layout(
        title_text=f"Общая сумма: {total_transactions} ₽",
        title_font_size=18
    )

    return pie.to_dict()
