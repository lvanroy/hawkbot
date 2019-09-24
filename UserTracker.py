import re
import asyncio

from Persistence import Persistence
import psycopg2.errors
from psycopg2.errorcodes import FOREIGN_KEY_VIOLATION

persistence = Persistence()


class UserTracker:
    # ~~~~~~~~~~~~~~~~~~~~ Family ~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def add_family(user, family_name, channel):
        if not persistence.check_if_family_exists(family_name):
            user_id = user.id
            persistence.add_family(user_id, family_name)
            if persistence.check_if_family_exists(family_name):
                asyncio.ensure_future(channel.send("Success: this family was successfully added!"))
            else:
                asyncio.ensure_future(channel.send("Error: something went wrong, please notify the bot owner."))
        else:
            asyncio.ensure_future(channel.send("Error: this family already exists."))

    @staticmethod
    def remove_family(user, family_name, channel):
        if persistence.check_if_family_exists(family_name):
            user_id = user.id
            if persistence.check_if_user_owns_family(user_id, family_name):
                persistence.remove_family(family_name)
                if not persistence.check_if_family_exists(family_name):
                    asyncio.ensure_future(channel.send("Success: this family was successfully removed!"))
                else:
                    asyncio.ensure_future(channel.send("Error: something went wrong, please notify the bot owner."))
            else:
                asyncio.ensure_future(channel.send("Error: this user does not own this family."))
        else:
            asyncio.ensure_future(channel.send("Error: this family does not exist."))

    # ~~~~~~~~~~~~~~~~~~~~ Toons ~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def add_toon(user, toon, toon_family, toon_class, level, xp, channel):
        if not persistence.check_if_toon_exists(toon):
            user_id = user.id
            if persistence.check_if_user_owns_family(user_id, toon_family):
                try:
                    persistence.add_toon(toon, toon_family, toon_class, level, xp)
                except psycopg2.errors.lookup(FOREIGN_KEY_VIOLATION):
                    asyncio.ensure_future(channel.send("something went wrong while adding the toon, make sure you " +
                                                       "have added a family before adding a toon."))
                if persistence.check_if_toon_exists(toon):
                    asyncio.ensure_future(channel.send("Succcess: this toon was successfully added."))
                else:
                    asyncio.ensure_future(channel.send("Error: something went wrong, please notify the bot owner."))
            else:
                asyncio.ensure_future(channel.send("Error: this user does not own the corresponding family or this "
                                                   "family does not exist."))
        else:
            asyncio.ensure_future(channel.send("Error: this toon already exists."))

    @staticmethod
    def remove_toon(user, toon, toon_family, channel):
        if persistence.check_if_toon_exists(toon):
            if persistence.check_if_toon_belongs_to_family(toon, toon_family):
                user_id = user.id
                if persistence.check_if_user_owns_family(user_id, toon_family):
                    persistence.remove_toon(toon)
                    if not persistence.check_if_toon_exists(toon):
                        asyncio.ensure_future(channel.send("Success: this toon was successfully removed."))
                    else:
                        asyncio.ensure_future(channel.send("Error: something went wrong, please notify the bot owner."))
                else:
                    asyncio.ensure_future(channel.send("Error: this user does not own the corresponding family."))
            else:
                asyncio.ensure_future(channel.send("Error: this toon does not belong to that family."))
        else:
            asyncio.ensure_future(channel.send("Error: this toon does not exist."))

    @staticmethod
    def get_toons_for_family(family, channel):
        if persistence.check_if_family_exists(family):
            toons = persistence.get_toons(family)
            if len(toons) == 0:
                asyncio.ensure_future(channel.send("Error: this user does not have any registered toons."))
            else:
                return toons
        else:
            asyncio.ensure_future(channel.send("Error: this family does not exist."))
        return list()

    @staticmethod
    def set_toon_level(channel, toon, level, xp_percentage):
        if persistence.check_if_toon_exists(toon):
            persistence.set_toon_level(toon, level, xp_percentage)
            result = persistence.get_toon_level(toon)
            print(str(result[0]) == level)
            print(float(result[1]) == float(xp_percentage))
            if str(result[0]) == level and float(result[1]) == float(xp_percentage):
                asyncio.ensure_future(channel.send("Success: the level was successfully updated."))
            else:
                asyncio.ensure_future(channel.send("Error: something went wrong, please notify the bot owner."))
        else:
            asyncio.ensure_future(channel.send("Error: this toon does not exist."))

    @staticmethod
    def get_toon_overview(channel, family):
        if persistence.check_if_family_exists(family):
            toons = persistence.get_toons(family)
            if len(toons) == 0:
                asyncio.ensure_future(channel.send("Error: there are no toons registered with this family."))
            else:
                output = "```========================================================\n"
                output += "|toon            |class      |level|%      |ap |aap|dp |\n"
                output += "========================================================\n"
                for toon in toons:
                    condition = persistence.check_if_toon_exists_in_gear(toon[0])
                    output += "|" + toon[0] + ((16 - len(toon[0])) * ' ')
                    output += "|" + toon[2] + ((11 - len(toon[2])) * ' ')
                    output += "|" + str(toon[3]) + ((5 - len(str(toon[3]))) * ' ')
                    output += "|" + str(toon[4]) + ((6 - len(str(toon[4]))) * ' ') + "%"
                    if condition:
                        ap = persistence.get_gear_value(toon[0], "ap")
                        aap = persistence.get_gear_value(toon[0], "aap")
                        dp = persistence.get_gear_value(toon[0], "dp")
                        output += "|" + str(ap) + ((3 - len(str(ap))) * ' ')
                        output += "|" + str(aap) + ((3 - len(str(aap))) * ' ')
                        output += "|" + str(dp) + ((3 - len(str(dp))) * ' ')
                    else:
                        output += '|0  |0  |0  '
                    output += "|\n"
                output += "========================================================\n```"
                asyncio.ensure_future(channel.send(output))
        else:
            asyncio.ensure_future(channel.send("Error: that family name does not exist."))

    # ~~~~~~~~~~~~~~~~~~~~ Gear ~~~~~~~~~~~~~~~~~~~~~~~~
    def set_gear_variable(self, channel, value, toon, variable):
        condition = self.check_if_integer(value)
        if condition:
            if not persistence.check_if_toon_exists(toon):
                asyncio.ensure_future(channel.send("Error: this toon does not exist."))
                return
            if not persistence.check_if_toon_exists_in_gear(toon):
                persistence.add_toon_to_gear(toon)
            old_value = persistence.get_gear_value(toon, variable)
            persistence.set_gear_value(toon, value, variable)
            difference = int(value) - old_value
            if difference != 0:
                persistence.add_event(toon, "ap", difference)
            if str(persistence.get_gear_value(toon, variable)) == value:
                asyncio.ensure_future(channel.send("Success: ap was updated."))
            else:
                asyncio.ensure_future(channel.send("Error: something went wrong, please notify the bot owner."))
        else:
            asyncio.ensure_future(self.alert_for_incorrect_format(channel))
        return

    # ~~~~~~~~~~~~~~~~~~~ Skills ~~~~~~~~~~~~~~~~~~~~~~~~~
    def set_skill_value(self, channel, value, toon, skill):
        condition = self.check_if_integer(value)
        if condition:
            if not persistence.check_if_toon_exists(toon):
                asyncio.ensure_future(channel.send("Error: this toon does not exist."))
                return
            if not persistence.check_if_toon_exists_in_skills(toon):
                persistence.add_toon_to_skills(toon)
            old_value = persistence.get_skill_value(toon, skill)
            persistence.set_skill_value(toon, value, skill)
            difference = int(value) - old_value
            if difference != 0:
                persistence.add_event(toon, skill, difference)
            if str(persistence.get_skill_value(toon, skill)) == value:
                asyncio.ensure_future(channel.send("Success: {} was updated.".format(skill)))
            else:
                asyncio.ensure_future(channel.send("Error: something went wrong, please notify the bot owner."))

    @staticmethod
    def get_skill_overview(channel, family):
        if persistence.check_if_family_exists(family):
            toons = persistence.get_toons(family)
            if len(toons) == 0:
                asyncio.ensure_future(channel.send("Error: there are no toons registered with this family."))
            else:
                output = "```====================================================================================" \
                         "====================\n"
                output += "|toon            |class      |level|%      |Gath |Fish |Hunt |" \
                          "Cook |Alch |Proc |Train|Trade|Farm |Sail |\n"
                output += "======================================================================================" \
                          "==================\n"
                for toon in toons:
                    condition = persistence.check_if_toon_exists_in_skills(toon[0])
                    output += "|" + toon[0] + ((16 - len(toon[0])) * ' ')
                    output += "|" + toon[2] + ((11 - len(toon[2])) * ' ')
                    output += "|" + str(toon[3]) + ((5 - len(str(toon[3]))) * ' ')
                    output += "|" + str(toon[4]) + ((6 - len(str(toon[4]))) * ' ') + "%"
                    if condition:
                        skills = persistence.get_skills_for_toon(toon[0])
                        output += "|" + str(skills[0]) + ((5 - len(str(skills[0]))) * ' ')
                        output += "|" + str(skills[1]) + ((5 - len(str(skills[1]))) * ' ')
                        output += "|" + str(skills[2]) + ((5 - len(str(skills[2]))) * ' ')
                        output += "|" + str(skills[3]) + ((5 - len(str(skills[3]))) * ' ')
                        output += "|" + str(skills[4]) + ((5 - len(str(skills[4]))) * ' ')
                        output += "|" + str(skills[5]) + ((5 - len(str(skills[5]))) * ' ')
                        output += "|" + str(skills[6]) + ((5 - len(str(skills[6]))) * ' ')
                        output += "|" + str(skills[7]) + ((5 - len(str(skills[7]))) * ' ')
                        output += "|" + str(skills[8]) + ((5 - len(str(skills[8]))) * ' ')
                        output += "|" + str(skills[9]) + ((5 - len(str(skills[9]))) * ' ')
                    else:
                        output += '|0    ' * 10
                    output += "|\n"
                output += "======================================================================================" \
                          "==================```"
                output2 = "```====================================================================================" \
                          "====================" \
                          "\n| The conversion of numerical values to actual skill levels is given by:" + 31 * ' ' +\
                          "|\n| 1-10:   beginner      1-10" + 75 * ' ' +\
                          "|\n| 11-20:  apprentice    1-10" + 75 * ' ' +\
                          "|\n| 21-30:  skilled       1-10" + 75 * ' ' +\
                          "|\n| 31-40:  professional  1-10" + 75 * ' ' +\
                          "|\n| 41-50:  artisan       1-10" + 75 * ' ' +\
                          "|\n| 51-80:  master        1-30" + 75 * ' ' +\
                          "|\n| 81-130: guru          1-50" + 75 * ' ' +\
                          "|\n======================================================================================" \
                          "==================```"
                asyncio.ensure_future(channel.send(output))
                asyncio.ensure_future(channel.send(output2))
        else:
            asyncio.ensure_future(channel.send("Error: that family name does not exist."))

    # ~~~~~~~~~~~~~~~~~~~ History ~~~~~~~~~~~~~~~~~~~~~~~~

    @staticmethod
    def register_event(toon, stat, value):
        persistence.add_event(toon, stat, value)

    @staticmethod
    def get_toon_history(toon, channel):
        user_exists = persistence.check_if_toon_exists_in_gear(toon)
        if not user_exists:
            asyncio.ensure_future(channel.send("Error: this character does not have a history."))
            return
        else:
            history = persistence.get_toon_history(toon)
            output = ""
            for event in history:
                output += "{} at {}: {} has increased its {} by {}\n"\
                             .format(event[0], str(event[1]).rsplit(".")[0], event[2], event[3], event[4])
            asyncio.ensure_future(channel.send(output))
            return

    @staticmethod
    def get_family_history(family, channel):
        if persistence.check_if_family_exists(family):
            result = persistence.get_family_history(family)
            output = ""
            for event in result:
                output += "{} at {}: {} has increased its {} by {}\n"\
                             .format(event[0], str(event[1]).rsplit(".")[0], event[2], event[3], event[4])
            asyncio.ensure_future(channel.send(output))
        else:
            asyncio.ensure_future(channel.send("Error: this family does not exist"))

    # ~~~~~~~~~~~~~~~~~~~~ General ~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def check_if_integer(value):
        pattern = re.compile("(0|[1-9]\\d*)")
        if pattern.match(value):
            return True
        return False

    @staticmethod
    async def alert_for_incorrect_format(channel):
        await channel.send("Incorrect format, use !help to check the available commands!")
        return
