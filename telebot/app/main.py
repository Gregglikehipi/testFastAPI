from app.bot import bot
import time
from receiver import *
from datetime import datetime


def myFunc(e):
  return e['date']


@bot.message_handler(commands=["start"])
def handle_role_selection(message):
    bot.send_message(message.chat.id, 'Есть 9 команд:\n'
                                      '/start получить список команд\n'
                                      '/add добавить товар в базу API по ID\n'
                                      '/get получить товар из API по ID\n'
                                      '/getAll получить все товары из API по ID\n'
                                      '/delete удалить товар из API по ID\n'
                                      '/minMax найти максимальную и минимальную цену за 6 месяцев\n'
                                      '/average найти разницу в цене товара и стредней по категории\n'
                                      '/countGroup найти количество товара по категориям\n'
                                      '/countAll найти количество всего товара\n'
                                      '/historyPrice найти динамику цены по товару')

@bot.message_handler(commands=["add"])
def add_command(message):
    bot.send_message(message.chat.id, 'Введите ID товара')
    bot.register_next_step_handler(message, write_id_add)

def write_id_add(message):
    api_add(int(message.text))
    bot.send_message(message.chat.id, 'Добавлено')


@bot.message_handler(commands=["get"])
def get_command(message):
    bot.send_message(message.chat.id, 'Введите ID товара')
    bot.register_next_step_handler(message, write_id_get)

def write_id_get(message):
    ans = api_get(int(message.text))
    bot.send_message(message.chat.id, f'Товар\n'
                                      f'ID: {ans["nm_id"]}\n'
                                      f'Имя: {ans["name"]}\n'
                                      f'Бренд: {ans["brand"]}\n'
                                      f'Бренд ID: {ans["brand_id"]}\n'
                                      f'Сайт Бренд ID: {ans["site_brand_id"]}\n'
                                      f'Поставщик ID: {ans["supplier_id"]}\n'
                                      f'Sale: {ans["sale"]}\n'
                                      f'Цена: {ans["price"]}\n'
                                      f'Скидочная цена: {ans["sale_price"]}\n'
                                      f'Рейтинг: {ans["rating"]}\n'
                                      f'Отзывов: {ans["feedbacks"]}\n'
                                      f'Цвет: {ans["colors"]}\n'
                                      f'Количество: {ans["qnt"]}\n'
                                      f'ID категории: {ans["subjectId"]}'
                                    )



@bot.message_handler(commands=["getAll"])
def getAll_command(message):
    bot.send_message(message.chat.id, 'Товары')
    ans = api_get_all()
    print(ans)
    ans = ans["list"]
    for i in ans:
        bot.send_message(message.chat.id, f'Товар: {i}')



@bot.message_handler(commands=["delete"])
def delete_command(message):
    bot.send_message(message.chat.id, 'Введите ID товара')
    bot.register_next_step_handler(message, write_id_delete)

def write_id_delete(message):
    api_delete(int(message.text))
    bot.send_message(message.chat.id, 'Удаленно')


@bot.message_handler(commands=["minMax"])
def statistic_minMax(message):
    bot.send_message(message.chat.id, 'Введите ID товара')
    bot.register_next_step_handler(message, write_statistic_minMax)

def add_months(current_date, months_to_add):
    new_date = datetime(current_date.year + (current_date.month + months_to_add - 1) // 12,
                        (current_date.month + months_to_add - 1) % 12 + 1,
                        current_date.day, current_date.hour, current_date.minute, current_date.second)
    return new_date

def write_statistic_minMax(message):
    ans = api_priceHistory(int(message.text))
    print(ans)
    ans = ans["price"]
    if len(ans) == 0:
        bot.send_message(message.chat.id, 'Динамики цены нет')
    else:
        curr = datetime.today().strftime('%Y-%m-%d')
        curr = datetime.strptime(curr, '%Y-%m-%d')
        min = 99999999999999
        max = 0
        for i in ans:
            if add_months(datetime.utcfromtimestamp(i["date"]), 6) > curr:
                if max < i["price"]:
                    max = i["price"]
                if min > i["price"]:
                    min = i["price"]
        bot.send_message(message.chat.id, f'Мин: {min}, Макс: {max}')


@bot.message_handler(commands=["average"])
def statistic_average(message):
    bot.send_message(message.chat.id, 'Введите ID товара')
    bot.register_next_step_handler(message, write_statistic_average)

def write_statistic_average(message):
    ans = api_average(int(message.text))
    bot.send_message(message.chat.id, f'Цена на этот товар: {ans["price"]}\n'
                                      f'Средняя цена по категории: {ans["avgPrice"]}')


@bot.message_handler(commands=["historyPrice"])
def statistic_priceHistory(message):
    bot.send_message(message.chat.id, 'Введите ID товара')
    bot.register_next_step_handler(message, write_statistic_priceHistory)


def write_statistic_priceHistory(message):
    ans = api_priceHistory(int(message.text))
    bot.send_message(message.chat.id, 'Динамика цены\n')
    print(ans)
    ans = ans["price"]
    ans.sort(key=myFunc)
    print(datetime.utcfromtimestamp(ans[0]["date"]).strftime('%Y-%m-%d'))
    for i in ans:
        bot.send_message(message.chat.id, f'Дата: {datetime.utcfromtimestamp(i["date"])} Цена: {i["price"]}')


@bot.message_handler(commands=["countGroup"])
def statistic_countGroup(message):
    bot.send_message(message.chat.id, 'Введите ID группы')
    bot.register_next_step_handler(message, write_statistic_countGroup)

def write_statistic_countGroup(message):
    ans = api_countGroup(int(message.text))
    bot.send_message(message.chat.id, f'Количество товара в категории {ans["ans"]}')


@bot.message_handler(commands=["countAll"])
def statistic_countAll(message):
    ans = api_countAll()
    bot.send_message(message.chat.id, f'Количество всего товара {ans["ans"]}')


while True:
    try:
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(5)