from fbchat import *
import pickle
from fbchat.models import *
username = input("Enter username: ")
password = input("Enter password: ")
client = Client(username, password)
print('Your id: ', client.uid)
while True:
    user = input("Enter name of user to Search for: ")
    users = client.searchForUsers(user)
    user = users[0]
    print("User's ID: {}".format(user.uid))
    print("User's name: {}".format(user.name))
    print("User's profile picture url: {}".format(user.photo))
    print("User's main url: {}".format(user.url))
    c = input("Continue?(y/n):")
    if c.lower() != 'y':
        break
