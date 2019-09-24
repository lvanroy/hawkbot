import feedparser

from threading import Timer

from datetime import datetime

news_and_anouncements = "https://community.blackdesertonline.com/index.php?forums/news-announcements.181/index.rss"
updates = "https://community.blackdesertonline.com/index.php?forums/patch-notes.5/index.rss"

refreshTimer = None
newsParser = feedparser.parse(news_and_anouncements)
updateParser = feedparser.parse(updates)

last_news_update = datetime.now()
last_update_update = datetime.now()

news_channel = None
update_channel = None


def check_for_updates():
    print("expire")
    global refreshTimer
    refreshTimer = Timer(3600, check_for_updates)
    refreshTimer.start()

    new_news = list()
    new_updates = list()

    for entry in newsParser.entries:
        pubdate = entry["pubDate"]
        pubdate = pubdate.split(",")[1]
        day = pubdate.split(" ")[0]
        month = pubdate.split(" ")[1]
        year = pubdate.split(" ")[2]
        hour = pubdate.split(" ")[3].split(":")[0]
        minute = pubdate.split(" ")[3].split(":")[1]
        second = pubdate.split(" ")[3].split(":")[2]
        pubdate = datetime(year, month, day, hour, minute, second)
        if pubdate > last_news_update:
            new_news.insert(0, entry)
        else:
            break

    for entry in updateParser.entries:
        pubdate = entry["pubDate"]
        pubdate = pubdate.split(",")[1]
        day = pubdate.split(" ")[0]
        month = pubdate.split(" ")[1]
        year = pubdate.split(" ")[2]
        hour = pubdate.split(" ")[3].split(":")[0]
        minute = pubdate.split(" ")[3].split(":")[1]
        second = pubdate.split(" ")[3].split(":")[2]
        pubdate = datetime(year, month, day, hour, minute, second)
        if pubdate > last_update_update:
            new_updates.insert(0, entry)
        else:
            break



def initialise_update_tracker(news, update):
    global refreshTimer
    refreshTimer = Timer(10, check_for_updates)
    refreshTimer.start()

    global news_channel
    news_channel = news

    global update_channel
    update_channel = update
