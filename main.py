###############################
# Made by github.com/No0ne-15 #
#     > Public  Project <     #
#   For no0ne-community.com   #
###############################

import threading
import os
import random

try:
    import httpx
    import customtkinter as ctk
    import win32gui
    import win32.lib.win32con as win32con
    import webbrowser
    
except ModuleNotFoundError:
    os.system("pip install httpx")
    os.system("pip install customtkinter")
    os.system("pip install win32gui")
    os.system("pip install pypiwin32")
    os.system("pip install webbrowser")

red = "#e83535"
light_red = "#f56e6e"

with open("data/tokens.txt", "r+") as f:
    token_list = f.read().splitlines()

with open("data/proxies.txt", "r+") as f:
    proxies_list = f.read().splitlines()

win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_HIDE)

#---------------------------------------------------------------------------------------#

class Main:
    def __init__(self):
        self.main = ctk.CTk()
        self.main.geometry("1000x600")
        self.main.minsize(1000, 600)
        self.main.maxsize(1000, 600)
        self.main.title(f"GUI Discord Token Checker   -   By github.com/No0ne")
        self.info_frame = ctk.CTkFrame(master=self.main, border_color="black", width=980, height=100)
        self.info_frame.grid(row=0, column=0, padx=10, pady=(10, 5))
        self.button = ctk.CTkButton(master=self.info_frame, text="Open GitHub", fg_color=red, hover_color=light_red, font=("Roboto", 20, "bold"), width=313, command=self.open_github)
        self.button.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="we")
        self.button = ctk.CTkButton(master=self.info_frame, text="Join Discord", fg_color=red, hover_color=light_red, font=("Roboto", 20, "bold"), width=314, command=self.open_discord)
        self.button.grid(row=0, column=1, padx=5, pady=10, sticky="we")
        self.button = ctk.CTkButton(master=self.info_frame, text="Open Website", fg_color=red, hover_color=light_red, font=("Roboto", 20, "bold"), width=313, command=self.open_website)
        self.button.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="we")
        self.checker_frame = ctk.CTkFrame(master=self.main, width=980, height=460)
        self.checker_frame.grid(row=1, column=0, padx=10, pady=5)
        self.loaded = ctk.CTkFrame(master=self.checker_frame, width=980, height=200)
        self.loaded.grid(row=0, column=0, padx=10, pady=10)
        self.text = ctk.CTkLabel(master=self.loaded, text=f"Tokens: {len(token_list)}", fg_color="transparent", font=("Roboto", 20, "bold"))
        self.text.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self.text = ctk.CTkLabel(master=self.loaded, text=f"Proxies: {len(proxies_list)}", fg_color="transparent", font=("Roboto", 20, "bold"))
        self.text.grid(row=0, column=1, padx=10, pady=10, sticky="we")
        self.switch_proxy = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(master=self.checker_frame, text="Use Proxy", progress_color=red, font=("Roboto", 20, "bold"), variable=self.switch_proxy, onvalue="on", offvalue="off")
        self.switch.grid(row=1, column=0, padx=(415, 10), pady=10, sticky="nswe")
        self.button_check = ctk.CTkButton(master=self.checker_frame, text="Check", fg_color=red, hover_color=light_red, font=("Roboto", 20, "bold"), width=450, command=self.checker)
        self.button_check.grid(row=2, column=0, padx=10, pady=5, sticky="we")
        self.progressbar = ctk.CTkProgressBar(master=self.checker_frame, orientation="horizontal", progress_color=red, mode="indeterminate", width=960)
        self.progressbar.grid(row=3, column=0, padx=10, pady=(15, 10), sticky="nswe")
        self.progressbar.set(0)
        self.checker_textbox = ctk.CTkTextbox(master=self.main, font=("Roboto", 18), width=980, height=325)
        self.checker_textbox.grid(row=2, column=0, padx=10, pady=(5, 10), sticky="we")
        self.checker_textbox.configure(state="disabled")
        self.main.mainloop()
    
    def checker(self):
        self.choice = self.switch_proxy.get()
        if self.choice == "off":
            threading.Thread(target=self.checker_proxyless).start()
        elif self.choice == "on":
            threading.Thread(target=self.proxy_checking).start()

    def checker_proxyless(self):
        self.button_check.configure(state="disabled")
        self.checker_textbox.configure(state="normal")
        self.checker_textbox.insert("0.0", f"\n\n\n")
        self.progressbar.set(0)
        self.progressbar.start()
        open('result/valid.txt', 'w').close()
        open('result/invalid.txt', 'w').close()
        open('result/locked.txt', 'w').close()
        valid = 0
        invalid = 0
        locked = 0
        for token in token_list:
            r = httpx.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
            if r.status_code == 200:
                console_token = token.split('.')
                self.checker_textbox.insert("0.0", f"VALID       -     {console_token[0]}.{console_token[1]}.********************************************\n")
                with open("result/valid.txt","a") as f:
                    f.write(f"{token}\n")
                valid += 1
            elif r.status_code == 401:
                self.checker_textbox.insert("0.0", f"INVALID   -     {token}\n")
                with open("result/invalid.txt","a") as f:
                    f.write(f"{token}\n")
                invalid += 1
            elif r.status_code == 403:
                self.checker_textbox.insert("0.0", f"LOCKED   -     {token}\n")
                with open("result/locked.txt","a") as f:
                    f.write(f"{token}\n")
                locked += 1
        self.checker_textbox.insert("0.0", f"Successfully checked tokens.txt (Proxyless)      -      Result: [{valid} Valid] [{invalid} Invalid] [{locked} Phone Locked]      -      Saved in  /result\n\n")
        self.checker_textbox.configure(state="disabled")
        self.progressbar.stop()
        self.button_check.configure(state="normal")

    def proxy_checking(self):
        self.button_check.configure(state="disabled")
        self.checker_textbox.configure(state="normal")
        self.checker_textbox.insert("0.0", f"\n\n\n")
        self.progressbar.set(0)
        self.progressbar.start()
        open('result/valid.txt', 'w').close()
        open('result/invalid.txt', 'w').close()
        open('result/locked.txt', 'w').close()
        self.valid = 0
        self.invalid = 0
        self.locked = 0
        self.threads = 0
        self.count = 0
        while True:
            if self.threads <= 10:
                for token in token_list:  
                    random_proxy = "http://" + random.choice(proxies_list).strip()
                    threading.Thread(target=self.checker_proxied(token, random_proxy)).start()

            if self.count == len(token_list):
                break
        self.checker_textbox.insert("0.0", f"Successfully checked tokens.txt (Proxyless)      -      Result: [{self.valid} Valid] [{self.invalid} Invalid] [{self.locked} Phone Locked]      -      Saved in  /result\n\n")
        self.checker_textbox.configure(state="disabled")
        self.progressbar.stop()
        self.button_check.configure(state="normal")

    def checker_proxied(self, token, random_proxy):
        self.threads += 1
        try:
            r = httpx.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token}, proxy=random_proxy, timeout=5)
            if r.status_code == 200:
                console_token = token.split('.')
                self.checker_textbox.insert("0.0", f"VALID       -     {console_token[0]}.{console_token[1]}.********************************************\n")
                with open("result/valid.txt","a") as f:
                    f.write(f"{token}\n")
                self.valid += 1
            elif r.status_code == 401:
                self.checker_textbox.insert("0.0", f"INVALID   -     {token}\n")
                with open("result/invalid.txt","a") as f:
                    f.write(f"{token}\n")
                self.invalid += 1
            elif r.status_code == 403:
                self.checker_textbox.insert("0.0", f"LOCKED   -     {token}\n")
                with open("result/locked.txt","a") as f:
                    f.write(f"{token}\n")
                self.locked += 1
        except:
                self.checker_textbox.insert("0.0", f"ERROR      -     Invalid Proxy :  {random_proxy} (no response after 5s)\n")
                new_proxy = "http://" + random.choice(proxies_list).strip()
                self.checker_proxied(token, new_proxy)
        self.threads -= 1
        self.count += 1

    def open_github(self):
        webbrowser.open(f"https://github.com/No0ne-15")

    def open_discord(self):
        webbrowser.open(f"https://discord.no0ne-community.com")

    def open_website(self):
        webbrowser.open(f"https://no0ne-community.com")

if __name__ == "__main__":
    Main()
