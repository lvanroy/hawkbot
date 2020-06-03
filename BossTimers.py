from threading import Timer
from datetime import datetime
from math import floor

import time
import asyncio


# initialise the boss spawn timers, these timers will cause notifications to all subscribed members
# half an hour in advance and when the boss has acc spawned
def check_advanced_notice():
    timers["general"] = Timer(40, check_advanced_notice)
    timers["general"].start()

    for key in remaining_time.keys():
        elapsed_time = floor(time.time() - start_time[key])
        elapsed_hours = floor(elapsed_time/60/60)
        elapsed_minutes = floor(elapsed_time/60) % 60
        elapsed_seconds = floor(elapsed_time) % 60
        remaining_time_for_boss = remaining_time[key]
        hours = floor((remaining_time_for_boss/60/60)) - elapsed_hours
        minutes = floor(remaining_time_for_boss/60 % 60) - elapsed_minutes
        seconds = remaining_time_for_boss % 60 - elapsed_seconds

        if seconds < 0:
            minutes -= 1
        if minutes < 0:
            hours -= 1
            minutes = 60 + minutes

        if hours == 1 and minutes == 0 and channel is not None and not notified[key][0]:
            hour_notifier = Timer(seconds, notify_in_advance, [key, 60])
            hour_notifier.start()
            notified[key][0] = True
            notified[key[3] = False

        if hours == 0 and minutes == 30 and channel is not None and not notified[key][1]:
            half_hour_notifier = Timer(seconds, notify_in_advance, [key, 30])
            half_hour_notifier.start()
            notified[key][1] = True

        elif hours == 0 and minutes == 5 and channel is not None and not notified[key][2]:
            five_min_notifier = Timer(seconds, notify_in_advance, [key, 5])
            five_min_notifier.start()
            notified[key][2] = True


def notify_in_advance(boss, period):
    asyncio.run_coroutine_threadsafe(
        channel.send("{} {} will spawn in {} minutes!".format(mapping[boss], boss, period)), loop)


def notify_karanda():
    if not notified["Karanda"][3]:
        if channel is not None:
            asyncio.run_coroutine_threadsafe(channel.send("<@&605835920477913090> Karanda has spawned!"), loop)

        current_time = get_curent_time()

        time_remaining = check_remaining_time(karanda, current_time)
        karanda_timer = Timer(time_remaining, notify_karanda)
        karanda_timer.start()
        timers["Karanda"] = karanda_timer
        remaining_time["Karanda"] = time_remaining
        start_time["Karanda"] = time.time()
        notified["Karanda"] = [False, False, False, True]


def notify_kutum():
    if not notified["Kutum"][3]:
        if channel is not None:
            asyncio.run_coroutine_threadsafe(channel.send("<@&605835798901817354> Kutum has spawned!"), loop)

        current_time = get_curent_time()

        time_remaining = check_remaining_time(kutum, current_time)
        kutum_timer = Timer(time_remaining, notify_kutum)
        kutum_timer.start()
        timers["Kutum"] = kutum_timer
        remaining_time["Kutum"] = time_remaining
        start_time["Kutum"] = time.time()
        notified["Kutum"] = [False, False, False, True]


def notify_kzarka():
    if not notified["Kzarka"][3]:
        if channel is not None:
            asyncio.run_coroutine_threadsafe(channel.send("<@&605835785907863601> Kzarka has spawned!"), loop)

        current_time = get_curent_time()

        time_remaining = check_remaining_time(kzarka, current_time)
        kzarka_timer = Timer(time_remaining, notify_kzarka)
        kzarka_timer.start()
        timers["Kzarka"] = kzarka_timer
        remaining_time["Kzarka"] = time_remaining
        start_time["Kzarka"] = time.time()
        notified["Kzarka"] = [False, False, False, True]


def notify_offin():
    if not notified["Offin"][3]:
        if channel is not None:
            asyncio.run_coroutine_threadsafe(channel.send("<@&605835946184802304> Offin has spawned!"), loop)

        current_time = get_curent_time()

        time_remaining = check_remaining_time(offin, current_time)
        offin_timer = Timer(time_remaining, notify_offin)
        offin_timer.start()
        timers["Offin"] = offin_timer
        remaining_time["Offin"] = time_remaining
        start_time["Offin"] = time.time()
        notified["Offin"] = [False, False, False, True]


def notify_nouver():
    if not notified["Nouver"][3]:
        if channel is not None:
            asyncio.run_coroutine_threadsafe(channel.send("<@&605835974693617664> Nouver has spawned!"), loop)

        current_time = get_curent_time()

        time_remaining = check_remaining_time(nouver, current_time)
        nouver_timer = Timer(time_remaining, notify_nouver)
        nouver_timer.start()
        timers["Nouver"] = nouver_timer
        remaining_time["Nouver"] = time_remaining
        start_time["Nouver"] = time.time()
        notified["Nouver"] = [False, False, False, True]


def notify_garmoth():
    if not notified["Garmoth"][3]:
        if channel is not None:
            asyncio.run_coroutine_threadsafe(channel.send("<@&605836079504818176> Garmoth has spawned!"), loop)

        current_time = get_curent_time()

        time_remaining = check_remaining_time(garmoth, current_time)
        garmoth_timer = Timer(time_remaining, notify_garmoth)
        garmoth_timer.start()
        timers["Garmoth"] = garmoth_timer
        remaining_time["Garmoth"] = time_remaining
        start_time["Garmoth"] = time.time()
        notified["Garmoth"] = [False, False, False, True]


def notify_quint_and_muraka():
    if not notified["Quint And Muraka"][3]:
        if channel is not None:
            asyncio.run_coroutine_threadsafe(channel.send("<@&605836116033273858> Quint and Muraka have spawned!"), loop)

        current_time = get_curent_time()

        time_remaining = check_remaining_time(quint_and_muraka, current_time)
        quint_and_muraka_timer = Timer(time_remaining, notify_quint_and_muraka)
        quint_and_muraka_timer.start()
        timers["Quint And Muraka"] = quint_and_muraka_timer
        remaining_time["Quint And Muraka"] = time_remaining
        start_time["Quint And Muraka"] = time.time()
        notified["Quint And Muraka"] = [False, False, False, True]


def notify_vell():
    if not notified["Vell"][3]:
        if channel is not None:
            asyncio.run_coroutine_threadsafe(channel.send("<@&605836162824929280> Vell has spawned"), loop)

        current_time = get_curent_time()

        time_remaining = check_remaining_time(vell, current_time)
        vell_timer = Timer(time_remaining, notify_vell)
        vell_timer.start()
        timers["Vell"] = vell_timer
        remaining_time["Vell"] = time_remaining
        start_time["Vell"] = time.time()
        notified["Vell"] = [False, False, False, True]


# spawn times in seconds for each boss
karanda = [900,     7200,   87300,  154800, 180000,
           205200,  252900, 346500, 363600, 388800,
           432900,  500400]
kutum = [900,     57600,  93600,  129600, 173700,
         230400,  266400, 291600, 327600, 378000,
         425700,  464400, 519300, 536400]
kzarka = [18000,  32400,  80100,  104400, 173700,
          190800, 252900, 316800, 346500, 414000,
          425700, 500400, 525600, 561600, 598500]
offin = [43200, 241200, 439200]
nouver = [68400,  144000, 260100, 277200, 302400,
          352800, 403200, 450000, 475200, 519300,
          561600, 598500]
garmoth = [166500, 339300, 586800]
quint_and_muraka = [256500, 489600]
vell = [576000]

mapping = {
    "Karanda": "<@&605835920477913090>",
    "Kutum": "<@&605835798901817354>",
    "Kzarka": "<@&605835785907863601>",
    "Offin": "<@&605835946184802304>",
    "Nouver": "<@&605835974693617664>",
    "Garmoth": "<@&605836079504818176>",
    "Quint And Muraka": "<@&605836116033273858>",
    "Vell": "<@&605836162824929280>"
}

timers = dict()
remaining_time = dict()
start_time = dict()

notified = dict()

channel = None
loop = asyncio.get_event_loop()


def initialise_timers(bot_channel):
    global channel
    channel = bot_channel

    current_time = get_curent_time()

    general = Timer(40, check_advanced_notice)
    general.start()
    timers["general"] = general

    time_remaining = check_remaining_time(karanda, current_time)
    karanda_timer = Timer(time_remaining, notify_karanda)
    karanda_timer.start()
    timers["Karanda"] = karanda_timer
    remaining_time["Karanda"] = time_remaining
    start_time["Karanda"] = time.time()
    notified["Karanda"] = [False, False, False, False]

    time_remaining = check_remaining_time(kutum, current_time)
    kutum_timer = Timer(time_remaining, notify_kutum)
    kutum_timer.start()
    timers["Kutum"] = kutum_timer
    remaining_time["Kutum"] = time_remaining
    start_time["Kutum"] = time.time()
    notified["Kutum"] = [False, False, False, False]

    time_remaining = check_remaining_time(kzarka, current_time)
    kzarka_timer = Timer(time_remaining, notify_kzarka)
    kzarka_timer.start()
    timers["Kzarka"] = kzarka_timer
    remaining_time["Kzarka"] = time_remaining
    start_time["Kzarka"] = time.time()
    notified["Kzarka"] = [False, False, False, False]

    time_remaining = check_remaining_time(offin, current_time)
    offin_timer = Timer(time_remaining, notify_offin)
    offin_timer.start()
    timers["Offin"] = offin_timer
    remaining_time["Offin"] = time_remaining
    start_time["Offin"] = time.time()
    notified["Offin"] = [False, False, False, False]

    time_remaining = check_remaining_time(nouver, current_time)
    nouver_timer = Timer(time_remaining, notify_nouver)
    nouver_timer.start()
    timers["Nouver"] = nouver_timer
    remaining_time["Nouver"] = time_remaining
    start_time["Nouver"] = time.time()
    notified["Nouver"] = [False, False, False, False]

    time_remaining = check_remaining_time(garmoth, current_time)
    garmoth_timer = Timer(time_remaining, notify_garmoth)
    garmoth_timer.start()
    timers["Garmoth"] = garmoth_timer
    remaining_time["Garmoth"] = time_remaining
    start_time["Garmoth"] = time.time()
    notified["Garmoth"] = [False, False, False, False]

    time_remaining = check_remaining_time(quint_and_muraka, current_time)
    quint_and_muraka_timer = Timer(time_remaining, notify_quint_and_muraka)
    quint_and_muraka_timer.start()
    timers["Quint And Muraka"] = quint_and_muraka_timer
    remaining_time["Quint And Muraka"] = time_remaining
    start_time["Quint And Muraka"] = time.time()
    notified["Quint And Muraka"] = [False, False, False, False]

    time_remaining = check_remaining_time(vell, current_time)
    vell_timer = Timer(time_remaining, notify_vell)
    vell_timer.start()
    timers["Vell"] = vell_timer
    remaining_time["Vell"] = time_remaining
    start_time["Vell"] = time.time()
    notified["Vell"] = [False, False, False, False]

    return


def check_remaining_time(boss_spawn_times, current_time):
    time_remaining = None
    for i in range(len(boss_spawn_times)):
        spawn_time = boss_spawn_times[i]
        if spawn_time > current_time and spawn_time-current_time > 7100:
            time_remaining = spawn_time - current_time
            break

    if time_remaining is None:
        time_remaining = 604800 - current_time + boss_spawn_times[0]

    return time_remaining


async def print_timers(spamchannel, boss=None):
    output = ""

    if boss is None:
        for key in remaining_time.keys():
            elapsed_time = floor(time.time() - start_time[key])
            elapsed_hours = floor(elapsed_time/60/60)
            elapsed_minutes = floor(elapsed_time/60) % 60
            elapsed_seconds = floor(elapsed_time) % 60
            remaining_time_for_boss = remaining_time[key]
            hours = floor((remaining_time_for_boss/60/60)) - elapsed_hours
            minutes = floor(remaining_time_for_boss/60 % 60) - elapsed_minutes
            seconds = remaining_time_for_boss % 60 - elapsed_seconds

            if seconds < 0:
                minutes -= 1
                seconds = 60 + seconds
            if minutes < 0:
                hours -= 1
                minutes = 60 + minutes

            output += "{} will spawn in {}:{}:{}\n".format(key, hours, minutes, seconds)
    else:
        boss = boss[0].capitalize() + boss[1:]
        elapsed_time = floor(time.time() - start_time[boss])
        elapsed_hours = floor(elapsed_time / 60 / 60)
        elapsed_minutes = floor(elapsed_time / 60) % 60
        elapsed_seconds = floor(elapsed_time) % 60
        remaining_time_for_boss = remaining_time[boss]
        hours = floor((remaining_time_for_boss / 60 / 60)) - elapsed_hours
        minutes = floor(remaining_time_for_boss / 60 % 60) - elapsed_minutes
        seconds = remaining_time_for_boss % 60 - elapsed_seconds

        if seconds < 0:
            minutes -= 1
            seconds = 60 + seconds
        if minutes < 0:
            hours -= 1
            minutes = 60 + minutes

        output += "{} will spawn in {}:{}:{}\n".format(boss, hours, minutes, seconds)
    await spamchannel.send(output)


def get_curent_time():
    now = datetime.utcnow()
    weekday = now.weekday()*24*60*60
    hours = (int(now.strftime("%H"))+2)*60*60
    minutes = int(now.strftime("%M"))*60
    seconds = int(now.strftime("%S"))
    current_time = (weekday + hours + minutes + seconds) % 604800
    return current_time
