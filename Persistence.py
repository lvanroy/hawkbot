import psycopg2


class Persistence:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user="hawk",
                                               password="hawk",
                                               database="shadowhawks")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def close_connection(self):
        self.connection.close()

    def check_if_user_exists(self, user):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE id=\'{}\'".format(user_id))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def check_if_user_exists_in_gear(self, user):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Gear WHERE id=\'{}\'".format(user_id))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def check_if_toon_exists(self, user, toon):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Toons WHERE id = '{}' and name = '{}'".format(user_id, toon))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_user(self, user):
        user_id = user.id
        user_name = user.name
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Users(id, username) VALUES ({}, $STR${}$STR$)".format(user_id, user_name))
        self.connection.commit()

    def add_gear(self, user):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Gear(id, dp, ap, aap) VALUES ({}, 0, 0, 0)".format(user_id))
        self.connection.commit()

    def add_toon(self, user, toon, toon_class):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Toons(id, name, class) VALUES ({}, $STR${}$STR$, {})"
                       .format(user_id, toon, toon_class))
        self.connection.commit()

    def set_dp(self, user, value):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Gear SET dp = \'{}\' WHERE id=\'{}\'".format(value, user_id))
        self.connection.commit()

    def set_ap(self, user, value):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Gear SET ap = \'{}\' WHERE id=\'{}\'".format(value, user_id))
        self.connection.commit()

    def set_aap(self, user, value):
        user_id = user.id
        cursor = self.connection.cursor()
        cursor.execute("UPDATE Gear SET aap = \'{}\' WHERE id=\'{}\'".format(value, user_id))
        self.connection.commit()

    @staticmethod
    def escape_special_characters(text):
        return text.translate(str.maketrans({"(": r"\\(",
                                             ")": r"\\)"}))
