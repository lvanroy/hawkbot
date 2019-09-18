import re
import asyncio

from Persistence import Persistence

persistence = Persistence()


class GearTracker:
    def set_dp(self, value, toon, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_toon_exists_in_gear(toon):
                persistence.add_toon_to_gear(toon)
            persistence.set_dp(toon, value)
        return

    def set_ap(self, value, toon, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_toon_exists_in_gear(toon):
                persistence.add_toon_to_gear(toon)
            persistence.set_ap(toon, value)
        return

    def set_aap(self, value, toon, channel):
        condition = asyncio.ensure_future(self.check_if_integer(value, channel))
        if condition:
            if not persistence.check_if_toon_exists_in_gear(toon):
                persistence.add_toon_to_gear(toon)
            persistence.set_aap(toon, value)
        return

    def get_stats(self, toon, channel):
        user_exists = persistence.check_if_toon_exists_in_gear(toon)

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
