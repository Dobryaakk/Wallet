start_yes = ("<b>Привіт 👋🏼</b>\n\nЯ бот, створений для обліку твоїх фінансів та утворення статистики, "
             "щоб зробити управління грошима більш зручним. \n\n"
             "<i>Змінити валюту можна за допомогою команди <b>/change</b>.</i>")

start_not = ("Зробіть управління своїми грошима легкою та цікавою справою завдяки мені 🤖\n\n<i>Змінити валюту можна"
             "за допомогою команди <b>/change</b>.</i>")


# async def parser(amount, from_currency):
#     converted_results = []
#     for target_currency in currency_:
#         link = f'https://finance.rambler.ru/calculators/converter/{amount}-{from_currency}-{target_currency}/'
#         response = requests.get(link, headers=headers).text
#         soup = BeautifulSoup(response, 'lxml')
#         converted_amount = soup.find('div', class_='_2TC8G commercial-branding').findAll('span', class_='_1wjU3')[
#             1].text
#         converted_results.append(f'{target_currency}: {converted_amount}')
#
