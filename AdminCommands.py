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
                if result[1] < 0.05 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 1)
                elif result[1] < 0.1 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 2)
                elif result[1] < 0.2 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 3)
                elif result[1] < 0.3 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 4)
                elif result[1] < 0.4 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 5)
                elif result[1] < 0.5 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 6)
                elif result[1] < 0.6 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 7)
                elif result[1] < 0.7 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 8)
                elif result[1] < 0.8 * max_act:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 9)
                else:
                    output += "{} gained {}, level {}\n".format(result[0], result[1], 10)
            else:
                output += "{} gained {}, level {}\n".format(result[0], result[1], 1)
        return output

    @staticmethod
    def reset_tracker():
        persistence.reset_tracker()
        return
