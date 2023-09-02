import os
import time
class Setup:

    @staticmethod 
    def CheckConfig():
        setting1 = []
        settings = json.load(open("Input/settings.json", encoding="utf-8"))
        for setting in settings:
            setting1.append(setting)

        setting2 = []
        for settin2 in setting1:
            setting2.append(settin2)

    @staticmethod
    def WriteFile():
        with open("Storage/settings.json", "a") as file:
            file.write("""{
    "Proxy": {
        "Use_Proxy": false
    },
    "Captcha": {
        "Api": 4,
        "Captcha_key": ""
    },
    "General": {
        "hide_token": true
    },
    "Guild": {
        "bypass_membership_screening": true
    },
    "User": {
        "solvecaptcha_on_friendreq": true,
        "friend_delay": true,
        "delay": 10
    },
    "Advanced": {
        "tls_client": true,
        "JA3": ""
    }, 
    "Developer": {
        "debug": false
    }
}""")
            file.close()

        with open("Input/message.json", "a") as file:
            file.write("""{
    "content": "Hello, Join https://t.me/faded_changelog"
}""")
            file.close()

    @staticmethod
    def folders() -> None:
        if os.path.exists("Input/"):
            pass
        else:
            os.makedirs("Input/")

        if os.path.exists("Storage/"):
            pass
        else:
            os.makedirs("Storage/")

        if os.path.exists("Output/"):
            pass
        else:
            os.makedirs("Output/")

        if os.path.exists("Input/Avatars/"):
            pass
        else:
            os.makedirs("Input/Avatars/")

    @staticmethod
    def Files():
        Setup.folders()
        time.sleep(1)

        if os.path.isfile("Input/bios.txt"):
            pass
        else:
            open("Input/bios.txt", "a+")
            Setup.WriteFile()

        if os.path.isfile("Input/invalid.txt"):
            pass
        else:
            open("Input/invalid.txt", "a+")

        if os.path.isfile("Input/invites.txt"):
            pass
        else:
            open("Input/invites.txt", "a+")

        if os.path.isfile("Input/locked.txt"):
            pass
        else:
            open("Input/locked.txt", "a+")

        if os.path.isfile("Input/memberids.txt"):
            pass
        else:
            open("Input/memberids.txt", "a+")

        if os.path.isfile("Input/message.json"):
            pass
        else:
            open("Input/message.json", "a+")

        if os.path.isfile("Input/proxies.txt"):
            pass
        else:
            open("Input/proxies.txt", "a+")

        if os.path.isfile("Input/serverids.txt"):
            pass
        else:
            open("Input/serverids.txt", "a+")

        if os.path.isfile("Input/tokens.txt"):
            pass
        else:
            open("Input/tokens.txt", "a+")

        if os.path.isfile("Input/valid.txt"):
            pass
        else:
            open("Input/valid.txt", "a+")

        if os.path.isfile("Output/tokens.txt"):
            pass
        else:
            open("Output/tokens.txt", "a+")

        if os.path.isfile("Output/used.txt"):
            pass
        else:
            open("Output/used.txt", "a+")

        if os.path.isfile("Storage/settings.json"):
            pass
        else:
            open("Storage/settings.json", "a+")

Setup().Files()
# makes sure config is there as required in all Modules 
import json
from captchatools import new_harvester
import threading
import ctypes
from pystyle import Write, Colors, Colorate
import random
import time
from keyauth import *
import pwinput
from datetime import datetime
from capmonster_python import HCaptchaTask
import sys
from discum.utils.slash import SlashCommander
from websocket import WebSocket
from veilcord import VeilCord
from Modules import guild, misc, captcha 
from Modules import account as acc
from tls_client import exceptions
from keyauth import exceptions 

# client = Keyauth(
#     name="Faded Discord",
#     owner_id="obj0mnfh5V",
#     secret="d115567aa6df88a6ec3c78fefa8e4e355b82eccea593bb339c38b1fea2cb3bb2",
#     version="1.4",
#     file_hash=None
# )

username = "ADMIN"

class Faded:
    def __init__(self):
        self.config = json.load(open("Storage/settings.json", encoding="utf-8"))
        # self.expiry = client.user.expires
        # if self.expiry == None:
        #     self.expiry = "LIFETIME"
        # else:
        #     self.expiry = int(client.user.expires / 60 / 60 / 60) + "Days"
        self.threads = []
        self.expiry = "LIFETIME"

    def run_joiner(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Joiner | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        choic = Write.Input("Join Multiple Servers (Y/N) > ", Colors.red_to_purple, interval=0.0025)
        delay = float(Write.Input("Delay > ", Colors.red_to_purple, interval=0.0025))
        bst = str(Write.Input("Boost Server On Join Y/N > ", Colors.red_to_purple, interval=0.0025))
        if bst.lower() == "y":
            boost = True
        else:
            boost = False
        setnick = str(Write.Input("Set Nickname On Join Y/N > ", Colors.red_to_purple, interval=0.0025))
        if setnick.lower() == "y":
            nickname = str(Write.Input("Nickname > ", Colors.red_to_purple, interval=0.0025))
        else:
            nickname = None 
        if choic in ["Y", "y"]:
            with open("Input/invites.txt", "r") as f:
                invites = f.read().splitlines()
        elif choic in ["N", "n"]:
            invite = Write.Input("https://discord.gg/", Colors.red_to_purple)
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
            for token in tokens:
                    if ":" in token:
                        token = token.split(":")[2]
                    else:
                        token = token
                    time.sleep(delay)
                    if choic in ["Y", "y"]:
                        for invite in invites:
                            t = threading.Thread(target=guild.Join, args=(invite, token, boost, nickname)).start()
                    elif choic in ["N", "n"]:
                        t = threading.Thread(target=guild.Join, args=(invite, token, boost, nickname)).start()
        print(Colorate.Horizontal(Colors.red_to_purple, f"(*) Press Enter To Return To Menu"))
        input()

    def run_checker(self):
        # Checker
        if sys.platform == 'darwin':
            sys.stdout.write('\x1b]2;Faded | Checker\x07')
        else:
            ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Checker | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            t = threading.Thread(target=acc.Check, args=(token, ))
            t.start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Finished Checking Tokens", True))
        input()

    def run_leaver(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Leaver | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        opts = Write.Input("Leave Multiply Servers (Y/N) > ", Colors.red_to_purple, interval=0.0025)
        delay = Write.Input("Delay > ", Colors.red_to_purple, interval=0.0025)
        if opts in ["N", "n"]:
            srverid = Write.Input("Server ID > ", Colors.red_to_purple, interval=0.0025)
            srverid = int(srverid)
        elif opts in ["Y", "y"]:
            with open("Input/serverids.txt", "r") as f:
                srverids = f.read().splitlines()
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            if ":" in token:
                token = token.split(":")[2]
            else:
                token = token
            if opts == "Y":
                for srverid in srverids:
                    srverid = int(srverid)
                    time.sleep(delay)
                    t = threading.Thread(target=guild.Leaver, args=(token, srverid)).start()
            else:
                t = threading.Thread(target=guild.Leaver, args=(token, srverid)).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_booster(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Booster | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        serverid = Write.Input("Server ID > ", Colors.red_to_purple)
        serverid = int(serverid)
        boosts = Write.Input("Amount Of Boosts > ", Colors.red_to_purple)
        boosts = int(boosts)
        tokens_used = int(boosts / 2)
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for i in range(tokens_used):
            token = tokens[i]
            if ":" in token:
                token = token.split(":")[2]
            else:
                token = token
            threading.Thread(target=guild.Boost, args=(token, serverid)).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_bio(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Bio Changer | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            if ':' in token:
                token = token.split(':')[2]
            else:
                token = token 
            threading.Thread(target=acc.ChangeBio, args=(token, )).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_password(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Password Changer | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        new_password = Write.Input("New Password > ", Colors.red_to_purple)
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            threading.Thread(target=acc.ChangePassword, args=(token, new_password)).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()
        
    def run_boostchecker(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Boost Checker | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            threading.Thread(target=acc.NitroCheck, args=(token, )).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_guildfetcher(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Guild Fetcher | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            if ":" in token:
                token = token.split(":")[2]
            else:
                token = token
            threading.Thread(target=guild.CancelBoosts, args=(token, )).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_pfp(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded PFP Changer | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            if ":" in token:
                token = token.split(":")[2]
            else:
                token = token 
            threading.Thread(target=acc.ChangePfp, args=(token, )).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_format(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Formatter | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        misc.Utils.Format()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_resetfiles(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded | Resetting Files | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        misc.ResetFiles()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_resetconfig(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded | Resetting Config | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        misc.ResetConfig()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_viewsettings(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded | Viewing Settings | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        capkey = self.config["Captcha"]["Captcha_key"]
        ja3 = self.config["Advanced"]["JA3"]
        config = json.load(open("Storage/settings.json", encoding="utf-8"))
        if len(ja3) > 30:
            ja = ja3[:30] + "*********************************************"
        else:
            ja = ja3
        print(Colorate.Horizontal(Colors.yellow_to_red, config, True))
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()
    def run_massdm(self):
        if username != "MerkzCo":
            print(Colorate.Horizontal(Colors.rainbow, f"(*) In Development Now!"))
        else:
            with open("Input/memberids.txt", "r") as f:
                ids = f.read().splitlines()
            for user in ids:
                with open("Input/tokens.txt", "r") as f:
                    tokens = f.read().splitlines()
                amounttokens = len(tokens)
                amounttokens = amounttokens - 1
                token = tokens[random.randint(0, amounttokens)]
                if ":" in token:
                    token = token.split(":")[2]
                else:
                    token = token 
                threading.Thread(target=guild.CreateChannel, args=(token, user)).start()
            print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
            input()

    def run_channelspam(self):
            ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Raid Tool | Channel Spammer | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
            messagee = Write.Input("Message > ", Colors.rainbow)
            massment = Write.Input("Mass Mention (Y/N) > ", Colors.rainbow)
            channelid = Write.Input("Channel ID > ", Colors.rainbow)
            amount = Write.Input("Amount Of Messages > ", Colors.rainbow)
            amount = int(amount)
            channelid = int(channelid)

            with open("Input/tokens.txt", "r") as f:
                tokens = f.read().splitlines()
            for i in range(amount):
                token = random.choice(tokens)
                if ":" in token:
                    token = token.split(":")[2]
                else:
                    token = token 

                if massment in ["Y", "y"]:
                    with open("Input/memberids.txt", "r") as f:
                        ids = f.read().splitlines()

                    mes = []
                    message = ""

                    for idss in ids:
                        mes.append(idss)

                    for idsss in mes:
                        if len(message) > 400:
                            pass
                        else:
                            message = message + f"<@{idsss}> "
                    message = message + messagee
                    time.sleep(0.05)
                    threading.Thread(target=guild.SendChannelMessage, args=(token, channelid, message)).start()
                else:
                    time.sleep(0.05)
                    threading.Thread(target=guild.SendChannelMessage, args=(token, channelid, messagee)).start()
            print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
            input()
    
    def run_friendrequest(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Raid Tool | Friend Request Spammer | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        optionss = Write.Input("Send To Multiple IDS (Y/N) > ", Colors.rainbow)
        if optionss in ["Y", "y"]:
            with open("Input/memberids.txt", "r") as f:
                idss = f.read().splitlines()
        else:
            friendid = Write.Input("User ID > ", Colors.rainbow)
        if optionss in ["Y", "y"]:
            for ids in idss:
                if self.config["User"]["friend_delay"]:
                    time.sleep(self.config["User"]["delay"])
                    with open("Input/tokens.txt", "r") as f:
                        tokens = f.read().splitlines()
                    token = random.choice(tokens)
                    if ":" in token:
                        token = token.split(":")[2]
                    else:
                        token = token 
                    threading.Thread(target=acc.SendFriendRequest, args=(token, ids)).start()
                else:
                    with open("Input/tokens.txt", "r") as f:
                        tokens = f.read().splitlines()
                    token = random.choice(tokens)
                    if ":" in token:
                        token = token.split(":")[2]
                    else:
                        token = token 
                    threading.Thread(target=acc.SendFriendRequest, args=(token, ids)).start()
        elif optionss in ["N", "n"]:
            with open("Input/tokens.txt", "r") as f:
                tokens = f.read().splitlines()
            for token in tokens:
                if ":" in token:
                    token = token.split(":")[2]
                else:
                    token = token
                threading.Thread(target=acc.SendFriendRequest, args=(token, friendid)).start()
        else:
            print("Invalid Input...")
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_vcspam(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Raid Tool | VC Spammer | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        guildid = Write.Input("Guild ID > ", Colors.rainbow)
        channelid = Write.Input("Channel ID > ", Colors.rainbow)
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            if ":" in token:
                token = token.split(":")[2]
            else:
                token = token 
            threading.Thread(target=guild.VcSpammer, args=(token, guildid, channelid)).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

    def run_userchanger(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Username Changer | t.me/faded_changelog | Logged In As: {username} | Expires: {self.expiry}")
        uername = Write.Input("Username > ", Colors.rainbow)
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            if ":" in token:
                tken = token.split(":")[2]
                password = token.split(":")[1]
            else:
                tken = token 
                password = None 
            threading.Thread(target=acc.UsernameChanger, args=(tken, password, uername)).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()
    
    def run_housechanger(self):
        with open("Input/tokens.txt", "r") as f:
            tokens = f.read().splitlines()
        for token in tokens:
            if ':' in token:
                token = token.split(":")[2]
            else:
                token = token
            
            threading.Thread(target=acc.HouseChanger, args=(token, )).start()
        print(Colorate.Horizontal(Colors.purple_to_blue, f"(*) Press Enter To Return To Menu", True))
        input()

def run():
    if sys.platform == 'win32':
        os.system('cls')
    elif sys.platform == 'darwin':
        os.system('clear')
    username = "ADMIN"
    if sys.platform == 'darwin':
        sys.stdout.write(f'\x1b]2;Faded | t.me/faded_changelog | Logged In As: {username}\x07')
    else:
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded | t.me/faded_changelog | Logged In As: {username} ")

    banner = f"""
 /$$$$$$$$             /$$                 /$$
| $$_____/            | $$                | $$
| $$    /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$$
| $$$$$|____  $$ /$$__  $$ /$$__  $$ /$$__  $$
| $$__/ /$$$$$$$| $$  | $$| $$$$$$$$| $$  | $$
| $$   /$$__  $$| $$  | $$| $$_____/| $$  | $$
| $$  |  $$$$$$$|  $$$$$$$|  $$$$$$$|  $$$$$$$
|__/   \_______/ \_______/ \_______/ \_______/ 

Web Loader Now Out! https://keyauth.cc/panel/MerkzCo/Faded+Discord

[01] Joiner          [02] Checker          [03] Leaver

[04] Booster         [05] Bio Changer      [06] Password Changer

[07] Boost Checker   [08] Guild Fetcher    [09] Pfp Changer

[10] Formatter       [11] Reset Files      [12] Reset Config

[13] View Settings   [14] Mass DM          [15] Raid Tool

[16] Emoji Verify    [17] Username Changer [18] Hypesquad Changer

[19] Exit

    """
    print(Colorate.Horizontal(Colors.yellow_to_red, banner, True))
    opt = Write.Input("Select > ", Colors.red_to_purple, interval=0.0025)
    if opt in ["1", "01"]:
        Faded().run_joiner()
    elif opt in ["2", "02"]:
        Faded().run_checker()
    elif opt in ["3", "03"]:
        Faded().run_leaver()
    elif opt in ["4", "04"]:
        Faded().run_booster()
    elif opt in ["5", "05"]:
        Faded().run_bio()
    elif opt in ["6", "06"]:
        Faded().run_password()
    elif opt in ["7", "07"]:
        Faded().run_boostchecker()
    elif opt in ["8", "08"]:
        Faded().run_guildfetcher()
    elif opt in ["9", "09"]:
        Faded().run_pfp()
    elif opt == "10":
        Faded().run_format()
    elif opt == "11":
        Faded().run_resetfiles()
    elif opt == "12":
        Faded().run_resetconfig()
    elif opt == "13":
        Faded().run_viewsettings()
    elif opt == "14":
        Faded().run_massdm()
    elif opt == "15":
        if sys.platform == 'win32':
            os.system('cls')
        elif sys.platform == 'darwin':
            os.system('clear')
        banner = """
 /$$$$$$$$             /$$                 /$$                
| $$_____/            | $$                | $$          /$$   
| $$    /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$$         | $$   
| $$$$$|____  $$ /$$__  $$ /$$__  $$ /$$__  $$       /$$$$$$$$
| $$__/ /$$$$$$$| $$  | $$| $$$$$$$$| $$  | $$      |__  $$__/
| $$   /$$__  $$| $$  | $$| $$_____/| $$  | $$         | $$   
| $$  |  $$$$$$$|  $$$$$$$|  $$$$$$$|  $$$$$$$         |__/   
|__/   \_______/ \_______/ \_______/ \_______/                
                                                              
[01] Channel Spammer   [02] Friend Request Spammer   [3] VC Spammer

[04] Exit Program
 
"""
        ctypes.windll.kernel32.SetConsoleTitleW(f"Faded Raid Tool | t.me/faded_changelog | Logged In As: {username}")
        print(Colorate.Diagonal(Colors.yellow_to_red, banner, True))
        inp = Write.Input("Select > ", Colors.red_to_purple, interval=0.0025)
        if inp in ["1", "01"]:
            Faded().run_channelspam()
        elif inp in ["2", "02"]:
            Faded().run_friendrequest()
        elif inp in ["3", "03"]:
            Faded().run_vcspam()
        elif inp in ["4", "04"]:
            print("Exiting...")
            time.sleep(3)
            os._exit(1)
        else:
            print("Please Enter Valid Input... Closing")
            time.sleep(5)
            os.system("exit")
    elif opt == "16":
        if username != "ADMIN":
            print('Coming Next Update!')
        else:
            pass
        time.sleep(10)
    elif opt == '17':
        Faded().run_userchanger()
    elif opt == '18':
        Faded().run_housechanger()
    elif opt == '19':
        print('Exiting...')
        time.sleep(3)
        os._exit(1)
    else:
        print("Please Enter Valid Input... Returning to main menu!")
        time.sleep(5)


# if __name__ == '__main__':
#         try:
#             if sys.platform == 'win32':
#                 os.system('cls')
#             elif sys.platform == 'darwin':
#                 os.system('clear')
#             if os.path.isfile("Storage/account.json"):
#                 account = json.load(open("Storage/account.json", encoding="utf-8"))
#                 if "username" and "password" in account:
#                     username = account["username"]
#                     password = account["password"]
#                     client.login(username, password)
#                 else:
#                     username = None
#                     password = None
#                     client.login(username, password)
#             else:
#                 try:
#                     banner = """
#   /$$$$$$             /$$      /$$
#  /$$__  $$           | $$     | $$
# | $$  \ $$ /$$   /$$ /$$$$$$  | $$$$$$$
# | $$$$$$$$| $$  | $$|_  $$_/  | $$__  $$
# | $$__  $$| $$  | $$  | $$    | $$  \ $$
# | $$  | $$| $$  | $$  | $$ /$$| $$  | $$
# | $$  | $$|  $$$$$$/  |  $$$$/| $$  | $$
# |__/  |__/ \______/    \___/  |__/  |__/

# [1] Login   [2] Register   [3] Exit Program
#             """
#                     print(Colorate.Vertical(Colors.purple_to_red, f"{banner}", True))
#                     option = Write.Input("Select > ", Colors.red_to_purple)
#                     if option == "1":
#                         reply = client.login(
#                             username=input("Username > "),
#                             password=pwinput.pwinput("Password > ")
#                         )
#                         if os.path.isfile("Storage/account.json"):
#                             pass
#                         else:
#                             with open("Storage/account.json", "w") as f:
#                                 f.write("""{
#     "username": "",
#     "password": ""
# }""")
#                     elif option == "2":
#                         reply = client.register(
#                             username=input("Username > "),
#                             password=pwinput.pwinput("Password > "),
#                             license_key=pwinput.pwinput("Licence > ")
#                         )
#                         with open("Storage/account.json", "w") as f:
#                             f.write("""{
#     "username": "",
#     "password": ""
# }""")
#                             f.close()
#                     elif option == "3":
#                         os._exit(1)
#                 except KeyboardInterrupt:
#                     os._exit(1)
#         except Exception as err:
#             print(err)

#         while True:
#             run()