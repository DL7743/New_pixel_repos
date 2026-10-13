
{
    "next_user_id": 3,
    "next_order_id": 4,
    "users": [
        {
            "id": 1,
            "name": "Алия",
            "email": "aliya@example.com"
        },
        {
            "id": 2,
            "name": "Марк",
            "email": "mark@example.com"
        }
    ],
    "orders": [
        {
            "id": 1,
            "user_id": 1,
            "item": "Стикерпак Космос",
            "price": 1200,
            "status": "paid"
        },
        {
            "id": 2,
            "user_id": 1,
            "item": "Постер Pixel City",
            "price": 3500,
            "status": "new"
        },
        {
            "id": 3,
            "user_id": 2,
            "item": "Стикерпак Котики",
            "price": 1500,
            "status": "paid"
        }
    ]
}
# Начальные данные
# Один магазин продаёт стикерпаки и постеры. Один пользователь может создать несколько заказов. 
# Пользователь хранится один раз, а заказ содержит его номер. 
# Образец разделён на части только для чтения: весь JSON нужно собрать в один shop.json.
# 01 Первый запуск
# 1. Создайте app.py и shop.json. Перенесите в JSON образец из раздела «Начальные данные».
# 2. Напишите load_db и save_db. Без файла возвращайте пустую структуру. При повреждённом JSON покажите ошибку и не перезаписывайте файл.
import json
FILE_NAME = "shop.json"
def empty_db():
    return {"next_user_id": 1,
            "next_order_id": 1,
            "users": [], "orders": []}
def load_db():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return empty_db()
      
def save_db(data):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4) 

# 02 Что уже хранится
# 1. Загрузите базу и выведите количество пользователей и заказов.
# 2. Выведите ID и названия всех заказов. Не меняйте файл.
data = load_db()
print(f"Количество пользователей: {len(data['users'])}")
print(f"Количество заказов: {len(data['orders'])}")
for order in data['orders']:    
    print(f"ID: {order['id']}, Название: {order['item']}")

# 03 Проверка номеров
# 1. Напишите has_unique_ids(records), которая возвращает True при отсутствии повторных id.
# 2. Отдельно проверьте users и orders. Одинаковые номера в разных списках разрешены.
def has_unique_ids(records):
    seen_ids = []
    for record in records:  
        if record["id"] in seen_ids:
            return False
        seen_ids.append(record["id"])
    return True
#has_unique_ids()
# 04 Карточка покупателя
# 1. Напишите find_user(data, user_id). Верните найденный словарь или None.
# 2. Проверьте существующий и неизвестный номер.
def find_user(data, user_id):
    for user in data["users"]:
        if user["id"] == user_id:
            return user
    return None

# 05 Регистрация без дублей
# 1. Напишите add_user(data, name, email). Имя и email не должны быть пустыми.
# 2. Уберите крайние пробелы. Email сравнивайте в нижнем регистре. Не допускайте повторного email.
# 3. Выдайте id из next_user_id, увеличьте счётчик. При отказе верните None.
def add_user(data, name, email):
    name = name.strip()
    email = email.strip().lower()

    if not name or not email:
        return None
    
    for user in data["users"]:
        if user["email"].lower() == email:
            return None

    user ={
        "id": data["next_user_id"],
        "name": name,
        "email": email
    }

    data["users"].append(user)
    data["next_user_id"] += 1
    return user

# 06 Заказ только для существующего человека
# 1. Напишите add_order(data, user_id, item, price).
# 2. При неизвестном пользователе, пустом товаре или цене не выше нуля верните None.
# 3. Создайте заказ со статусом new и уникальным id.
def add_order(data, user_id, item, price):
    if find_user(data, user_id) is None:
        return None
    item = item.strip()
    if not item or price <= 0:
        return None

    order = {
        "id": data["next_order_id"],
        "user_id": user_id,
        "item": item,
        "price": price,
        "status": "new"
    }

    data["orders"].append(order)
    data["next_order_id"] += 1
    return order

# 07 Понятный журнал заказов
# 1. Напишите get_order_rows(data), возвращающую новый список с id, name, item, price и status.
# 2. Получайте имя через user_id. В самих заказах не храните копию имени.
# 3. Для повреждённой связи показывайте «Пользователь не найден».
def get_order_rows(data):
    rows =[]
    for order in data["orders"]:
        user = find_user(data,order["user_id"])
        name = "Пользователь не найден"
        if user is not None:
            name = user["name"]
        rows.append(
           { 
            "id": order["id"], "name": name, 
            "item": order["item"], "price": order["price"],
            "status": order["status"]
            }
        )
    return rows
         
# 08 История одного покупателя
# 1. Напишите get_user_orders(data, user_id).
# 2. Верните все заказы этого человека новым списком. Если заказов нет, верните [].
def get_user_orders(data, user_id):
    result =[]
    for order in data["orders"]:
        if order["user_id"] == user_id:
            result.append(order)
    return result

# 09 Оплата без повторного списания
# 1. Создайте find_order и pay_order. Оплатить можно только заказ со статусом new.
# 2. При успехе установите paid и верните True, иначе False.
# 3. Не добавляйте сумму повторно при повторном вызове.

def find_order(data,order_id):
    for order in data["orders"]:
        if order["id"] == order_id:
            return order
    return None

def pay_order(data, order_id):
    order = find_order(data, order_id)
    if order is None or order["status"] != "new":
        return False
    order["status"] = "paid"
    return True


# 10 Отмена с сохранением истории
# 1. Создайте cancel_order. Отменять можно только new.
# 2. Установите cancelled, не удаляя запись. Верните результат True или False.

# находим заказ и делаем проверку существует ли заказ, 
# находим заказ со статусом new и меняем на cancelled
def cancel_order(data, order_id):
    order = find_order(data, order_id)
    if order is None or order["status"] != "new":
        return False
    order["status"] = "cancelled"
    return True

# 11 Удаление без потери связи
# 1. Создайте delete_user. Удаление разрешено только человеку без заказов.
# 2. Учитывайте заказы любого статуса. Счётчик ID не уменьшайте.
# находим покупателя и проводим проверку на его наличие, 
# потом проходим по циклу заказов и проверяем есть ли заказы у покупателя,
# если нет заказов, то затем удаляем его
def delete_user(data, user_id):
    user = find_user(data, user_id)
    if not user:
        return False
    for order in data["orders"]:
            if order["user_id"] == user_id:
                return False
    data["users"].remove(user)
    return True               

# 12 Поиск товара
# 1. Создайте search_orders(data, text). Найдите заказы по части названия без учёта регистра.
# 2. Верните новый список и не удаляйте элементы из базы. Пустой запрос возвращает все заказы.
# проверяем есть ли текст, усли текста нет то возвращаем весь список заказов от 0 элемента до конца
# череp срез [:]
# переводим текст в нижний регистр, затем создаем новый список куда будем помещать заказы с текстом
# проходим по циклу заказов. создаем переменную где переводим в нижни регистр текст в описание item 
# если текст найден в описании item добавляем в список
def search_orders(data, text):
    if not text:
        return data["orders"][:]
    search_text = text.lower()
    found_orders = []
    for order in data["orders"]:
        item_name = order["item"].lower()
        if search_text in item_name:
            found_orders.append(order)  
    return found_orders

# 13 Дорогие заказы сначала
# 1. Создайте sort_orders. Верните заказы по убыванию price через sorted и lambda.
# 2. Порядок исходного списка должен остаться прежним.
def sort_orders(data):
    result = sorted(data["orders"], key = lambda order: order["price"], reverse = True )
    return result
# 14 Сколько потратил каждый человек
# 1. Создайте get_paid_totals. Верните словарь: ключ — user_id, значение — сумма оплаченных заказов.
# 2. Статусы new и cancelled не учитывайте. Для одного пользователя сложите все его paid.
# создаем новый словарь для оплаченных заказов, проходим по циклу заказов и проверяем
# заказы со статусом paid и если user_id совпадает с заказом по этому покупателю и вытаскиввем стоимость
# и делаем проверку есть ли id покупателя в этом словаре, затем складываем все оплаченные заказы 
# конкретного покупателя
def get_paid_totals(data):
    totals = {}
    for order in data["orders"]:
        if order["status"] == "paid":
            user_id = order["user_id"]
            price = order["price"]
            if user_id not in totals:
                totals[user_id] = 0

            totals[user_id] += price
            
    return totals


# 15 Рабочий PixelShop
# 1. Создайте export_report: запишите в report.txt имя каждого пользователя и его сумму paid, включая ноль.
# 2. Соберите меню: журнал заказов, новый пользователь, новый заказ, оплата, отмена, отчёт и выход.
# 3. Сохраняйте после успешного изменения, защищайте ввод чисел. Добавьте README с инструкцией запуска.
# 4. Загрузите app.py, shop.json и README в уже настроенный Git репозиторий командами status, add, commit, push.
def main():
    try:
        data = load_db()
    except json.JSONDecodeError:
        print("JSON поврежден или пустой, исправьте файл shop.json")
        return
    
    while True:
        print("\n1 Заказы | 2 Пользователь | 3 Заказ | 4 Оплата")
        choice = input("Действие: ")

        if choice == "1":
            for row in get_order_rows(data):
                print(row["id"],row["name"], row["item"], row["status"])
        elif choice == "2":
            name = input("Имя: ")
            email = input("Почта: ")
            changed = add_user(data,name,email) is not None
main()