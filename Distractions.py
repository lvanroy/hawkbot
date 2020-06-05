import requests as req
import json


def get_joke_categories():
    r = req.get("https://sv443.net/jokeapi/v2/categories")
    result = "The available categories are: \n"
    for category in json.loads(r.text)["categories"]:
        result += "\t{}\n".format(category)
    return result


def get_joke(category):
    r = req.get("https://sv443.net/jokeapi/v2/joke/{}".format(category))
    data = json.loads(r.text)
    if data["type"] == "single":
        return data["joke"]
    else:
        return "{}\n{}".format(data["setup"], data["delivery"])
