import psycopg2
from psycopg2 import errors
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION


class Persistence:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user="hawk",
                                               password="hawk",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="shadowhawks")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def close_connection(self):
        self.connection.close()

    # ~~~~~~~~~~~~~~~~~~~~ Family ~~~~~~~~~~~~~~~~~~~~
    def check_if_family_exists(self, family):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"families\" WHERE family=\'{}\'".format(family))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def check_if_user_owns_family(self, user, family):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"families\" WHERE family=\'{}\' and id=\'{}\'".format(family, user))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_family(self, user, family):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"families\"(id, family) VALUES ({}, $STR${}$STR$)".format(user, family))
        self.connection.commit()

    def remove_family(self, family):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM \"families\" WHERE family=\'{}\'".format(family))
        self.connection.commit()

    # ~~~~~~~~~~~~~~~~~~~~ Toons ~~~~~~~~~~~~~~~~~~~~

    def check_if_toon_exists(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"toons\" WHERE name = '{}'".format(toon))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def check_if_toon_belongs_to_family(self, toon, family):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"toons\" WHERE name = \'{}\' and family = \'{}\'".format(toon, family))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_toon(self, toon, family, toon_class):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO \"toons\"(name, family, class) VALUES (\'{}\', \'{}\', \'{}\')"
                           .format(toon, family, toon_class))
        except errors.lookup(FOREIGN_KEY_VIOLATION):
            raise
        self.connection.commit()

    def remove_toon(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM \"toons\" WHERE name='{}'".format(toon))
        self.connection.commit()

    def get_toons(self, family):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"toons\" WHERE family='{}'".format(family))
        result = cursor.fetchall()
        return result

    # ~~~~~~~~~~~~~~~~~~~~ Gear ~~~~~~~~~~~~~~~~~~~~

    def check_if_toon_exists_in_gear(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"gear\" WHERE toon=\'{}\'".format(toon))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_gear(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"gear\"(toon, dp, ap, aap) VALUES ('{}', 0, 0, 0)".format(toon))
        self.connection.commit()

    def set_dp(self, toon, value):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"gear\" SET dp = \'{}\' WHERE toon=\'{}\'".format(value, toon))
        self.connection.commit()

    def get_dp(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT dp FROM \"gear\" WHERE toon='{}'".format(toon))
        dp = cursor.fetchone()
        return dp[0]

    def set_ap(self, toon, value):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"gear\" SET ap = \'{}\' WHERE toon=\'{}\'".format(value, toon))
        self.connection.commit()

    def get_ap(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT ap FROM \"gear\" WHERE toon='{}'".format(toon))
        ap = cursor.fetchone()
        return ap[0]

    def set_aap(self, toon, value):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"gear\" SET aap = \'{}\' WHERE toon=\'{}\'".format(value, toon))
        self.connection.commit()

    def get_aap(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT aap FROM \"gear\" WHERE toon='{}'".format(toon))
        aap = cursor.fetchone()
        return aap[0]

    # ~~~~~~~~~~~~~~~~~~~~ History ~~~~~~~~~~~~~~~~~~~~

    def add_event(self, toon, stat, quantity):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"history\"(toon, stat, event_date, event_time, amount) "
                       "VALUES ('{}', '{}', now(), now(), {})".format(toon, stat, quantity))
        self.connection.commit()

    def get_toon_history(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT \"event_date\", \"event_time\", \"toon\", \"stat\", \"amount\" \
                       FROM \"history\" WHERE toon='{}'".format(toon) +
                       "ORDER BY \"event_date\" DESC, \"event_time\" DESC")
        result = cursor.fetchmany(10)
        return result

    def get_family_history(self, family):
        cursor = self.connection.cursor()
        cursor.execute("SELECT \"event_date\", \"event_time\", \"toon\", \"stat\", \"amount\" " +
                       "FROM \"history\" WHERE toon IN (SELECT \"name\" FROM \"toons\" " +
                       "WHERE family='{}') ".format(family) +
                       "ORDER BY \"event_date\" DESC, \"event_time\" DESC")
        result = cursor.fetchmany(10)
        return result

    # ~~~~~~~~~~~~~~~~~~~~ General ~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def escape_special_characters(text):
        return text.translate(str.maketrans({"(": r"\\(",
                                             ")": r"\\)"}))
