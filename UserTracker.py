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
    def add_toon(user, toon, toon_family, toon_class, channel):
        if not persistence.check_if_toon_exists(toon):
            user_id = user.id
            if persistence.check_if_user_owns_family(user_id, toon_family):
                try:
                    persistence.add_toon(toon, toon_family, toon_class)
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
            persistence.add_event(toon, skill, difference)
            if str(persistence.get_skill_value(toon, skill)) == value:
                asyncio.ensure_future(channel.send("Success: {} was updated.".format(skill)))
            else:
                asyncio.ensure_future(channel.send("Error: something went wrong, please notify the bot owner."))

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
