import requests as req
import json
from os import system, listdir
from random import choice

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

def get_meme(category):
    system('cd ../skraper-master;./skraper ninegag /{} -t json -n 100'.format(category))
    file = listdir('../skraper-master/ninegag')
    f = open("../skraper-master/ninegag/{}".format(file[0]))
    data = json.load(f)
    f.close()
    system('rm ../skraper-master/ninegag/*')
    selection = data[choice(range(len(data)))]
    return "{}\n{}".format(selection["text"], selection["media"][0]["url"])
