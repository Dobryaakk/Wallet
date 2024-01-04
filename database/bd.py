import sqlite3
import psycopg2


class History:
    def __init__(self, host, user, password, db_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        try:
            with self.conn:
                self.cur.execute("""
                    CREATE TABLE IF NOT EXISTS add_history(
                        user_id SERIAL,
                        amount INTEGER,
                        date DATE DEFAULT CURRENT_DATE
                    )
                """)
                self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS subtract_history (
                            user_id SERIAL,
                            amount INTEGER,
                            date DATE DEFAULT CURRENT_DATE                   
                        )
                    """)
        except Exception as ex:
            print(ex)

    def get_sum(self, user_id, operation_type):
        table_name = f"{operation_type}_history"
        with self.conn:
            self.cur.execute(f"SELECT SUM(amount) FROM {table_name} WHERE user_id = %s", (user_id,))
            result = self.cur.fetchone()
            return result[0] if result else 0

    def get_average(self, user_id, operation_type):
        table_name = f"{operation_type}_history"
        with self.conn:
            self.cur.execute(f"SELECT AVG(amount) FROM {table_name} WHERE user_id = %s", (user_id,))
            result = self.cur.fetchone()
            return int(result[0]) if (result and result[0] is not None) else 0

    def add_money_history(self, user_id, amount):
        with self.conn:
            self.cur.execute("""
                INSERT INTO add_history (user_id, amount) VALUES (%s, %s)
            """, (user_id, amount))
            last_row_id = self.cur.lastrowid
            return last_row_id

    def get_add_history_by_id(self, user_id):
        with self.conn:
            self.cur.execute("""
                       SELECT TO_CHAR(date, 'YYYYMMDD') as formatted_date, amount 
                       FROM add_history 
                       WHERE user_id = %s
                   """, (user_id,))
            results = self.cur.fetchall()
            history_entries = []
            for result in results:
                formatted_date = int(result[0])
                history_entries.append({'timestamp': formatted_date, 'amount': result[1]})

            return history_entries

    def subtract_money(self, user_id, amount):
        with self.conn:
            self.cur.execute("""
                INSERT INTO subtract_history (user_id, amount) VALUES (%s, %s)
            """, (user_id, amount))
            last_row_id = self.cur.lastrowid
            return last_row_id

    def get_subtract_history_by_id(self, user_id):
        with self.conn:
            self.cur.execute("""
                       SELECT TO_CHAR(date, 'YYYYMMDD') as formatted_date, amount 
                       FROM subtract_history 
                       WHERE user_id = %s
            """, (user_id,))
            results = self.cur.fetchall()
            history_entries = []
            for result in results:
                formatted_date = int(result[0])
                history_entries.append({'timestamp': formatted_date, 'amount': result[1]})

            return history_entries

    def create_history_file(self, user_id):
        history_entries = self.get_subtract_history_by_id(user_id)
        if history_entries:
            with open(f'history_{user_id}.txt', 'w') as file:
                for entry in history_entries:
                    file.write(f"Дата: {entry['timestamp']}, Витрачено: {entry['amount']}\n\n")
            return f'history_{user_id}.txt'
        else:
            return None


class Balance:

    def __init__(self, host, user, password, db_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                 CREATE TABLE IF NOT EXISTS balance (
                     user_id INTEGER,
                     user_money INTEGER,
                     PRIMARY KEY (user_id)
                 )
             """)

    def add_money(self, user_id, amount):
        with self.conn:
            self.cur.execute("SELECT user_id FROM balance WHERE user_id = %s", (user_id,))
            existing_user = self.cur.fetchone()

            if existing_user:
                self.cur.execute("""
                    UPDATE balance SET user_money = user_money + %s WHERE user_id = %s
                """, (amount, user_id))
            else:
                self.cur.execute("""
                    INSERT INTO balance (user_id, user_money) VALUES (%s, %s)
                """, (user_id, amount))

    def minus_money(self, user_id, amount):
        with self.conn:
            self.cur.execute("SELECT user_id FROM balance WHERE user_id = %s", (user_id,))
            existing_user = self.cur.fetchone()

            if existing_user:
                self.cur.execute("""
                      UPDATE balance SET user_money = user_money - %s WHERE user_id = %s
                  """, (amount, user_id))
            else:
                self.cur.execute("""
                      INSERT INTO balance (user_id, user_money) VALUES (%s, %s)
                  """, (user_id, amount))

    def check_money(self, user_id):
        print(f"You`r user ID = {user_id}")
        self.cur.execute("SELECT user_money FROM balance WHERE user_id = %s", (user_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return '0'


class Database_curr:
    def __init__(self, host, user, password, db_name):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                user_name VARCHAR(255),
                pred INTEGER DEFAULT 3
            )
            """)

    def insert_or_update_data(self, user_id, user_name, pred_value):
        with self.conn:
            self.cur.execute("""
            SELECT user_id FROM users WHERE user_id = %s
            """, (user_id,))
            existing_user = self.cur.fetchone()

            if existing_user:
                self.cur.execute("""
                UPDATE users SET pred = %s WHERE user_id = %s
                """, (pred_value, user_id))
                return True
            else:
                self.cur.execute("""
                INSERT INTO users (user_id, user_name, pred)
                VALUES (%s, %s, %s)
                """, (user_id, user_name, pred_value))
                return False

    def get_default_pred_value(self):
        with self.conn:
            self.cur.execute("""
            SELECT pred FROM users LIMIT 1
            """)
            row = self.cur.fetchone()
            if row:
                return row[0]
            else:
                return 1
