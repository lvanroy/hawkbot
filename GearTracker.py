import re
import asyncio

from Persistence import Persistence

persistence = Persistence()


class GearTracker:
    def add_toon(self, user, toon, toon_class, channel):
        if not persistence.check_if_toon_exists(user, toon):
            persistence.add_toon(user, toon, toon_class)
        else:
            asyncio.ensure_future(channel.send("Error: this toon already exists."))

    def set_dp(self, value, user, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_user_exists(user):
                persistence.add_user(user)
            if not persistence.check_if_user_exists_in_gear(user):
                persistence.add_gear(user)
            persistence.set_dp(user, value)
        return

    def set_ap(self, value, user, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_user_exists(user):
                persistence.add_user(user)
            if not persistence.check_if_user_exists_in_gear(user):
                persistence.add_gear(user)
            persistence.set_ap(user, value)
        return

    def set_aap(self, value, user, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_user_exists(user):
                persistence.add_user(user)
            if not persistence.check_if_user_exists_in_gear(user):
                persistence.add_gear(user)
            persistence.set_aap(user, value)
        return

    def get_stats(self, user, channel):
        user_exists = persistence.check_if_user_exists_in_gear(user_id)

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
