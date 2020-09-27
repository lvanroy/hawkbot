import asyncio

from Persistence import Persistence
from math import ceil

persistence = Persistence()


class AdminCommands:
    @staticmethod
    def add_activity(family, current_activity, channel):
        if not persistence.see_if_activity_exists(family):
            persistence.add_activity(family, current_activity)
        else:
            asyncio.ensure_future(channel.send("Error: this family already exists"))

    @staticmethod
    def register_renewal(family, current_activity, channel):
        if persistence.see_if_activity_exists(family):
            persistence.register_renewal(family, current_activity)
        else:
            asyncio.ensure_future(channel.send("Error: this family does not exist."))

    @staticmethod
    def compute_payout_values():
        results = persistence.get_weekly_activities()
        min_act = None
        max_act = None
        for result in results:
            if min_act is None:
                min_act = result[1]
                max_act = result[1]
            if result[1] < min_act:
                min_act = result[1]
            if result[1] > max_act:
                max_act = result[1]

        output = ""
        for result in results:
            if max_act != min_act:
                output += "{} has gained a total of {} activity and has level {}\n"\
                    .format(result[0], result[1], int(ceil(result[1] - min_act)/(max_act - min_act) * 9 + 1))
            else:
                output += "{} has gained a total of {} activity and has level {}\n".format(result[0], result[1], 1)
        return output

    @staticmethod
    def reset_tracker():
        persistence.reset_tracker()
        return
