import re
import asyncio

from Persistence import Persistence

persistence = Persistence()


class UserTracker:
    # ~~~~~~~~~~~~~~~~~~~~ Toons ~~~~~~~~~~~~~~~~~~~~~~~~
    @staticmethod
    def add_toon(user, toon, toon_class, channel):
        if not persistence.check_if_toon_exists(toon):
            persistence.add_toon(user, toon, toon_class)
        else:
            asyncio.ensure_future(channel.send("Error: this toon already exists."))

    @staticmethod
    def remove_toon(user, toon, channel):
        if not persistence.check_if_toon_exists(toon):
            asyncio.ensure_future(channel.send("Error: this toon does not exist."))
            return
        else:
            persistence.remove_toon(user, toon)
            return

    @staticmethod
    def get_toons(user, channel):
        if not persistence.check_if_user_exists(user.id):
            asyncio.ensure_future(channel.send("Error: this user is not registered."))
        else:
            toons = persistence.get_toons(user)
            if len(toons) == 0:
                asyncio.ensure_future(channel.send("Error: this user does not have any registered toons."))
            else:
                return toons
        return list()

    # ~~~~~~~~~~~~~~~~~~~~ Gear ~~~~~~~~~~~~~~~~~~~~~~~~

    def set_dp(self, value, toon, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_toon_exists(toon):
                asyncio.ensure_future(channel.send("Error: this toon does not exist."))
                return
            if not persistence.check_if_toon_exists_in_gear(toon):
                persistence.add_gear(toon)
            old_dp = persistence.get_dp(toon)
            persistence.set_dp(toon, value)
            dif = value - old_dp
            persistence.add_event(toon, "dp", dif)
        return

    def set_ap(self, value, toon, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_toon_exists(toon):
                asyncio.ensure_future(channel.send("Error: this toon does not exist."))
                return
            if not persistence.check_if_toon_exists_in_gear(toon):
                persistence.add_gear(toon)
            old_ap = persistence.get_ap(toon)
            persistence.set_ap(toon, value)
            print(old_ap)
            dif = int(value) - old_ap
            persistence.add_event(toon, "ap", dif)
        return

    def set_aap(self, value, toon, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_toon_exists(toon):
                asyncio.ensure_future(channel.send("Error: this toon does not exist."))
                return
            if not persistence.check_if_toon_exists_in_gear(toon):
                persistence.add_gear(toon)
            old_aap = persistence.get_aap(toon)
            persistence.set_aap(toon, value)
            dif = value - old_aap
            persistence.add_event(toon, "aap", dif)
        return

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
            counter = 0
            for event in reversed(history):
                output = "{}: {} has increased its {} by {}\n".format(event[1], event[3], event[0], event[2]) + output
                counter += 1
                if counter == 20:
                    break
            asyncio.ensure_future(channel.send(output))
            return

    def get_character_history(self, user, channel):
        toons = self.get_toons(user, channel)
        for toon in toons:
            self.get_toon_history(toon[1], channel)
            asyncio.ensure_future(channel.send("\n"))

    # ~~~~~~~~~~~~~~~~~~~~ General ~~~~~~~~~~~~~~~~~~~~

    async def check_if_integer(self, value, channel):
        pattern = re.compile("(0|[1-9]\\d*)")
        if pattern.match(value):
            return True
        await self.alert_for_incorrect_format(channel)
        return False

    @staticmethod
    async def alert_for_incorrect_format(channel):
        await channel.send("Incorrect format, use !help to check the available commands!")
        return
