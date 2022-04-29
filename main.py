from time import sleep
import requests
import json
from PIL import Image, ImageDraw, ImageFont
import textwrap
from instabot import Bot
import datetime
import os 
import time
import glob



url = "https://zenquotes.io/api/random"
W, H = (1920,1080)
bot = Bot()


def calcTomorrowDate():
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    return int(tomorrow.strftime("%d"))
def calcTodayDate():
    today = datetime.datetime.now()
    return int(today.strftime("%d"))


def generateQuote():
    response = requests.get(url)
    final = json.loads(response.text)
    #print(final[0]['q'])
    #print(final[0]['a'])

    return final[0]['q']



def generateQuoteImage():
    global bot
    bot.login(username = "remove this and enter username",password = "remove this and enter password") #put your username and password
    m = generateQuote()
    para = textwrap.wrap(m, width=70)

    msg = para

    im = Image.new("RGB",(W,H),"yellow")
    draw = ImageDraw.Draw(im)
    myFont = ImageFont.truetype("libre.ttf", 40)
    w, h = draw.textsize(para[0], font = myFont)
    current_h, pad = (H-h)/2, 10
    for line in para:
        w, h = draw.textsize(line, font = myFont)
        draw.text(((W-w)/2,current_h), line,align='center', fill="black",font=myFont)
        current_h += h + pad

    im.save("fin.jpg", "JPEG")

    bot.upload_photo("fin.jpg", caption = m )
    bot.logout()
    
    
if __name__ == "__main__":

    try:
        cookie_del = glob.glob("config/*cookie.json")
        os.remove(cookie_del[0])
        os.remove('fin.jpg.REMOVE_ME')
        
    except:
        pass
    
    mode = input("1 for posting now \n2 for scheduled posting \n>>")
    if mode == "1":
        generateQuoteImage()

    elif mode == "2":
        today = calcTodayDate()
        tomorrow = calcTomorrowDate()
        generateQuoteImage()
        while True:
            if today == tomorrow:
                generateQuoteImage()
                tomorrow = calcTomorrowDate()
            else:
                today = calcTodayDate()
                time.sleep(60*60*2)
