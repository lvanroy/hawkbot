import feedparser
import asyncio

from threading import Timer
from datetime import datetime

from Persistence import Persistence

news_and_anouncements = "https://community.blackdesertonline.com/index.php?forums/news-announcements.181/index.rss"
updates = "https://community.blackdesertonline.com/index.php?forums/patch-notes.5/index.rss"

refreshTimer = None

news_channel = None
update_channel = None

persistence = Persistence()

loop = asyncio.get_event_loop()


def check_for_updates():    
    newsParser = feedparser.parse(news_and_anouncements)
    updateParser = feedparser.parse(updates)


    print("update refresh\n")
    global refreshTimer
    refreshTimer = Timer(86400, check_for_updates)
    refreshTimer.start()

    new_news = list()
    new_updates = list()

    for entry in newsParser.entries:
        title = escape_special_characters(entry["title"])
        url = escape_special_characters(entry["link"])
        if not persistence.see_if_news_exists(title, url):
            new_news.insert(0, entry)
            persistence.add_news(title, url)
        else:
            break

    for entry in new_news:
        output = entry["title"]
        output += "\n{}".format(entry["link"])
        asyncio.run_coroutine_threadsafe(news_channel.send(output), loop)

    for entry in updateParser.entries:
        title = escape_special_characters(entry["title"])
        url = escape_special_characters(entry["link"])
        if not persistence.see_if_update_exists(title, url):
            new_updates.insert(0, entry)
            persistence.add_update(title, url)
        else:
            break

    for entry in new_updates:
        output = entry["title"]
        output += "\n{}".format(entry["link"])
        asyncio.run_coroutine_threadsafe(update_channel.send(output), loop)


def initialise_update_tracker(news, update):
    global refreshTimer
    refreshTimer = Timer(60, check_for_updates)
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
