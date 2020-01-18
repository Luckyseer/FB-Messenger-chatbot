# Author - Hameel Babu Rasheed
# Just a simple python facebook messenger bot made for my friend group. Hastily put together, not meant for serious
# stuff. Be careful with the username and password if you're using this!
from fbchat import *
from fbchat.models import *
import random
import datetime
import time
import pickle
username = input("Enter your username(Email Address): ")
password = input("Enter your password: ")
client = Client(username, password)
thread_id =''  # Enter the thread_id of the group here. You can find the thread id in the URL on PC in messenger
thread_type = ThreadType.GROUP
done = False
# I hard coded it for 4 users specifically because that's how many our group had.
# I'll probably make this better and more scalable later.
user1 = ''  # Enter the user_ids, can be gotten by running the 'fetchid' script
user2 = ''
user3 = ''
user4 = ''  # If you're in the group, this should be your id
version = '1.3.1'  # Uploaded it pretty late on github
rng = random.SystemRandom()
greetings = ["Hello", "Hi", "Hey there", "Greetings"]
rejections = ["Ew.", "No thank you.", "Thanks for the offer but I\'ll pass.", "Umm.. Let\'s just stay as friends.",
              "Gross.", "No.", "Nope", "Can you not?"]
gratitude = ["Don't mention it.", "Ok.", "You're welcome I guess..", "K.", "Sure.", "Mhm."]
randomstuff = ["Yes?", "How can I help you?", "You called?", "Did you call me?", "Do you need something?"]
sleepmode = False
blackjackmode = False
smuglist = ["smug.png", "smug2.jpg", "smug3.jpg", "smug4.png", "smug5.jpg", "smug6.jpg", "smug7.jpg"]
commandlist = ['!roll - Rolls a d6', '!roll d<x> - Rolls a d<x> Replace <x> with a number',
               '!give <person> <x> - Gives <person> <x> money', '!balance - Checks remaining money.',
               '!kick<person> - Kicks person from group', '!add<person> - Adds person to group',
               '!addall - Adds everybody to the group', '!kick<person> - Kicks persons from group',
               '!time - Tells the local time.(For the bot)', '!version - Tells the current version of the bot',
               '!sleep - Bot goes to sleep', '!smug - smug', '!blackjack - Plays a game of blackjack',
               '!exit - Exits the bot remotely']
b_list = ['b1.gif', 'b2.gif', 'b3.gif']
commands = ""
pasta = "Nani the fuck did omae just fucking say about me, you little bitch? atashi’ll have omae know atashi graduated top of watashi no class in the Bot Army, and watashi have been involved in numerous secret raids on Al-Weeba, and atashi have over 300 confirmed kicks. atashi am trained in anime warfare and atashi wa the top sniper in the entire JAPAN armed forces. omae are nothing to me but just another target. atashi will wipe omae the fuck out with precision the likes of which has never been seen before on this facebook group, mark my fucking words. omae think you can get away with saying that shit to me over the atashinternet? Think again, fucker. As we speak atashi am contacting my secret network of bots across japan and omaer atashiP is being traced right now so omae better prepare for the storm, maggot. The storm that wipes out the pathetic little thing omae call omaer life. you’re fucking dead, kid. atashi can be anywhere, anytime, and atashi can kill omae in over seven hundred ways, and that’s just with my bare hands. Not only am atashi extensively trained in unarmed combat, but atashi have access to the entire arsenal of the Japanese Marine Corps and atashi will use it to its full extent to wipe your miserable ass off the face of the continent, omae little shit. if only omae could have known nani unholy retribution your little “clever” comment was about to bring down upon omae, maybe omae would have held your fucking tongue. But omae couldn’t, omae didn’t, and now you’re paying the price, omae goddamn baka. atashi will shit fury all over omae and omae will drown in it. you’re fucking dead, kiddo."
for i in commandlist:
    commands += i + '\n'


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


face_cards = ['King', 'Jack', 'Queen']


class BlackJack:
    """Simple blackjack game. One deck. """
    #   Has a weird/wrong interaction when you have more than one ace. It should be fine usually but in specific cases
    #   the score wil be wrong. I'll fix it soon
    def __init__(self):
        self.suits = ['♥️', '♦️', '♠️', '♣️ ']
        self.values = ['Ace', 'King', 'Jack', 'Queen', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.deck = [Card(suit, value) for value in self.values for suit in self.suits]
        self.players = []
        self.player_hand = []
        self.dealer_hand = []
        self.player_score = 0
        self.ace_count = 0  # No. of Aces.
        self.dealer_score = 0
        self.new_game = True
        self.player_bust = False
        self.stand_mode = False
        self.multiple_aces = False

    def deal_player(self):
        num = random.randrange(len(self.deck))
        if self.deck[num].value == 'Ace':
            self.player_hand.append(self.deck[num])
        else:
            self.player_hand.insert(0, self.deck[num])  # To make calculation of score simpler.
        self.deck.pop(num)

    def dealer_draw(self):
        num = random.randrange(len(self.deck))
        if self.deck[num].value == 'Ace':
            self.dealer_hand.append(self.deck[num])  # Just to make calculation of score simpler.
        else:
            self.dealer_hand.insert(0, self.deck[num])
        self.deck.pop(num)

    def new_deck(self):
        self.deck = [Card(suit, value) for value in self.values for suit in self.suits]

    def reset(self):
        self.player_bust = False
        self.new_deck()
        self.stand_mode = False
        self.multiple_aces = False
        self.player_hand = []
        self.dealer_hand = []

    def calculate_player_score(self):
        self.player_score = 0
        self.ace_count = 0
        for card in self.player_hand:
            if card.value in face_cards:
                self.player_score += 10
            elif card.value != 'Ace':
                self.player_score += int(card.value)
            elif card.value == 'Ace':
                self.ace_count += 1
                if self.player_score + 11 > 21 or self.ace_count > 1:
                    self.player_score += 1
                else:
                    self.player_score += 11

    def calculate_dealer_score(self):
        self.dealer_score = 0
        self.ace_count = 0
        for card in self.dealer_hand:
            if card.value in face_cards:
                self.dealer_score += 10
            elif card.value != 'Ace':
                self.dealer_score += int(card.value)
            elif card.value == 'Ace':
                self.ace_count += 1
                if self.dealer_score + 11 > 21 or (
                        self.dealer_score + 11 > 17 and self.dealer_score < self.player_score <= 21) or self.ace_count > 1:
                    self.dealer_score += 1
                else:
                    self.dealer_score += 11

    def display_player_hand(self, player):
        client.send(Message(text='@%s\'s Current hand:' % player.name), thread_id=thread_id,
                    thread_type=thread_type)
        for card in self.player_hand:
            client.send(Message(text='%s %s' % (card.suit, card.value)), thread_id=thread_id,
                        thread_type=thread_type)
        client.send(Message(text='Score: %s' % self.player_score), thread_id=thread_id,
                    thread_type=thread_type)

    def display_dealer_hand(self):
        client.send(Message(text='Dealer\'s Current hand:'), thread_id=thread_id,
                    thread_type=thread_type)
        for card in self.dealer_hand:
            client.send(Message(text='%s %s' % (card.suit, card.value)), thread_id=thread_id,
                        thread_type=thread_type)
        client.send(Message(text='Score: %s' % self.dealer_score), thread_id=thread_id,
                    thread_type=thread_type)

    def start_game(self, player, message):
        if self.new_game:
            client.send(Message(text='Welcome! I will be your dealer today!'), thread_id=thread_id, thread_type=thread_type)
            time.sleep(2)
            client.send(Message(text='First I will be dealing your cards @%s' % player.name), thread_id=thread_id,
                        thread_type=thread_type)
            time.sleep(2)
            self.deal_player()
            self.calculate_player_score()
            self.display_player_hand(player)
            self.dealer_draw()
            time.sleep(2)
            self.calculate_dealer_score()
            self.display_dealer_hand()
            time.sleep(2)
            self.deal_player()
            self.calculate_player_score()
            self.display_player_hand(player)
            client.send(Message(text='Now, would you like to !hit or !stand ?'), thread_id=thread_id,
                        thread_type=thread_type)
            self.new_game = False
        if not self.new_game:
            if message == '!hit' and not self.stand_mode:
                self.deal_player()
                self.calculate_player_score()
                self.display_player_hand(player)
                time.sleep(1)
                if self.player_score > 21:
                    client.send(Message(text='Unfortunately you busted! @%s' % player.name),
                                thread_id=thread_id,
                                thread_type=thread_type)
                    self.stand_mode = True
                    self.player_bust = True
            elif message == '!stand' and not self.stand_mode:
                client.send(Message(text='Alright I will now draw the cards!'), thread_id=thread_id,
                            thread_type=thread_type)
                self.stand_mode = True
                time.sleep(1)
            elif message == '!continue':
                self.new_game = True
        if self.stand_mode:
            if self.dealer_score < 17:
                time.sleep(1)
                self.dealer_draw()
                self.calculate_dealer_score()
                self.display_dealer_hand()
            if self.dealer_score >= 17 and self.dealer_score <= 21:
                if (self.dealer_score < self.player_score) and not self.player_bust:
                    client.send(Message(text='%s wins!' % player.name), thread_id=thread_id,
                                thread_type=thread_type)
                else:
                    client.send(Message(text='The dealer wins!'), thread_id=thread_id,
                                thread_type=thread_type)
                self.reset()
                client.send(Message(text='If you want to play again do !continue.'), thread_id=thread_id,
                            thread_type=thread_type)
            elif self.dealer_score > 21:
                if not self.player_bust:
                    client.send(Message(text='The dealer busted, %s wins!' % player.name), thread_id=thread_id,
                                thread_type=thread_type)
                else:
                    client.send(Message(text='The dealer busted, Nobody wins!'), thread_id=thread_id,
                                thread_type=thread_type)
                self.reset()
                client.send(Message(text='If you want to play again do !continue.'), thread_id=thread_id,
                            thread_type=thread_type)


blackjack = BlackJack()


while not done:
    messages = client.fetchThreadMessages(thread_id=thread_id, limit=1)
    if not sleepmode:
        for message in messages:
            if message.text == '!roll':
                dice = rng.randrange(1, 7)
                user_id = message.author
                user = client.fetchUserInfo(user_id)['%s' % user_id]
                client.send(Message(text='@%s Rolled %d!🎲' % (user.name, dice), mentions=[Mention(thread_id, offset=0, length=len(user.name)+1)]), thread_id=thread_id, thread_type=thread_type)
            if type(message.text) == type(user1):   # checking if its a str
                if message.text[0:7] == '!roll d':
                    try:
                        lim = int(message.text[7:]) + 1
                    except:
                        lim = 7
                    dice = rng.randrange(1, lim)
                    user_id = message.author
                    user = client.fetchUserInfo(user_id)['%s' % user_id]
                    client.send(Message(text='@%s Rolled %d! (d%d)🎲' % (user.name, dice, lim-1), mentions=[Mention(thread_id, offset=0, length=len(user.name)+1)]), thread_id=thread_id, thread_type=thread_type)
                elif message.text[0:5] == '!give':
                    if message.text[6:10] == 'bala':
                        recipient = user1
                        receiver = 'bala'
                        leng = 10
                    elif message.text[6:11] == 'sayed':
                        recipient = user2
                        receiver = 'sayed'
                        leng = 11
                    elif message.text[6:13] == 'user3':
                        recipient = user3
                        receiver = 'user3'
                        leng = 13
                    elif message.text[6:12] == 'user4':
                        recipient = user4
                        receiver = 'user4'
                        leng = 12
                    else:
                        break
                    user_id = message.author
                    user = client.fetchUserInfo(user_id)['%s' % user_id]
                    try:
                        amount = int(message.text[leng:])
                    except:
                        amount = 0
                    if user_id == recipient:
                        client.send(Message(text='You can\'t give money to yourself!'), thread_id=thread_id, thread_type=thread_type)
                    elif user_id == user1:
                        with open("storeddata.dat", "rb") as f:
                            d = pickle.load(f)
                            if d['bala'] < amount:
                                client.send(Message(text='You dont have enough money! @%s' % user.name), thread_id=thread_id,
                                            thread_type=thread_type)
                            else:
                                d[receiver] = d[receiver] + amount
                                d['bala'] -= amount
                                client.send(Message(text='@%s gave %s %d$' % (user.name, receiver, amount), mentions=[Mention(thread_id, offset=0, length=len(user.name) + 1)]),
                                            thread_id=thread_id,
                                            thread_type=thread_type)
                        with open("storeddata.dat", "wb") as f:
                            pickle.dump(d, f)
                    elif user_id == user2:
                        with open("storeddata.dat", "rb") as f:
                            d = pickle.load(f)
                            if d['sayed'] < amount:
                                client.send(Message(text='You dont have enough money! @%s' % user.name), thread_id=thread_id,
                                            thread_type=thread_type)
                            else:
                                d[receiver] = d[receiver] + amount
                                d['sayed'] -= amount
                                client.send(Message(text='@%s gave %s %d$' % (user.name, receiver, amount), mentions=[Mention(thread_id, offset=0, length=len(user.name) + 1)]),
                                            thread_id=thread_id,
                                            thread_type=thread_type)
                        with open("storeddata.dat", "wb") as f:
                            pickle.dump(d, f)
                    elif user_id == user3:
                        with open("storeddata.dat", "rb") as f:
                            d = pickle.load(f)
                            if d['zeeshan'] < amount:
                                client.send(Message(text='You dont have enough money! @%s' % user.name), thread_id=thread_id,
                                            thread_type=thread_type)
                            else:
                                d[receiver] = d[receiver] + amount
                                d['zeeshan'] -= amount
                                client.send(Message(text='@%s gave %s %d$' % (user.name, receiver, amount), mentions=[Mention(thread_id, offset=0, length=len(user.name) + 1)]),
                                            thread_id=thread_id,
                                            thread_type=thread_type)
                        with open("storeddata.dat", "wb") as f:
                            pickle.dump(d, f)
                    elif user_id == user4:
                        with open("storeddata.dat", "rb") as f:
                            d = pickle.load(f)
                            if d['hameel'] < amount:
                                client.send(Message(text='You dont have enough money! @%s' % user.name), thread_id=thread_id,
                                            thread_type=thread_type)
                            else:
                                d[receiver] = d[receiver] + amount
                                d['hameel'] -= amount
                                client.send(Message(text='@%s gave %s %d$' % (user.name, receiver, amount), mentions=[Mention(thread_id, offset=0, length=len(user.name) + 1)]),
                                            thread_id=thread_id,
                                            thread_type=thread_type)
                        with open("storeddata.dat", "wb") as f:
                            pickle.dump(d, f)

            if message.text == '!kickbala':
                if message.author == user4:
                    try:
                        client.send(Message(text='Kicking Bala!'), thread_id=thread_id, thread_type=thread_type)
                        client.removeUserFromGroup(user1, thread_id=thread_id)
                    except:
                        print("Couldn't kick Bala!")
                else:
                    client.send(Message(text='Only my master can do that command!'), thread_id=thread_id, thread_type=thread_type)
            if message.text == '!kicksayed':
                if message.author == user4:
                    try:
                        client.send(Message(text='Kicking Sayed!'), thread_id=thread_id, thread_type=thread_type)
                        client.removeUserFromGroup(user2, thread_id=thread_id)
                    except:
                        print('Couldn\'t kick Sayed!')
                else:
                    client.send(Message(text='Only my master can do that command!'), thread_id=thread_id, thread_type=thread_type)
            if message.text == '!kickzeeshan':
                if message.author == user4:
                    try:
                        client.send(Message(text='Kicking Zeeshan!'), thread_id=thread_id, thread_type=thread_type)
                        client.removeUserFromGroup(user3, thread_id=thread_id)
                    except:
                        print('Couldn\'t kick Zeeshan!')
                else:
                    client.send(Message(text='Only my master can do that command!'), thread_id=thread_id, thread_type=thread_type)
            if message.text == '!kickall':
                if message.author == user4:
                    try:
                        client.send(Message(text='Kicking Everyone!!'), thread_id=thread_id, thread_type=thread_type)
                        client.removeUserFromGroup(user3, thread_id=thread_id)
                    except:
                        print('Couldn\'t kick Zeeshan!')
                    try:
                        client.removeUserFromGroup(user2, thread_id=thread_id)
                    except:
                        print('Couldn\'t kick Sayed!')
                    try:
                        client.removeUserFromGroup(user1, thread_id=thread_id)
                    except:
                        print("Couldn't kick Bala!")
                else:
                    client.send(Message(text='Only my master can do that command!'), thread_id=thread_id, thread_type=thread_type)

            if message.text == '!addall':
                try:
                    client.send(Message(text='Adding all!'), thread_id=thread_id, thread_type=thread_type)
                    client.addUsersToGroup([user1], thread_id=thread_id)
                except:
                    print("couldn\'t add bala!")
                try:
                    client.addUsersToGroup([user3], thread_id=thread_id)
                except:
                    print("couldn\'t add user3!")
                try:
                    client.addUsersToGroup([user2], thread_id=thread_id)
                except:
                    print("couldn\'t add sayed!")
            if message.text == '!addbala':
                try:
                    client.send(Message(text='Adding Bala!'), thread_id=thread_id, thread_type=thread_type)
                    client.addUsersToGroup([user1], thread_id=thread_id)
                except:
                    print("couldn\'t add bala")
            if message.text == '!addsayed':
                try:
                    client.send(Message(text='Adding Sayed!'), thread_id=thread_id, thread_type=thread_type)
                    client.addUsersToGroup([user2], thread_id=thread_id)
                except:
                    print("couldn\'t add Sayed")
            if message.text == '!addzeeshan':
                try:
                    client.send(Message(text='Adding Zeeshan!'), thread_id=thread_id, thread_type=thread_type)
                    client.addUsersToGroup([user3], thread_id=thread_id)
                except:
                    print("couldn\'t add Zeeshan")
            if message.text == '!kickhameel':
                if message.author == user4:
                    client.send(Message(text='I can\'t kick my master!'), thread_id=thread_id, thread_type=thread_type)
                else:
                    user_id = message.author
                    user = client.fetchUserInfo(user_id)['%s' % user_id]
                    client.send(Message(text='Nice try @%s !' % (user.name),
                                        mentions=[Mention(thread_id, offset=9, length=len(user.name) + 1)]),
                                thread_id=thread_id, thread_type=thread_type)
            if message.text == '!time':
                currentDT = datetime.datetime.now() # It'll be the time on the system the script is running on.
                client.send(Message(text='IST: %s' % currentDT.strftime("%I:%M:%S %p")), thread_id=thread_id, thread_type=thread_type)
            if message.text == '!balance':
                user_id = message.author
                user = client.fetchUserInfo(user_id)['%s' % user_id]
                datafile = open("storeddata.dat", "rb")
                d = pickle.load(datafile)
                datafile.close()
                if user_id == user1:
                    balance = d["bala"]
                elif user_id == user2:
                    balance = d["sayed"]
                elif user_id == user3:
                    balance = d["zeeshan"]
                elif user_id == user4:
                    balance = d["hameel"]
                else:
                    balance = 0
                client.send(Message(text='@%s has %d$!' % (user.name, balance),
                                    mentions=[Mention(thread_id, offset=0, length=len(user.name) + 1)]),
                            thread_id=thread_id, thread_type=thread_type)
            if '@Bot Chan' in str(message.text):  # jokes and generic responses to a mention.
                user_id = message.author
                user = client.fetchUserInfo(user_id)['%s' % user_id]
                if "hey" in message.text.lower() or "hi" in message.text.lower():
                    rand = random.randrange(0, len(greetings) - 1)
                    client.send(Message(text='@%s %s!' % (user.name, greetings[rand]),
                                        mentions=[Mention(thread_id, offset=0, length=len(user.name) + 1)]),
                                thread_id=thread_id, thread_type=thread_type)
                elif "marry me" in message.text.lower() or "love" in message.text.lower():
                    rand = random.randrange(0, len(rejections) - 1)
                    client.send(Message(text='%s @%s' % (rejections[rand], user.name),
                                        mentions=[Mention(thread_id, offset=len(rejections[rand])+1, length=len(user.name) + 1)]),
                                thread_id=thread_id, thread_type=thread_type)
                elif "thank" in message.text.lower() or "ty" in message.text.lower():
                    rand = random.randrange(0, len(gratitude) - 1)
                    client.send(Message(text='%s @%s' % (gratitude[rand], user.name),
                                        mentions=[Mention(thread_id, offset=len(rejections[rand])+1, length=len(user.name) + 1)]),
                                thread_id=thread_id, thread_type=thread_type)
                else:
                    rand = random.randrange(0, len(randomstuff) - 1)
                    client.send(Message(text='@%s %s' % (user.name, randomstuff[rand]),
                                        mentions=[Mention(thread_id, offset=0, length=len(user.name) + 1)]),
                                thread_id=thread_id, thread_type=thread_type)
            if message.text == '!sleep':
                client.send(Message(text='Going to sleep💤! Wake me up by typing !wakeup and wait for approximately a minute without sending any other messages!'), thread_id=thread_id, thread_type=thread_type)
                sleepmode = True
            if message.text == '!version':
                client.send(Message(text='Current version: %s' % version), thread_id=thread_id, thread_type=thread_type)
            if str(message.text)[0:4] == '!bet':
                user_id = message.author
                user = client.fetchUserInfo(user_id)['%s' % user_id]
                try:
                    amount = int(message.text[4:])
                except:
                    client.send(Message(text='Please enter a valid amount @%s!' % user.name), thread_id=thread_id,
                                thread_type=thread_type)
            if message.text == '!blackjack':
                if not blackjackmode:
                    client.send(Message(text='Let\'s play some blackjack!, !blackjackoff after you\'re done.'), thread_id=thread_id,
                                thread_type=thread_type)
                    bjplayer = message.author
                    bjuser = client.fetchUserInfo(bjplayer)['%s' % bjplayer]
                    blackjackmode = True
                else:
                    client.send(Message(text='We\'re already playing blackjack!'), thread_id=thread_id, thread_type=thread_type)
            if message.text == '!blackjackoff':
                client.send(Message(text='Switching off blackjack mode!'), thread_id=thread_id,
                            thread_type=thread_type)
                blackjackmode = False
                blackjack.reset()
                blackjack.new_game = True
            if message.text == '!smug':
                try:
                    smug_img = smuglist[random.randrange(len(smuglist) - 1)]
                    client.sendLocalImage('smug/%s' % smug_img,
                                      thread_id=thread_id, thread_type=thread_type)
                except:
                    print("Could not send !smug image")
            if str(message.text[0:9]) == '!birthday':
                birthday_boy = message.text[10:].capitalize()
                try:
                    birthday_img = b_list[random.randrange(len(b_list) - 1)]
                    client.sendLocalImage('gifs/%s' % birthday_img, message=Message(text='Happy birthday %s!' % birthday_boy),
                                      thread_id=thread_id, thread_type=thread_type)
                except:
                    print("Could not send image.")
            if message.text == '!triggered':
                client.send(Message(text='*breathes in*'), thread_id=thread_id,
                            thread_type=thread_type)
                time.sleep(2)
                client.send(Message(text=pasta), thread_id=thread_id,
                            thread_type=thread_type)

            if message.text == '!cmdlist':
                client.send(Message(text=commands), thread_id=thread_id, thread_type=thread_type)
            if message.text == '!exit':
                print("exiting..")
                client.send(Message(text='Exiting!'), thread_id=thread_id, thread_type=thread_type)
                done = True

    if sleepmode:  # didn't want to waste data.
        for message in messages:
            if message.text == "!wakeup":
                client.send(Message(text='Waking up!'), thread_id=thread_id, thread_type=thread_type)
                sleepmode = False
                break
            time.sleep(40)

    if blackjackmode:
        for message in messages:
            blackjack.start_game(bjuser, message.text)


