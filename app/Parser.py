import requests
import json

def get_cards(num):
    link = f'https://basket-10.wbbasket.ru/vol{num // (10**5)}/part{num // (10**3)}/{num}/info/ru/card.json'
    res = requests.get(link)
    response = json.loads(res.text)
    cards = {}
    cards['colors'] = response['colors']
    return cards


def get_detail(num):
    link = f'https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&nm={num}'
    res = requests.get(link)
    response = json.loads(res.text)
    data = response['data']['products'][0]
    details = {}
    details['nm_id'] = data['id']
    details['name'] = data['name']
    details['brand'] = data['brand']
    details['brand_id'] = data['brandId']
    details['site_brand_id'] = data['siteBrandId']
    details['subjectId'] = data['subjectId']
    details['supplier_id'] = data['supplierId']
    details['sale'] = data['sale']
    details['price'] = data['priceU']
    details['sale_price'] = data['salePriceU']
    details['rating'] = data['rating']
    details['feedbacks'] = data['feedbacks']
    color = data['colors']
    if len(color) != 0:
        color = color[0]['name']
    else:
        color = None
    details['colors'] = color
    return details


def get_history_price(num):
    link = f'https://basket-10.wbbasket.ru/vol{num // (10**5)}/part{num // (10**3)}/{num}/info/price-history.json'
    res = requests.get(link)
    if res.status_code == 404:
        print("not found")
        return []
    response = json.loads(res.text)
    prices = []
    for price in response:
        prices.append({"id": num,
                       "price": price['price']['RUB'],
                       "date": price['dt']})
    return prices


def get_quantity(num):
    link = f'https://product-order-qnt.wildberries.ru/v2/by-nm/?nm={num}'
    res = requests.get(link)
    response = json.loads(res.text)
    return response
