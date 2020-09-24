import discord
import random
import asyncio

from BossTimers import initialise_timers, print_timers
from UserTracker import UserTracker
from UpdateTracker import initialise_update_tracker
from Distractions import get_joke_categories, get_joke, get_meme
from AdminCommands import AdminCommands

from os import system, path

from discord.utils import get

f = open("./token.txt", 'r')
token = f.read().split("\n")[0]

user_tracker = UserTracker()

client = discord.Client()

bot_channel = client.get_channel(623893978273808404)
initialise_timers(bot_channel)

admin_commands = AdminCommands()


@client.event
async def on_ready():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if not path.exists("../skraper-master/cli/target"):
        system('cd ../skraper-master;./mvnw clean package -DskipTests=true ')

    update_channel = client.get_channel(626063347854606337)
    news_channel = client.get_channel(626077658802946068)
    initialise_update_tracker(news_channel, update_channel)

    global user_tracker
    user_tracker = UserTracker()

    print("Good to go!!")


@client.event
async def on_message(message):
    # ensure message of the bot itself are skipped
    if message.author == client.user:
        return

    # ensure that the boss is only active in its respective channel(s)
    if str(message.channel) != "botspam" and str(message.channel) != "request-roles" and \
            str(message.channel) != "jokes-and-funny-stuff" and \
            str(message.channel) != "admin-commands":
        return

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Spam ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if str(message.channel) == "botspam":
        # give the users an option to see which commands are available
        if message.content == "!help":
            output = "Use the following commands to make and or delete families:\n" \
                     "!family add <name>\n" \
                     "!family remove <name>\n" \
                     "\nUse the following commands to make and or delete toons:\n" \
                     "!toons add <family> <name> <class> <url>\n" \
                     "!toons remove <family> <name>\n" \
                     "The url must be a public bdoplanner character from which all character stats will be retrieved.\n" + \
                     "\nUse the following commands to get an overview of the toons for a given family:\n" \
                     "!toons overview <family>\n" + \
                     "!gear overview <family>\n" + \
                     "!skills overview <family>\n" + \
                     "!toon overview <toon>\n" + \
                     "\nUse the following commands to see the current timers:\n" + \
                     "!bosstimers <boss>" \
                     " (boss tag is optional, if no tag is given, the timers for all bosses will be given)\n" + \
                     "\ngeneral non bdo related commands:\n" + \
                     "!dice <lower> <upper> (these bounds are optional)\n" + \
                     "!praise\n!praisebot\n" + \
                     "\nthe following command gives a link to the bots github:\n" + \
                     "!github"

            await message.channel.send(output)
            return

        # -----------------------------------------------------------------------------------------
        # Family commands
        # these commands are used to manage the different families linked for a user,
        # one can add, display and remove families
        # families are linked to the created, and can therefore only be deleted by the creation user
        # -----------------------------------------------------------------------------------------
        elif message.content.startswith("!family add "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 3:
                family_name = arguments[2]
                user = message.author
                user_tracker.add_family(user, family_name, channel)
            else:
                await alert_for_incorrect_format(channel)

        elif message.content.startswith("!family remove "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 3:
                family_name = arguments[2]
                user = message.author
                user_tracker.remove_family(user, family_name, channel)
            else:
                await alert_for_incorrect_format(channel)

        # -----------------------------------------------------------------------------------------
        # Toon commands
        # these commands are used to manage the different toons linked for an account,
        # one can add, display and remove toons
        # -----------------------------------------------------------------------------------------
        elif message.content.startswith("!toons add "):
            arguments = message.content.split(" ")
            channel = message.channel
            print(arguments)
            if len(arguments) == 7:
                arguments[-4] = arguments[-4] + " " + arguments[-3]
                arguments.pop(-3)
            if len(arguments) == 6:
                toon_family = arguments[2]
                toon_name = arguments[3]
                toon_class = arguments[4]
                url = arguments[5]
                user = message.author
                if toon_class not in ["Warrior", "Ranger", "Sorceress", "Berserker",
                                      "Valkyrie", "Wizard", "Witch", "Tamer",
                                      "Maehwa", "Musa", "Ninja", "Kunoichi",
                                      "Striker", "Mystic", "Lahn", "Archer",
                                      "Dark Knight", "Shai", "Guardian"]:
                    await channel.send("Error, that class does not exist. "
                                       "All classes need to start with capital letters.")
                    return
                user_tracker.add_toon(user, toon_name, toon_family, toon_class, url, channel)
            else:
                await alert_for_incorrect_format(channel)

        elif message.content.startswith("!toons remove "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 4:
                toon_family = arguments[2]
                toon_name = arguments[3]
                user = message.author
                user_tracker.remove_toon(user, toon_name, toon_family, channel)
            else:
                await alert_for_incorrect_format(channel)

        elif message.content.startswith("!toons overview"):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 3:
                toon_family = arguments[-1]
                user_tracker.get_toon_overview(channel, toon_family)
            else:
                await alert_for_incorrect_format(channel)

        # -----------------------------------------------------------------------------------------
        # Skill commands
        # these commands are al related to the skill database that is stored for each guild member
        # these stats will be used to list progress for each toon that is part of the guild
        # these stats can also be used to properly direct messages for events that require higher levels
        # -----------------------------------------------------------------------------------------
        elif message.content.startswith("!skills overview "):
            arguments = message.content.split(" ")
            channel = message.channel
            if len(arguments) == 3:
                toon_family = arguments[-1]
                user_tracker.get_skill_overview(channel, toon_family)
            else:
                await alert_for_incorrect_format(channel)

        # -----------------------------------------------------------------------------------------
        # Timer commands
        # these commands let players access the boss timers and the imperial trade timers
        # as wel as the night timer
        # -----------------------------------------------------------------------------------------
        elif message.content.startswith("!bosstimers"):
            arguments = message.content.split(" ")
            if len(arguments) == 1:
                await print_timers(message.channel)
            elif len(arguments) == 2:
                await print_timers(message.channel, arguments[1])
            else:
                await alert_for_incorrect_format(message.channel)
            return

        # ------------------------------------------------------------------------------------------
        # General commands
        # these commands are not necessarily game related, but are mostly for fun
        # ------------------------------------------------------------------------------------------
        elif message.content.startswith("!dice"):
            arguments = message.content.split(" ")
            if len(arguments) == 3:
                lower = arguments[1]
                upper = arguments[2]
                number = random.randint(int(lower), int(upper))
                await message.channel.send(number)
            elif len(arguments) == 1:
                number = random.randint(0, 2000000000)
                await message.channel.send(number)
            else:
                await alert_for_incorrect_format(message.channel)
            return

        elif message.content.startswith("!praisebot"):
            await message.channel.send("<@604861929546317826> is the best bot ever!")

        elif message.content.startswith("!praise"):
            await message.channel.send("<@194853137096376320> Thank you for all the effort! Love the bot!")

        elif message.content.startswith("!github"):
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
        # give the users an option to see which commands are available
        if message.content == "!help":
            output = "This channel is used to request roles.\nAll roles can be requested by using the " \
                     "!assign <role> command.\nWe currently support the following roles: \n" \
                     "Kzarka\n" \
                     "Kutum\n" \
                     "Karanda\n" \
                     "Offin\n" \
                     "Nouver\n" \
                     "Garmoth\n" \
                     "Quint/Muraka\n" \
                     "Vell\n" \
                     "Having one of these boss roles will enable you to get notified whenever these bosses are " \
                     "60 min away from spawning, 30 min away from spawning, " \
                     "5 min away from spawning and when they have spawned.\n" \
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
                if arguments[1] in ["Kzarka", "Kutum", "Karanda", "Offin",
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
                if arguments[1] in ["Kzarka", "Kutum", "Karanda", "Offin",
                                    "Nouver", "Garmoth", "Quint/Muraka", "Vell"]:
                    role = get(message.guild.roles, name=arguments[1])
                    await member.remove_roles(role)
                    await message.channel.send("Removed role {} from {}".format(arguments[1], message.author))
                else:
                    await alert_for_incorrect_format(message.channel)
            else:
                await alert_for_incorrect_format(message.channel)
            return

        elif message.content.startswith("!"):
            output = "Command not recognized, use !help to get a list of available commands!"
            await message.channel.send(output)
            return

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ DISTRACTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif str(message.channel) == "jokes-and-funny-stuff":
        if message.content == "!joke categories":
            await message.channel.send(get_joke_categories())
            return

        elif message.content.startswith("!joke get"):
            arguments = message.content.split(" ")
            if len(arguments) == 3:
                await message.channel.send(get_joke(arguments[-1]))
            else:
                await alert_for_incorrect_format(message.channel)
            return

        elif message.content.startswith("!meme get"):
            arguments = message.content.split(" ")
            categories = ["hot", "funny", "animals", "awesome", "car", "gaming", "wtf", "politics", "meme", "darkhumor",
                          "satisfying"]
            if len(arguments) == 3 and arguments[-1] in categories:
                await message.channel.send(get_meme(arguments[-1]))
            else:
                await alert_for_incorrect_format(message.channel)
            return

        elif message.content == "!meme categories":
            output = "The following categories are currently supported: \n" \
                     "\t hot\n" \
                     "\t funny\n" \
                     "\t animals\n" \
                     "\t awesome\n" \
                     "\t car\n" \
                     "\t gaming\n" \
                     "\t wtf\n" \
                     "\t politics\n" \
                     "\t meme\n" \
                     "\t darkhumor\n" \
                     "\t satisfying"
            await message.channel.send(output)
            return

        elif message.content == "!help":
            output = "This channel is used for jokes and memes.\n" \
                     "!joke categories\n" \
                     "!joke get <category>\n" \
                     "!meme categories\n" \
                     "!meme get <category>"
            await message.channel.send(output)
            return

        elif message.content.startswith("!"):
            output = "Command not recognized, use !help to get a list of available commands!"
            await message.channel.send(output)
            return

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ADMIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elif str(message.channel) == "admin-commands":
        if message.content == "!weekly reset":
            await message.channel.send(admin_commands.compute_payout_values())
            return

        elif message.content == "!renew":
            arguments = message.content.split(" ")
            if len(arguments) == 3:
                admin_commands.register_renewal(arguments[1], arguments[2], message.channel)
            else:
                await alert_for_incorrect_format(message.channel)

        elif message.content == "!register":
            arguments = message.content.split(" ")
            if len(arguments) == 3:
                admin_commands.add_activity(arguments[1], arguments[2], message.channel)
            else:
                await alert_for_incorrect_format(message.channel)

        elif message.content == "!help":
            output = "This channel is used for admin commands.\n" \
                     "!weekly reset\n" \
                     "!renew <family> <current activity>\n" \
                     "!register <family> <current activity>"
            await message.channel.send(output)
            return

        elif message.content.startswith("!"):
            output = "Command not recognized, use !help to get a list of available commands!"
            await message.channel.send(output)
            return


async def alert_for_incorrect_format(channel):
    await channel.send("Incorrect format, use !help to check the available commands!")


client.run(token)
