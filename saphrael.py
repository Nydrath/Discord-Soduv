import json
import discord
import pydle
import asyncio
import decks
import random
from tornado.platform.asyncio import AsyncIOMainLoop
AsyncIOMainLoop().install()

with open("client_data.json", "r") as f:
    clientdata = json.load(f)

                                                                                                                                                                                                        
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
    if "rw" in message:
        deck = decks.RW_DECK
    elif "rune" in message:
        deck = decks.RUNES
    else:
        deck = decks.THOTH
    if "spread" in message:
        return random.sample(deck, 3)
    else:
        return [random.choice(deck)]


# Discord

discordclient = discord.Client()

@discordclient.event
@asyncio.coroutine
async def on_message(message):
    if "saphrael" in message.content.lower() or discordclient.user.mention in message.content or isinstance(message.channel, discord.PrivateChannel) and not message.author.bot:
        yield from discordclient.send_message(message.channel, message.author.mention+": "+" ".join([card[0]+" <"+card[1]+">" for card in pullcard(message.content)]))


# IRC

# Simple echo bot.
class IRCSoduv(pydle.Client):
    def on_connect(self):
         self.join('#/div/ination')

    def on_message(self, source, target, message):
         if "saphrael" in message.lower() or target == source:
            self.message(source, target+": "+" ".join([card[0]+" { "+card[1]+" }" for card in pullcard(message)]))

ircclient = IRCSoduv('Saphrael', realname='Saphrael')
ircclient.connect('irc.us.sorcery.net', 6667)
discordclient.run(clientdata["token"])
