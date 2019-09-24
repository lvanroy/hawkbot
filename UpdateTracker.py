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

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


def check_for_updates():
    print("expire")
    global refreshTimer
    refreshTimer = Timer(3600, check_for_updates)
    refreshTimer.start()

    new_news = list()
    new_updates = list()

    for entry in newsParser.entries:
        title = entry["title"]
        pubdate = entry["published"]
        pubdate = pubdate.split(",")[1]
        day = pubdate.split(" ")[0]
        month = pubdate.split(" ")[1]
        year = pubdate.split(" ")[2]
        hour = pubdate.split(" ")[3].split(":")[0]
        minute = pubdate.split(" ")[3].split(":")[1]
        second = pubdate.split(" ")[3].split(":")[2]
        pubdate = datetime(year, month, day, hour, minute, second)
        if not persistence.see_if_news_exists(title, pubdate):
            new_news.insert(0, entry)
            persistence.add_news(title, pubdate)
        else:
            break

    for entry in reversed(new_news):
        output = entry["title"]
        output += "\n[more here]({})".format(entry["link"])
        asyncio.run_coroutine_threadsafe(news_channel.send(output), loop)

    for entry in updateParser.entries:
        title = entry["title"]
        pubdate = entry["published"]
        pubdate = pubdate.split(",")[1]
        day = pubdate.split(" ")[0]
        month = pubdate.split(" ")[1]
        year = pubdate.split(" ")[2]
        hour = pubdate.split(" ")[3].split(":")[0]
        minute = pubdate.split(" ")[3].split(":")[1]
        second = pubdate.split(" ")[3].split(":")[2]
        pubdate = datetime(year, month, day, hour, minute, second)
        if not persistence.see_if_update_exists(title, pubdate):
            new_updates.insert(0, entry)
            persistence.add_update(title, pubdate)
        else:
            break

    for entry in reversed(new_updates):
        output = entry["title"]
        output += "\n[more here]({})".format(entry["link"])
        asyncio.run_coroutine_threadsafe(update_channel.send(output), loop)
        

def initialise_update_tracker(news, update):
    global refreshTimer
    refreshTimer = Timer(10, check_for_updates)
    refreshTimer.start()

    global news_channel
    news_channel = news

    global update_channel
    update_channel = update
