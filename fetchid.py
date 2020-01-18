from fbchat import *
import pickle
from fbchat.models import *
with open("storeddata.dat","rb") as f:
    d = pickle.load(f)
    print(d["sayed"])
    print(d)
client = Client('hameel12@hotmail.com', 'blamelamelame')
print('Hameel:', client.uid)
users = client.searchForUsers('Sayed Muhsin')
user = users[0]
print("User's ID: {}".format(user.uid))
print("User's name: {}".format(user.name))
print("User's profile picture url: {}".format(user.photo))
print("User's main url: {}".format(user.url))
users = client.searchForUsers('Mohammed Zeeshan')
user = users[0]
print("User's ID: {}".format(user.uid))
print("User's name: {}".format(user.name))
print("User's profile picture url: {}".format(user.photo))
print("User's main url: {}".format(user.url))
users = client.searchForUsers('이종석')
user = users[0]
print("User's ID: {}".format(user.uid))
print("User's name: {}".format(user.name))
print("User's profile picture url: {}".format(user.photo))
print("User's main url: {}".format(user.url))