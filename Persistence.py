import psycopg2


class Persistence:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user="Hawk",
                                               password="hawk",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="shadowhawks")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        self.windows_tables = {
            "Users": "public.Users",
            "Gear": "public.Gear",
            "Toons": "public.Toons"
        }

    def close_connection(self):
        self.connection.close()

    # ~~~~~~~~~~~~~~~~~~~~ Users ~~~~~~~~~~~~~~~~~~~~

    def check_if_user_exists(self, user):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"Users\" WHERE id=\'{}\'".format(user_id))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_user(self, user):
        user_id = user.id
        user_name = user.name
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"Users\"(id, username) VALUES ({}, $STR${}$STR$)".format(user_id, user_name))
        self.connection.commit()

    # ~~~~~~~~~~~~~~~~~~~~ Gear ~~~~~~~~~~~~~~~~~~~~

    def check_if_toon_exists_in_gear(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"Gear\" WHERE toon=\'{}\'".format(toon))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_gear(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"Gear\"(toon, dp, ap, aap) VALUES ('{}', 0, 0, 0)".format(toon))
        self.connection.commit()

    def set_dp(self, toon, value):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"Gear\" SET dp = \'{}\' WHERE toon=\'{}\'".format(value, toon))
        self.connection.commit()

    def get_dp(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT dp FROM \"Gear\" WHERE toon='{}'".format(toon))
        dp = cursor.fetchone()
        return dp[0]

    def set_ap(self, toon, value):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"Gear\" SET ap = \'{}\' WHERE toon=\'{}\'".format(value, toon))
        self.connection.commit()

    def get_ap(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT ap FROM \"Gear\" WHERE toon='{}'".format(toon))
        ap = cursor.fetchone()
        print(ap)
        return ap[0]

    def set_aap(self, toon, value):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"Gear\" SET aap = \'{}\' WHERE toon=\'{}\'".format(value, toon))
        self.connection.commit()

    def get_aap(self, toon):
        cursor = self.connection.fetchone()
        cursor.execute("SELECT aap FROM \"Gear\" WHERE toon='{}'".format(toon))
        aap = cursor.fetone()
        return aap[0]

    # ~~~~~~~~~~~~~~~~~~~~ Toons ~~~~~~~~~~~~~~~~~~~~

    def check_if_toon_exists(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"Toons\" WHERE name = '{}'".format(toon))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_toon(self, user, toon, toon_class):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"Toons\"(id, name, class) VALUES ({}, $STR${}$STR$, $STR${}$STR$)"
                       .format(user_id, toon, toon_class))
        self.connection.commit()

    def remove_toon(self, user, toon):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("DROP ROW FROM \"Toons\" WHERE id='{}' and name='{}'".format(user_id, toon))

    def get_toons(self, user):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"Toons\" WHERE id='{}'".format(user_id))
        result = cursor.fetchall()
        return result

    # ~~~~~~~~~~~~~~~~~~~~ History ~~~~~~~~~~~~~~~~~~~~

    def add_event(self, toon, stat, quantity):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"History\"(toon, stat, date, amount) VALUES ('{}', '{}', now(), {})"
                       .format(toon, stat, quantity))
        self.connection.commit()

    def get_toon_history(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"History\" WHERE toon='{}'".format(toon))
        result = cursor.fetchall()
        return result

    # ~~~~~~~~~~~~~~~~~~~~ General ~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def escape_special_characters(text):
        return text.translate(str.maketrans({"(": r"\\(",
                                             ")": r"\\)"}))
