import json,random

from requests import get

import logging,requests


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def areyoubored():
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

    response = requests.get("https://www.boredapi.com/api/activity",headers=headers)
    
    return (json.loads(response.text))
def showRandomImages(type):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    if "nsfw" in type:
        catlist=["waifu", "neko", "trap", "blowjob"]
    else:
        catlist=["glomp","slap","kill","happy","wink","poke","dance","cringe"]
    cat=random.choice(catlist)
    response = requests.get("https://api.waifu.pics/"+type+"/"+cat,headers=headers)

    return (json.loads(response.text))
