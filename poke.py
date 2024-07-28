import os
import sys
import time
import requests
from colorama import *
from datetime import datetime
import json
import random
import urllib.parse

red = Fore.LIGHTRED_EX
yellow = Fore.LIGHTYELLOW_EX
green = Fore.LIGHTGREEN_EX
black = Fore.LIGHTBLACK_EX
blue = Fore.LIGHTBLUE_EX
white = Fore.LIGHTWHITE_EX
meganta = Fore.MAGENTA
reset = Style.RESET_ALL

rcolor = (red, blue, green, meganta)
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full paths to the files
data_file = os.path.join(script_dir, "data.txt")


class PokeyQuest:
    def __init__(self):
        # Menampilkan logo
        print(r"""
 __  __      __                   __                         
/\ \/\ \    /\ \                 /\ \                        
\ \ `\\ \   \_\ \     __     _ __\ \ \____     __     __     
 \ \ , ` \  /'_` \  /'__`\  /\`'__\ \ '__`\  /'__`\ /'_ `\   
  \ \ \`\ \/\ \L\ \/\ \L\.\_\ \ \/ \ \ \L\ \/\  __//\ \L\ \  
   \ \_\ \_\ \___,_\ \__/.\_\\ \_\  \ \_,__/\ \____\ \____ \
    \/\/_/\/__,_ /\/__/\/_/ \/\/   \/___/  \/____/\/___L\ \
                                                      /\_____/
                                                      \/__/ .bot
        """)
        print(f"{Fore.GREEN}PokeyQuest{Fore.RESET}\n")

        self.auto_do_task = input(f"{yellow}Pakai Auto Lakukan Tugas? (y/n): ").lower() == 'y'
        self.auto_upgrade = input(f"{yellow}Pakai Auto Upgrade? (y/n): ").lower() == 'y'

    def headers(self, token):
        return {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {token}",
            "Origin": "https://dapp.pokequest.io",
            "Referer": "https://dapp.pokequest.io/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        }

    def get_token(self, data):
        url = f"https://api.pokey.quest/auth/login"

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://dapp.pokequest.io",
            "Referer": "https://dapp.pokequest.io/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36",
        }

        data = self.parse_query_id(data=data)

        data = json.dumps(data)

        headers["Content-Length"] = str(len(data))

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def user_info(self, token):
        url = f"https://api.pokey.quest/tap/sync"

        headers = self.headers(token=token)

        response = requests.post(url=url, headers=headers)

        return response

    def get_task(self, token):
        url = f"https://api.pokey.quest/mission/list"

        headers = self.headers(token=token)

        response = requests.get(url=url, headers=headers)

        return response

    def do_task(self, token, mission_id):
        url = f"https://api.pokey.quest/mission/claim"

        headers = self.headers(token=token)

        data = {"mission_id": mission_id}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def get_friend(self, token):
        url = f"https://api.pokey.quest/referral/list"

        headers = self.headers(token=token)

        response = requests.get(url=url, headers=headers)

        return response

    def claim_friend(self, token, friend_id):
        url = f"https://api.pokey.quest/referral/claim-friend"

        headers = self.headers(token=token)

        data = {"friend_id": friend_id}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def farm(self, token):
        url = f"https://api.pokey.quest/pokedex/farm"

        headers = self.headers(token=token)

        response = requests.post(url=url, headers=headers)

        return response

    def upgrade(self, token):
        url = f"https://api.pokey.quest/poke/upgrade"

        headers = self.headers(token=token)

        response = requests.post(url=url, headers=headers)

        return response

    def tap(self, token, tap_count):
        url = f"https://api.pokey.quest/tap/tap"

        headers = self.headers(token=token)

        data = {"count": tap_count}

        response = requests.post(url=url, headers=headers, data=data)

        return response

    def parse_query_id(self, data):
        parsed_query = urllib.parse.parse_qs(data)

        final_json = {}

        for key, values in parsed_query.items():
            if key == "user" and values:
                user_json_str = values[0]
                final_json[key] = json.loads(urllib.parse.unquote(user_json_str))
            else:
                final_json[key] = values[0] if values else None

        return final_json

    def main(self):
        while True:
            data = open(data_file, "r").read().splitlines()
            num_acc = len(data)
            for no, account_data in enumerate(data):
                print(f"{random.choice(rcolor)}|=========== [    Akun {no + 1}/{num_acc}     ] ===========|")

                try:
                    # Get token
                    get_token = self.get_token(data=account_data).json()
                    token = get_token["data"]["token"]

                    # Get user info
                    user_info = self.user_info(token=token).json()
                    level = user_info["data"]["level"]
                    available_taps = user_info["data"]["available_taps"]
                    print(f"{red}Level: {white}{level}")
                    print(f"{green}Tap yang tersisa: {red}{available_taps}")
                    print(f"{random.choice(rcolor)}|-------------------------------------------|")
                    balances = user_info["data"]["balance_coins"]
                    for balance in balances:
                        coin_type = balance["currency_symbol"]
                        coin_balance = balance["balance"]
                        print(f"{red}{coin_type} {green}Balance: {white}{coin_balance:,.0f}")

                    # Do task
                    if self.auto_do_task:
                        print(f"{random.choice(rcolor)}|-------------------------------------------|")
                        print(f"{yellow}Auto Lakukan Tugas: {green}ON")
                        print(f"{yellow}Sedang mencari tugas...")
                        get_task = self.get_task(token=token).json()
                        tasks = get_task["data"]
                        for task in tasks:
                            task_id = task["id"]
                            task_name = task["title"]
                            do_task = self.do_task(token=token, mission_id=task_id).json()
                            status = do_task["data"]["success"]
                            if status:
                                print(f"{white}{task_name}: {green}Berhasil")
                            else:
                                print(f"{white}{task_name}: {red}Gagal atau Sudah Selesai")
                    else:
                        print(f"{yellow}Auto Lakukan Tugas: {red}OFF")

                    # Claim friend
                    print(f"{yellow}Mencoba klaim dari teman...")
                    get_friend = self.get_friend(token=token).json()
                    friends = get_friend["data"]["data"]
                    for friend in friends:
                        friend_id = friend["id"]
                        claim_friend = self.claim_friend(token=token, friend_id=friend_id).json()
                        status = claim_friend["data"]["success"]
                        if status:
                            print(f"{white}Teman {friend_id}: {green}Berhasil")
                        else:
                            print(f"{white}Teman {friend_id}: {red}Sudah Diklaim")

                    # Reward from collection
                    print(f"{yellow}Sedang mencari hadiah dari koleksi...")
                    farm = self.farm(token=token).json()
                    try:
                        gold_reward = farm["data"]["gold_reward"]
                        print(f"{green}Hadiah Gold: {white}{gold_reward:,.0f}")
                    except:
                        print(f"{white}Ambil hadiah dari koleksi: {red}Belum saatnya")

                    # Upgrade
                    if self.auto_upgrade:
                        print(f"{random.choice(rcolor)}|-------------------------------------------|")
                        print(f"{yellow}Auto Upgrade: {green}ON")
                        upgrade = self.upgrade(token=token).json()
                        status = upgrade["error_code"]
                        if status == "OK":
                            level = upgrade["data"]["level"]
                            max_taps = upgrade["data"]["max_taps"]
                            print(f"{green}Level baru: {white}{level} - {green}Max taps: {white}{max_taps}")
                        elif status == "INSUFFICIENT_BALANCE":
                            print(f"{white}Auto Upgrade: {red}Koin tidak cukup")
                        else:
                            print(f"{white}Auto Upgrade: {red}Gagal, coba lagi")
                    else:
                        print(f"{yellow}Auto Upgrade: {red}OFF")

                    
                    print(f"{yellow}|=========== [ Memulai Tapping ] ===========|")
                    while True:
                        tap = self.tap(token=token, tap_count=50).json()
                        level = tap["data"]["level"]
                        available_taps = tap["data"]["available_taps"]
                        print(f"{random.choice(rcolor)}Taps yang tersisa: {red}{available_taps}")
                        balances = tap["data"]["balance_coins"]
                        for balance in balances:
                            coin_type = balance["currency_symbol"]
                            coin_balance = balance["balance"]
                            

                        if available_taps == 0:
                            print(f"{random.choice(rcolor)}|-------------------------------------------|")
                            for balance in balances:  # Jika ingin mencetak semua saldo koin
                                coin_type = balance["currency_symbol"]
                                coin_balance = balance["balance"]
                                print(f"{red}{coin_type} {green}Balance: {white}{coin_balance:,.0f}")
                            break  # Keluar dari loop jika tidak ada taps yang tersisa
                except Exception as e:
                    print(f"{red}Terjadi kesalahan dalam mengambil token, coba lagi!")

            print(f"{random.choice(rcolor)}============== Semua Akun Sudah Diproses =================")
            for i in range(180, 0, -1):  # Menggunakan directory waktu refresh
                sys.stdout.write(f"\r{random.choice(rcolor)}Memproses lagi semua akun dalam {i} detik...")
                sys.stdout.flush()
                time.sleep(1)
            print("Mari kita ulang lagi!")


if __name__ == "__main__":
    try:
        pokey = PokeyQuest()
        pokey.main()
    except KeyboardInterrupt:
        sys.exit()