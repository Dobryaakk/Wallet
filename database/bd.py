import sqlite3


class History:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        try:
            with self.conn:
                self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS add_history(
                            user_id serial,
                            amount ser,
                            date DATE DEFAULT (DATE('now', 'localtime'))
                        )
                    """)
                self.cur.execute("""
                        CREATE TABLE IF NOT EXISTS subtract_history (
                            user_id INTEGER,
                            amount INTEGER,
                            date DATE DEFAULT (DATE('now', 'localtime'))                   
                        )
                    """)
        except Exception as ex:
            print(ex)
    def get_sum(self, user_id, operation_type):
        table_name = f"{operation_type}_history"
        with self.conn:
            self.cur.execute(f"SELECT SUM(amount) FROM {table_name} WHERE user_id = ?", (user_id,))
            result = self.cur.fetchone()
            return result[0] if result else 0

    def get_average(self, user_id, operation_type):
        table_name = f"{operation_type}_history"
        with self.conn:
            self.cur.execute(f"SELECT AVG(amount) FROM {table_name} WHERE user_id = ?", (user_id,))
            result = self.cur.fetchone()
            return int(result[0]) if result else 0

    def add_money_history(self, user_id, amount):
        with self.conn:
            self.cur.execute("""
                INSERT INTO add_history (user_id, amount) VALUES (?, ?)
            """, (user_id, amount))
            last_row_id = self.cur.lastrowid
            return last_row_id

    def get_add_history_by_id(self, user_id):
        with self.conn:
            self.cur.execute("""
                       SELECT strftime('%Y%m%d', date) as formatted_date, amount 
                       FROM add_history 
                       WHERE user_id = ?
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
                INSERT INTO subtract_history (user_id, amount) VALUES (?, ?)
            """, (user_id, amount))
            last_row_id = self.cur.lastrowid
            return last_row_id

    def get_subtract_history_by_id(self, user_id):
        with self.conn:
            self.cur.execute("""
                SELECT strftime('%Y%m%d', date) as formatted_date, amount 
                FROM subtract_history 
                WHERE user_id = ?
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

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
                 CREATE TABLE IF NOT EXISTS money (
                     user_id INTEGER,
                     user_money INTEGER,
                     PRIMARY KEY (user_id)
                 )
             """)

    def add_money(self, user_id, amount):
        with self.conn:
            self.cur.execute("SELECT user_id FROM money WHERE user_id = ?", (user_id,))
            existing_user = self.cur.fetchone()

            if existing_user:
                self.cur.execute("""
                    UPDATE money SET user_money = user_money + ? WHERE user_id = ?
                """, (amount, user_id))
            else:
                self.cur.execute("""
                    INSERT INTO money (user_id, user_money) VALUES (?, ?)
                """, (user_id, amount))

    def minuse_money(self, user_id, amount):
        with self.conn:
            self.cur.execute("SELECT user_id FROM money WHERE user_id = ?", (user_id,))
            existing_user = self.cur.fetchone()

            if existing_user:
                self.cur.execute("""
                      UPDATE money SET user_money = user_money - ? WHERE user_id = ?
                  """, (amount, user_id))
            else:
                self.cur.execute("""
                      INSERT INTO money (user_id, user_money) VALUES (?, ?)
                  """, (user_id, amount))

    def check_money(self, user_id):
        print(f"You`r user ID = {user_id}")
        self.cur.execute("SELECT user_money FROM money WHERE user_id=?", (user_id,))
        row = self.cur.fetchone()
        if row:
            return row[0]
        else:
            return '0'


class Database_pred:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        with self.conn:
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER,
                user_name TEXT,
                pred INTEGER DEFAULT 3
            )
            """)

    def insert_or_update_data(self, user_id, user_name, pred_value):
        with self.conn:
            self.cur.execute("""
            SELECT user_id FROM users WHERE user_id = ?
            """, (user_id,))
            existing_user = self.cur.fetchone()

            if existing_user:
                self.cur.execute("""
                UPDATE users SET pred = ? WHERE user_id = ?
                """, (pred_value, user_id))
                return True
            else:
                self.cur.execute("""
                INSERT INTO users (user_id, user_name, pred)
                VALUES (?, ?, ?)
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
