from sqlalchemy import create_engine, text

class DBHelper:
    def __init__(self):
        dbname = f"postgresql+psycopg2://postgres:123@postgres:5432/postgres"
        engine = create_engine(dbname)
        self.conn = engine.connect()
        self.create_table()

    def create_table(self):
        com = text(f"CREATE TABLE IF NOT EXISTS item (id int PRIMARY KEY,"
                   f"name varchar(50),"
                   f"brand varchar(50),"
                   f"brand_id int,site_"
                   f"brand_id int,"
                   f"supplier_id int,"
                   f"sale int,"
                   f"price int,"
                   f"sale_price int,"
                   f"rating int,"
                   f"feedbacks int,"
                   f"colors varchar(50),"
                   f"qnt int,"
                   f"subjectId int);")
        self.conn.execute(com)
        com = text(f"CREATE TABLE IF NOT EXISTS price (id int,"
                   f"price int,"
                   f"date int);")
        self.conn.execute(com)
        self.conn.commit()



    def qnt_group_items(self, num):
        com = text(f"SELECT SUM(qnt) FROM item WHERE subjectId = {num}")
        result = self.conn.execute(com)
        ans = 0
        for a in result:
            ans = a[0]
        return ans

    def qnt_all_items(self):
        com = text(f"SELECT SUM(qnt) FROM item")
        result = self.conn.execute(com)
        ans = 0
        for a in result:
            ans = a[0]
        return ans

    def get_avg_price(self, num):
        com = text(f"SELECT AVG(price) FROM item WHERE subjectId = {num}")
        result = self.conn.execute(com)
        ans = 0
        for a in result:
            ans = a[0]
        print(ans)
        return ans

    def add_item(self, item):
        com = text(f"INSERT INTO item (id, name, brand, brand_id, site_brand_id, supplier_id, "
                   f"sale, price, sale_price, rating, feedbacks, colors, qnt, subjectId) "
                   f"VALUES ({item['nm_id']}, '{item['name']}', '{item['brand']}', {item['brand_id']}, "
                   f"{item['site_brand_id']}, {item['supplier_id']}, {item['sale']}, {item['price']}, {item['sale_price']}, "
                   f"{item['rating']}, {item['feedbacks']}, '{item['colors']}', {item['qnt']}, "
                   f"{item['subjectId']})")
        self.conn.execute(com)
        self.conn.commit()

    def get_all_item(self):
        com = text(f"select * from item")
        result = self.conn.execute(com)
        ans = []
        for row in result:
            ans.append(row[0])
        return ans

    def get_item(self, num):
        com = text(f"select * from item where id = {num} ")
        result = self.conn.execute(com)
        ans = []
        for row in result:
            ans.append(row)
        ans = ans[0]
        details = {}
        details['nm_id'] = ans[0]
        details['name'] = ans[1]
        details['brand'] = ans[2]
        details['brand_id'] = ans[3]
        details['site_brand_id'] = ans[4]
        details['supplier_id'] = ans[5]
        details['sale'] = ans[6]
        details['price'] = ans[7]
        details['sale_price'] = ans[8]
        details['rating'] = ans[9]
        details['feedbacks'] = ans[10]
        details['colors'] = ans[11]
        details['qnt'] = ans[12]
        details['subjectId'] = ans[13]
        return details

    def add_price_history(self, prices):
        for price in prices:
            com = text(f"INSERT INTO price (id, price, date) "
                       f"VALUES ({price['id']}, {price['price']}, {price['date']})")
            self.conn.execute(com)
        self.conn.commit()

    def delete_item(self, num):
        com = text(f"DELETE FROM item WHERE id = {num}")
        self.conn.execute(com)
        self.conn.commit()

    def get_price_history(self, num):
        com = text(f"select * from price where id = {num}")
        result = self.conn.execute(com)
        self.conn.commit()
        ans = []
        for row in result:
            ans.append({"price": row[1],
                        "date": row[2]})
        return ans
