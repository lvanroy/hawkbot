import re
import asyncio

from Persistence import Persistence

persistence = Persistence()


class GearTracker:
    @staticmethod
    def set_gear_stats(toon, stats):
        if not persistence.check_if_toon_exists_in_gear(toon):
            persistence.add_toon_to_gear(toon)
        persistence.set_gear_stats(toon, stats)
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
