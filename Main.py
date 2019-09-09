import discord
import random
import asyncio
import sys

from BossTimers import initialise_timers, print_timers
from UserTracker import UserTracker
from discord.utils import get

token = "NjA0ODYxOTI5NTQ2MzE3ODI2.XT_VGA.diM8D5Ksr2bTv44_VgxdOXLD_o8"

user_tracker = None

client = discord.Client()
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@client.event
async def on_ready():
    bot_channel = client.get_channel(605023656132739110)
    initialise_timers(bot_channel)

    global user_tracker
    user_tracker = UserTracker()

    print("Good to go!!")


@client.event
async def on_message(message):
    # ensure message of the bot itself are skipped
    if message.author == client.user:
        return

    print("We received a message from " +
          message.author.name + ": " +
          message.content)

    # ensure that the boss is only active in its respective channel(s)
    if str(message.channel) != "botspam" and str(message.channel) != "request-roles":
        return

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Spam ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if str(message.channel) == "botspam":
        # give the users an option to see which commands are available
        if message.content == "!help":
            output = "Use the following commands to make and or delete toons:\n" \
                     "!toons add <name> <class>\n" \
                     "!toons remove <name>\n" \
                     "\nUse the following commands to set respective gear variables:\n" + \
                     "!gear set ap <value> <toon>\n" + \
                     "!gear set aap <value> <toon>\n" + \
                     "!gear set dp <value> <toon>\n" \
                     "\n use the following commands to see the history for a given toon or character\n" \
                     "!toonhistory <toon>\n" \
                     "!charhistory <character>\n" + \
                     "\nUse the following commands to see the current timers:\n" + \
                     "!bosstimer <boss>" \
                     " (boss tag is optional, if no tag is given, the timers for all bosses will be given)\n" + \
                     "\ngeneral non bdo related commands:\n" + \
                     "!dice <lower> <upper> (these bounds are optional)\n" + \
                     "\nthe following command gives a link to the bots github:\n" + \
                     "!discord"

            await message.channel.send(output)
            return

        # -----------------------------------------------------------------------------------------
        # Toon commands
        # these commands are used to manage the different toons linked for an account,
        # one can add, display and remove toons
        # -----------------------------------------------------------------------------------------
        elif message.content.startswith("!toons add "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 5:
                arguments[-2] = arguments[-2] + " " + arguments[-1]
                arguments.pop()
            if len(arguments) == 4:
                toon_name = arguments[2]
                toon_class = arguments[3]
                print(toon_class)
                user = message.author
                if toon_class not in ["Warrior",     "Ranger",  "Sorceress", "Berserker",
                                      "Valkyrie",    "Wizard",  "Witch",     "Tamer",
                                      "Maehwa",      "Musa",    "Ninja",     "Kunoichi",
                                      "Striker",     "Mystic",  "Lahn",      "Archer",
                                      "Dark Knight", "Shai"]:
                    await channel.send("Error, that class does not exist. "
                                       "All classes need to start with capital letters.")
                    return
                user_tracker.add_toon(user, toon_name, toon_class, channel)
            else:
                await alert_for_incorrect_format(channel)

        elif message.content.startswith("!toons remove "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 3:
                toon_name = arguments[2]
                user = message.author
                user_tracker.remove_toon(user, toon_name, channel)
            else:
                await alert_for_incorrect_format(channel)

        # -----------------------------------------------------------------------------------------
        # Gear commands
        # these commands are al related to the gear database that is stored for each guild member
        # these stats will be used to properly determine the stats of the guild members, as well
        # as help us properly organise events, and notify the proper people for those events
        # -----------------------------------------------------------------------------------------
        elif message.content.startswith("!gear set ap "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 5:
                toon = arguments[-1]
                ap = arguments[-2]
                user_tracker.set_ap(ap, toon, channel)
            else:
                await alert_for_incorrect_format(channel)
            return
        elif message.content.startswith("!gear set aap "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 5:
                aap = arguments[-2]
                toon = arguments[-1]
                user_tracker.set_aap(aap, toon, channel)
            else:
                await alert_for_incorrect_format(channel)
            return
        elif message.content.startswith("!gear set dp "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 5:
                toon = arguments[-1]
                dp = arguments[-2]
                user_tracker.set_dp(dp, toon, channel)
            else:
                await alert_for_incorrect_format(channel)
            return

        # -----------------------------------------------------------------------------------------
        # History commands
        # these commands let players access the history of their account/toons
        # the history lists all changes in stats
        # the history will list at most the 20 most recent events
        # -----------------------------------------------------------------------------------------
        elif message.content.startswith("!toonhistory "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 2:
                toon = arguments[1]
                user_tracker.get_toon_history(toon, channel)
            else:
                await alert_for_incorrect_format(channel)
            return
        elif message.content.startswith("!charhistory "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 2:
                user = arguments[1]
                user_tracker.get_character_history(user, channel)

        # -----------------------------------------------------------------------------------------
        # Timer commands
        # these commands let players access the boss timers and the imperial trade timers
        # as wel as the night timer
        # -----------------------------------------------------------------------------------------
        elif message.content.startswith("!bosstimers"):
            arguments = message.content.split(" ")
            if len(arguments) == 1:
                await print_timers()
            elif len(arguments) == 2:
                await print_timers(arguments[1])
            else:
                await alert_for_incorrect_format(message.channel)
            return

        # ------------------------------------------------------------------------------------------
        # General commands
        # these commands are not necessarily game related, but are mostly for fun
        # ------------------------------------------------------------------------------------------
        elif message.content.startswith("!dice"):
            number = await random.randint(0, 2000000000)
            arguments = message.content.split(" ")
            if len(arguments) >= 3:
                lower = arguments[1]
                upper = arguments[2]
                number = await random.randint(int(lower), int(upper))
            await message.channel.send(number)
            return

        elif message.content.startswith("!discord"):
            await message.channel.send("https://github.com/larsVanRoy/hawkbot")

        elif message.content.startswith("!stop") and message.author.name == "badoody(OfTheImpossibru)":
            await client.close()

        elif message.content.startswith("!"):
            output = "Command not recognized, use !help to get a list of available commands!"
            await message.channel.send(output)
            return

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ROLES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif str(message.channel) == "request-roles":
        print(message.content)
        # give the users an option to see which commands are available
        if message.content == "!help":
            output = "This channel is used to request roles.\nAll roles can be requested by using the " \
                     "!assing <role> command.\nWe currently support the following roles: \n" \
                     "Kzarka\n" \
                     "Kutum\n" \
                     "Karanda\n" \
                     "Offin\n" \
                     "Nouver\n" \
                     "Garmoth\n" \
                     "Quint/Muraka\n" \
                     "Vell\n"\
                     "Having one of these boss roles will enable you to get notified whenever these bosses are " \
                     "30 min away from spawning, 5 min away from spawning and when they have spawned.\n" \
                     "roles can be removed by the !remove <role> command\n"
            await message.channel.send(output)
            return

        # ------------------------------------------------------------------------------------------
        # Role commands
        # These commands allow member to assign roles to themselves, all of these roles give no extra rights/benefits
        # and are purely to allow to properly address the correct guild members
        # ------------------------------------------------------------------------------------------
        elif message.content.startswith("!assign "):
            arguments = message.content.split(" ")
            if len(arguments) == 2:
                member = message.author
                if arguments[1] in ["Kzarka", "Kutum",   "Karanda",          "Offin",
                                    "Nouver", "Garmoth", "Quint/Muraka", "Vell"]:
                    role = get(message.guild.roles, name=arguments[1])
                    await member.add_roles(role)
                    await message.channel.send("Assigned role {} to {}".format(arguments[1], message.author))
                else:
                    await alert_for_incorrect_format(message.channel)
            else:
                await alert_for_incorrect_format(message.channel)
            return

        elif message.content.startswith("!remove "):
            arguments = message.content.split(" ")
            if len(arguments) == 2:
                member = message.author
                if arguments[1] in ["Kzarka", "Kutum",   "Karanda",          "Offin",
                                    "Nouver", "Garmoth", "Quint/Muraka", "Vell"]:
                    role = get(message.guild.roles, name=arguments[1])
                    await member.remove_roles(role)
                else:
                    await alert_for_incorrect_format(message.channel)
            else:
                await alert_for_incorrect_format(message.channel)
            return

        elif message.content.startswith("!"):
            output = "Command not recognized, use !help to get a list of available commands!"
            await message.channel.send(output)
            return


async def alert_for_incorrect_format(channel):
    await channel.send("Incorrect format, use !help to check the available commands!")


client.run(token)
