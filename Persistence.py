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

    def add_toon(self, toon, family, toon_class, planner_url):
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO \"toons\"(name, family, class, url, level, xp) "
                           "VALUES (\'{}\', \'{}\', \'{}\', \'{}\', {}, \'{}\')"
                           .format(toon, family, toon_class, planner_url, 0, 0))
        except errors.lookup(FOREIGN_KEY_VIOLATION):
            raise
        self.connection.commit()

    def remove_toon(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM \"toons\" WHERE name='{}'".format(toon))
        self.connection.commit()

    def get_toons(self, family):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, family, class, level, xp FROM \"toons\" WHERE family='{}'".format(family))
        result = cursor.fetchall()
        return result

    def set_toon_level(self, toon ,level, xp_percentage):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"toons\" set level={}, xp={} where name = '{}'"
                       .format(level, xp_percentage, toon))
        self.connection.commit()

    def get_toon_level(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT level, xp from \"toons\" where name = '{}'".format(toon))
        result = cursor.fetchone()
        return result

    def set_toon_url(self, toon, url):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"toons\" set url={} where name = '{}'"
                       .format(url, toon))

    # ~~~~~~~~~~~~~~~~~~~~ Gear ~~~~~~~~~~~~~~~~~~~~

    def check_if_toon_exists_in_gear(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"gear\" WHERE toon=\'{}\'".format(toon))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_toon_to_gear(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"gear\""
                       "(toon, dp, ap, aap, hap, bap, baap, dr, drr, hdr, eva, heva, hp, acc, acrit, da, dm) "
                       "VALUES ('{}', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)".format(toon))
        self.connection.commit()

    def set_gear_stats(self, toon, stats):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"gear\" SET " +
                       "{} = \'{}\', ".format("dp", stats["DP"]) +
                       "{} = \'{}\', ".format("ap", stats["AP"]) +
                       "{} = \'{}\', ".format("aap", stats["AAP"]) +
                       "{} = \'{}\', ".format("hap", stats["HAP"]) +
                       "{} = \'{}\', ".format("bap", stats["BAP"]) +
                       "{} = \'{}\', ".format("baap", stats["BAAP"]) +
                       "{} = \'{}\', ".format("dr", stats["DR"]) +
                       "{} = \'{}\', ".format("drr", stats["DRR"]) +
                       "{} = \'{}\', ".format("hdr", stats["HDR"]) +
                       "{} = \'{}\', ".format("eva", stats["E"]) +
                       "{} = \'{}\', ".format("heva", stats["HE"]) +
                       "{} = \'{}\', ".format("hp", stats["MHP"]) +
                       "{} = \'{}\', ".format("acc", stats["A"]) +
                       "{} = \'{}\', ".format("acrit", stats["ACHD"]) +
                       "{} = \'{}\', ".format("da", stats["EDAS"]) +
                       "{} = \'{}\' ".format("dm", stats["EAPAM"]) +
                       "WHERE toon=\'{}\'".format(toon))
        self.connection.commit()

    def set_gear_value(self, toon, value, variable):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"gear\" SET {} = \'{}\' WHERE toon=\'{}\'".format(variable, value, toon))
        self.connection.commit()

    def get_gear_value(self, toon, variable):
        cursor = self.connection.cursor()
        cursor.execute("SELECT {} FROM \"gear\" WHERE toon='{}'".format(variable, toon))
        dp = cursor.fetchone()
        return dp[0]

    # ~~~~~~~~~~~~~~~~~~~~ Skills ~~~~~~~~~~~~~~~~~~~~
    def check_if_toon_exists_in_skills(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM \"skills\" WHERE toon=\'{}\'".format(toon))
        entry = cursor.fetchone()
        if not entry:
            return False
        return True

    def add_toon_to_skills(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"skills\"(toon, gathering, fishing, hunting, cooking, alchemy, " +
                       "processing, training, trade, farming, sailing)" +
                       "VALUES ('{}', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)".format(toon))
        self.connection.commit()

    def set_skill_value(self, toon, value, skill):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE \"skills\" SET {} = '{}' WHERE toon = '{}'".format(skill, value, toon))
        self.connection.commit()

    def get_skill_value(self, toon, skill):
        cursor = self.connection.cursor()
        cursor.execute("SELECT {} FROM \"skills\" WHERE toon='{}'".format(skill, toon))
        value = cursor.fetchone()
        return value[0]

    def get_skills_for_toon(self, toon):
        cursor = self.connection.cursor()
        cursor.execute("SELECT gathering, fishing, hunting, cooking, alchemy, processing, training, " \
                       "trade, farming, sailing FROM \"skills\" where toon = '{}'".format(toon))
        result = cursor.fetchone()
        return result

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

    # ~~~~~~~~~~~~~~~~~~~~ News ~~~~~~~~~~~~~~~~~~~~
    def see_if_news_exists(self, title, url):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from \"news\" WHERE title = E'{}' AND  url = '{}'".format(title, url))
        result = cursor.fetchone()
        if not result:
            return False
        return True

    def add_news(self, title, url):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"news\" (title, url) VALUES (E'{}', '{}')".format(title, url))
        self.connection.commit()

    # ~~~~~~~~~~~~~~~~~~~~ Updates ~~~~~~~~~~~~~~~~~~~~
    def see_if_update_exists(self, title, url):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from \"updates\" WHERE title = E'{}'AND  url = '{}'".format(title, url))
        result = cursor.fetchone()
        if not result:
            return False
        return True

    def add_update(self, title, url):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"updates\" (title, url) VALUES (E'{}', '{}')".format(title, url))
        self.connection.commit()

    # ~~~~~~~~~~~~~~~~~~~~ Activity ~~~~~~~~~~~~~~~~~~~~
    def see_if_activity_exists(self, family):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from \"activity\" WHERE family = E'{}'".format(family))
        result = cursor.fetchone()
        if not result:
            return False
        return True

    def add_activity(self, family, activity):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO \"activity\" (family, activity, gained) VALUES (E'{}', {}, 0)"
                       .format(family, activity))
        self.connection.commit()

    def register_renewal(self, family, current_activity):
        cursor = self.connection.cursor()
        cursor.execute("SELECT activity, gained from \"activity\" WHERE family = E'{}'".format(family))
        result = cursor.fetchone()
        cursor.execute("UPDATE \"activity\" set activity = {}, gained = {} WHERE family = E'{}'"
                       .format(current_activity, result[1] + current_activity-result[0], family))
        self.connection.commit()

    def get_weekly_activities(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT family, gained from \"activity\"")
        result = cursor.fetchall()
        cursor.execute("UPDATE \"activity\" set gained = 0")
        self.connection.commit()

        return result

    # ~~~~~~~~~~~~~~~~~~~~ General ~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def escape_special_characters(text):
        return text.translate(str.maketrans({"(": r"\\(",
                                             ")": r"\\)"}))
