import json
import discord
import pydle
import asyncio
import decks
import random
import randomorg
import pyimgur
import math
from PIL import Image
import os
from tornado.platform.asyncio import AsyncIOMainLoop
AsyncIOMainLoop().install()

with open("client_data.json", "r") as f:
    clientdata = json.load(f)

imagenamecounter = 0

#         O. ,8.     ~N. +:     .D: Z$ .N= 7N                .N  $D   .ZI    ID:  .Z, :I.               .8, ,D.          +=..7:               .?~ .D,  .OMO:         :7..N~               ,8?OM.        
#         N  .I.     ?D  ,?.    .7. =D .O. ,N                .Z  :N  .MI      IM. ,N  .MMMMMMMMMMMMMMM, ,?.  NIZMM,      $.  ,+               .Z.  N=  Z, .Z.        +:  OI               Z$  =~        
#         .DM$,       .DM?       ,IM:   :8MMD                .MMM7. .$:        =+  .NMN.    =M.     .Z,  +NMN.    :MI     8MMM:               .+DMM.   O, .$.         7MM,               ,MM~IM.        
#          $M          +M          M.      .~D:             ,8.     ,D.        ,$.          =M.     .Z,            ~N,       .N:              8Z       .NMND$         ,N,              .MM. ,.          
#          8D          +M          N,        .=8          .?=.      ,8:    7.  .O.          =M.     .Z,             .N~        =N,          .N.              8M.      :N,            ?M?                
#          DD          +M          D,          =O,        D$         =D,   Z:  .$.          =M.     .Z,              N$         .NO        :D.                .MN.    :N,          :DZ,                 
#          N8          +M          D,           .=Z.    .N.           .+MMM.   ~=           =M.     .Z,              7N           .M.    .I~.                    7M~  =M.        :M,                    
#          DN          +M          N,            .MM.  ~N.                    .7,           =M.     .Z,              +M            +M$   N7                        8Z,+M.    N++M8.       .=O+8,        
#          7M.         +M         .M.           IN  =$7~                      =N            =M.     .Z,              =M          .I~ .N$N                           .~MM.   ,I  +MMMMMMMMMMM  .O.       
#          ~M.         +M         .M           :7.   =N,                      8Z            =M.     .Z,              =M.         D7   .=O                             7M    .M~:M?        .7$:Z:        
#          .?Z.        +M        .7I         .+=       =N,                   .O.            =M.     .Z,              =M.       +N.      .NO                           OM                  N8            
#           .M?        +M        =M.         8Z         .N.                  $:             =M.     .Z,              =M.      ,Z.        .=Z.                         N8                .$+.            
#            =M:       +M       .M?        =N.            =N.               ,D              =M.     .Z,              =M.    .=+            .=Z        ,$             ,N:               ,N:              
#             :M.      +M      ,8=.      .,$.              .NZ .          .,D:              =M.     .Z,              =M.  ..O$               =Z...     M.           .Z~               .M.               
#              .MM.    +M     7D:     .O. ,O.               .+~ .N:     ?~ .7,              =M.     .Z,              =M..O  8O                +N  ?:   ,M?         ,M+            .8, .8                
#               .?MN.  +M   IM8       ,D. .D,               .$.  N+     Z.  :~              =M.     .Z,              =M.,?  ?D                $O  :+    ?M?.     .+M.             .7. .N                
#                   ,ZDMMN$=           .OMO.                  7MD.       7ND+               =M.     .Z,              =M. ~MM:.                 ,NM+       .+NMM8$.                 :ZMO.                
                                                                                                                                                                                                       

def pullcard(message):
    if "trng" in message.lower():
#        try:
            random.seed(randomorg.rrandom())
#        except:
#            return ["The maximum number of true random queries for the day has been exceeded", ""]
    if "sigilize" in message.lower():
        return [["Finished sigil: ", drawsigil()]]
    if "celtic cross" in message.lower():
        return [["Cast cards: ", celticcross()]]
    if "rw" in message.lower():
        deck = decks.RW_DECK
    elif "rune" in message.lower():
        deck = decks.RUNES
    else:
        deck = decks.THOTH
    if "spread" in message.lower():
        return random.sample(deck, 3)
    else:
        return [random.choice(deck)]


# Discord

discordclient = discord.Client()

@discordclient.event
@asyncio.coroutine
def on_message(message):
    if "saph" in message.content.lower() or discordclient.user.mention in message.content or isinstance(message.channel, discord.PrivateChannel) and not message.author.bot:
        try:
            yield from discordclient.send_message(message.channel, message.author.mention+": "+" ".join([card[0]+" <"+card[1]+">" for card in pullcard(message.content)]))
        except discord.errors.Forbidden:
            pass


# IRC

# Simple echo bot.
class IRCSoduv(pydle.Client):
    def on_connect(self):
         self.join('#/div/ination')

    def on_channel_message(self, channel, nick, message):
         if "saph" in message.lower():
            self.message(channel, nick+": "+" ".join([card[0]+" { "+card[1]+" }" for card in pullcard(message)]))

    def on_private_message(self, nick, message):
        self.message(nick, " ".join([card[0]+" { "+card[1]+" }" for card in pullcard(message)]))

ircclient = IRCSoduv('Saphrael', realname='Saphrael')
ircclient.connect('irc.us.sorcery.net', 6667)


# Celtic cross spread

def celticcross():
    cardwidth = 280
    cardheight = 417
    horizontalspace = 10
    verticalspace = 10

    squaresize = cardwidth*2 + cardheight + horizontalspace*4
    maxheight = cardheight*4 + verticalspace*5
    squareheight = (maxheight - squaresize)/2

    image = Image.new("RGB", (squaresize + cardwidth + horizontalspace, maxheight), color=(0, 0, 0))

    cardfiles = ["thoth/{}.jpg".format(c) for c in random.sample(range(1, len(decks.THOTH)), 10)]
    cards = [Image.open(c) for c in cardfiles]

    image.paste(cards[0], (int(squaresize/2-cardwidth/2), int(maxheight/2-cardheight/2)))
    image.paste(cards[1].rotate(90, expand=True), (int(squaresize/2-cardheight/2), int(maxheight/2-cardwidth/2)))
    image.paste(cards[2], (int(squaresize/2-cardwidth/2), int(maxheight-squareheight-cardheight/2)))
    image.paste(cards[3], (int(horizontalspace), int(maxheight/2-cardheight/2)))
    image.paste(cards[4], (int(squaresize/2-cardwidth/2), int(squareheight-cardheight/2)))
    image.paste(cards[5], (int(squaresize-horizontalspace-cardwidth), int(maxheight/2-cardheight/2)))

    for i in range(4):
        image.paste(cards[6+i], (int(squaresize), int(verticalspace + i*(cardheight+verticalspace))))

    global imagenamecounter
    image.save("{}.png".format(imagenamecounter))
    imgurclient = pyimgur.Imgur(clientdata["imgurid"])
    upload = imgurclient.upload_image(os.getcwd()+"/{}.png".format(imagenamecounter))
    os.remove(os.getcwd()+"/{}.png".format(imagenamecounter))
    imagenamecounter += 1
    return upload.link

discordclient.run(clientdata["token"])
