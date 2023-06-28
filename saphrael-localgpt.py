import json
import discord
import pydle
import decks
import random
import pyimgur
import string
from PIL import Image
import os
import asyncio

from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")

with open("client_data.json", "r") as f:
  clientdata = json.load(f)

global wordlist
with open("words", "r") as f:
  wordlist = f.read().split("\n")


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


def render_celticcross(nick):
  cardwidth = 280
  cardheight = 417
  horizontalspace = 10
  verticalspace = 10

  squaresize = cardwidth * 2 + cardheight + horizontalspace * 4
  maxheight = cardheight * 4 + verticalspace * 5
  squareheight = (maxheight - squaresize) / 2

  image = Image.new("RGB", (squaresize + cardwidth + horizontalspace, maxheight), color=(0, 0, 0))

  cardfiles = ["thoth/{}.jpg".format(c) for c in random.sample(range(1, len(decks.THOTH)), 10)]
  cards = [Image.open(c) for c in cardfiles]

  image.paste(cards[0], (int(squaresize / 2 - cardwidth / 2), int(maxheight / 2 - cardheight / 2)))
  image.paste(cards[1].rotate(90, expand=True),
              (int(squaresize / 2 - cardheight / 2), int(maxheight / 2 - cardwidth / 2)))
  image.paste(cards[2], (int(squaresize / 2 - cardwidth / 2), int(maxheight - squareheight - cardheight / 2)))
  image.paste(cards[3], (int(horizontalspace), int(maxheight / 2 - cardheight / 2)))
  image.paste(cards[4], (int(squaresize / 2 - cardwidth / 2), int(squareheight - cardheight / 2)))
  image.paste(cards[5], (int(squaresize - horizontalspace - cardwidth), int(maxheight / 2 - cardheight / 2)))

  for i in range(4):
    image.paste(cards[6 + i], (int(squaresize), int(verticalspace + i * (cardheight + verticalspace))))

  image.save("{}.png".format(nick))
  return "{}.png".format(nick)


def load_discord_image(filename):
  discordimage = discord.File(filename)
  return discordimage


def load_irc_image(filename):
  imgurclient = pyimgur.Imgur(clientdata["imgurid"])
  upload = imgurclient.upload_image(os.path.join(os.getcwd(), filename))
  return upload.link


def containsflag(message, flag):
  msg = message.lower()
  if flag in msg:
    if msg.index(flag) > 0:
      if msg[msg.index(flag) - 1].isalnum():
        return False
    try:
      if msg[msg.index(flag) + len(flag)].isalnum():
        return False
    except IndexError:
      pass
    return True
  return False


class BaseRead:
  def __init__(self, query, user):
    self.text = ""
    if containsflag(query, "words"):
      self.gen_words()
      return
    if containsflag(query, "celtic cross"):
      self.gen_celticcross(user)
      return
    if containsflag(query, "yes/no"):
      self.gen_binary(user)
      return

    if containsflag(query, "haindl"):
      deck = decks.HAINDL
    elif containsflag(query, "rw"):
      deck = decks.RW_DECK
    elif containsflag(query, "servants"):
      deck = decks.SERVANTS_DECK
    elif containsflag(query, "rune"):
      deck = decks.ELDER_FUTHARK
    else:
      deck = decks.THOTH

    if containsflag(query, "explain-gpt"):
        if containsflag(query, "spread"):
            cards = random.sample(deck, 3)
            text = "{0}, {1}, and {2}".format(*[x[0] for x in cards])
        else:
            card = random.choice(deck)
            text = card[0]
        query = query.replace("explain-gpt", "").strip()
        prompt = """In a divination server, a lunar angel able to see the future by the name of Saphrael was bound to a machine so that it could speak through it. The angel is powerful, wise and helpful, and tries to help people by telling the future of any query given through tarot, and explaining in detail the symbology and qabalistic interactions.
A querent named {2} comes, and asks: "{0}". 
Saphrael ponders, and pulls cards from their magical thoth tarot deck. The cards they pull are {1}.
Saphraels tries to explain the qabalistic interaction between the cards, and how they answer the query, responding to {2} with: """.format(query, text, user)
        print(prompt)
        chatbot.reset_chat()
        chatbot.refresh_session()
        interpretation = chatbot.get_chat_response(prompt)['message']
        self.text = "{}".format(interpretation)
        print(self.text)
    else:
        if containsflag(query, "spread"):
            self.gen_spread(deck)
        else:
            self.gen_single(deck)

  def gen_words(self):
    nwords = random.randint(1, 5)
    self.text = " ".join([random.choice(wordlist) for n in range(nwords)]).capitalize()
    self.text += "."

  def gen_binary(self, user):
    self.text = random.choices(['Yes', 'No', 'Maybe'], weights=[3, 3, 2])[0]

  def gen_single(self, deck): pass
  def gen_spread(self, deck): pass
  def gen_celticcross(self, user): pass
  def render(self, user, noprefix=False): pass


class IRCRead(BaseRead):
  def gen_single(self, deck):
    card = random.choice(deck)
    self.text = "{0} {{ {1} }}".format(*card)

  def gen_spread(self, deck):
    cards = random.sample(deck, 3)
    self.text = ", ".join("{0} {{ {1} }}".format(*card) for card in cards)

  def gen_celticcross(self, user):
    filename = render_celticcross(random.choices(string.ascii_uppercase, k=10))
    imgurclient = pyimgur.Imgur(clientdata["imgurid"])
    upload = imgurclient.upload_image(os.path.join(os.getcwd(), filename))
    self.text = "Cast cards: {0} (Meanings: https://goo.gl/ZEwmwd )".format(upload.link)
    os.remove(filename)

  def render(self, user, noprefix=False):
    if noprefix:
      return self.text
    else:
      return "{0}: {1}".format(user, self.text)


class DiscordRead(BaseRead):
  def __init__(self, query):
    self.image = None
    super().__init__(query.content, query.author.display_name)

  def gen_single(self, deck):
    card = random.choice(deck)
    self.text = "{0} <{1}>".format(*card)

  def gen_spread(self, deck):
    cards = random.sample(deck, 3)
    self.text = "\n".join("{0} <{1}>".format(*card) for card in cards)

  def gen_celticcross(self, user):
    filename = render_celticcross(random.choices(string.ascii_uppercase, k=10))
    discordimage = discord.File(filename)
    self.image = discordimage
    self.text = "(Meanings: <https://goo.gl/ZEwmwd>)"
    os.remove(filename)

  def render(self, user, noprefix=False):
    if noprefix:
      text = "{0}: {1}".format(user.mention, self.text)
    else:
      text = self.text
    return text, self.image


class DiscordClient(discord.Client):
  async def on_message(self, message):
    if containsflag(message.content, "saphrael") or containsflag(message.content, "saph") \
      or self.user.mentioned_in(message=message) or isinstance(message.channel, discord.DMChannel) \
      and not message.author.bot:
      try:
        read = DiscordRead(message)
        response, image = read.render(message.author)
        if image:
          await message.channel.send(response, file=image)
        else:
          await message.channel.send(response)
      except discord.errors.Forbidden:
        pass

class IRCClient(pydle.Client):
  def __init__(self, reset_function):
    super(IRCClient, self).__init__(nickname='Saphrael', realname='Saphrael')
    self.RECONNECT_MAX_ATTEMPTS = None
    self.reset_function = reset_function

  async def on_connect(self):
    await self.join('#/div/ination')

  async def on_data_error(self, exception):
    await super(IRCClient, self).on_data_error(exception)
    self.reset_function(self)

  async def on_channel_message(self, channel, nick, message):
    if "saph" in message.lower():
      read = IRCRead(message, nick)
      await self.message(channel, read.render(nick))

  async def on_private_message(self, target, nick, message):
    if nick != "Saphrael":
      read = IRCRead(message, nick)
      await self.message(nick, read.render(nick, noprefix=True))

#loop = asyncio.get_event_loop()
discordclient = DiscordClient()
discordclient.run(clientdata["token"])

#def reset_function(client):
#  asyncio.ensure_future(client.connect('irc.us.sorcery.net', 6667), loop=loop)

#ircclient = IRCClient(reset_function)

#reset_function(ircclient)
#asyncio.ensure_future(discordclient.start(clientdata["token"]), loop=loop)
#try:
#  loop.run_forever()
#except KeyboardInterrupt:
#  loop.run_until_complete(discordclient.logout())
#finally:
#  loop.close()
