import feedparser
import asyncio

from threading import Timer
from datetime import datetime

from Persistence import Persistence

news_and_anouncements = "https://community.blackdesertonline.com/index.php?forums/news-announcements.181/index.rss"
updates = "https://community.blackdesertonline.com/index.php?forums/patch-notes.5/index.rss"

refreshTimer = None
newsParser = feedparser.parse(news_and_anouncements)
updateParser = feedparser.parse(updates)

news_channel = None
update_channel = None

persistence = Persistence()

loop = asyncio.get_event_loop()

cast_months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


def check_for_updates():
    global refreshTimer
    refreshTimer = Timer(3600, check_for_updates)
    refreshTimer.start()

    new_news = list()
    new_updates = list()

    for entry in newsParser.entries:
        title = escape_special_characters(entry["title"])
        pubdate = entry["published"]
        pubdate = pubdate.split(",")[1]
        day = pubdate.split(" ")[1]
        month = pubdate.split(" ")[2]
        year = pubdate.split(" ")[3]
        hour = pubdate.split(" ")[4].split(":")[0]
        minute = pubdate.split(" ")[4].split(":")[1]
        second = pubdate.split(" ")[4].split(":")[2]
        pubdate = datetime(int(year), cast_months[month], int(day), int(hour), int(minute), int(second))
        if not persistence.see_if_news_exists(title, pubdate):
            new_news.insert(0, entry)
            persistence.add_news(title, pubdate)
        else:
            break

    for entry in new_news:
        output = entry["title"]
        output += "\n{}".format(entry["link"])
        asyncio.run_coroutine_threadsafe(news_channel.send(output), loop)

    for entry in updateParser.entries:
        title = escape_special_characters(entry["title"])
        pubdate = entry["published"]
        pubdate = pubdate.split(",")[1]
        day = pubdate.split(" ")[1]
        month = pubdate.split(" ")[2]
        year = pubdate.split(" ")[3]
        hour = pubdate.split(" ")[4].split(":")[0]
        minute = pubdate.split(" ")[4].split(":")[1]
        second = pubdate.split(" ")[4].split(":")[2]
        pubdate = datetime(int(year), cast_months[month], int(day), int(hour), int(minute), int(second))
        if not persistence.see_if_update_exists(title, pubdate):
            new_updates.insert(0, entry)
            persistence.add_update(title, pubdate)
        else:
            break

    for entry in new_updates:
        output = entry["title"]
        output += "\n{}".format(entry["link"])
        asyncio.run_coroutine_threadsafe(update_channel.send(output), loop)


def initialise_update_tracker(news, update):
    global refreshTimer
    refreshTimer = Timer(10, check_for_updates)
    refreshTimer.start()

    global news_channel
    news_channel = news

    global update_channel
    update_channel = update


def escape_special_characters(text):
    for index in reversed(range(len(text))):
        if text[index] == "'":
            text = text[:index] + "\\" + text[index:]
    return text
