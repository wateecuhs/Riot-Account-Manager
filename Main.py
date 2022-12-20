import tkinter, customtkinter, win32gui, json, requests
from win32gui import FindWindow, GetWindowRect
from requests.auth import HTTPBasicAuth
from LCU import LcuInfo

x=0
with open("accounts.json","r") as accfile:
    accounts = json.load(accfile)



customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    custom_options = ("my_custom_var",)

    def __init__(self):
        super().__init__()
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.overrideredirect(False)
        self.title("Riot Login Selector")
        #self.resizable(False,False)

        window_handle = FindWindow(None, "Riot Client Main")
        window_rect   = GetWindowRect(window_handle)
        window_rect_1 = (window_rect[2]-window_rect[0])*0.27
        window_rect_2 = (window_rect[3]-window_rect[1])*0.05
        self.geometry(f"340x400+{int(window_rect[0]+window_rect_1)}+{window_rect_2+window_rect[1]}")

        self.button_addaccount = customtkinter.CTkButton(master = self, text="Add account",command=self.add_account,fg_color="#125748",hover_color="#1f7d69")
        self.button_addaccount.grid(row=0, column=1, padx=(10,20), pady=15)

        for x in range(len(accounts)):
            customtkinter.CTkButton(self, text=accounts[x].get('profile'), command=lambda number=x: login(number)
        ).grid(column=0, row=x, padx=(20,10), pady=15)
            
        
    def add_account(self):
        self.dialog_1 = customtkinter.CTkInputDialog(text="Type in the profile name you want to use:", title="Profile Name")
        profile_name = self.dialog_1.get_input()
        self.dialog_2 = customtkinter.CTkInputDialog(text="Type in your account's username:", title="Username")
        username = self.dialog_2.get_input()
        self.dialog_3 = customtkinter.CTkInputDialog(text="Type in your password:", title="Password")
        password = self.dialog_3.get_input()
        if profile_name == "" or username == "" or password ==  "" or profile_name == "Null" or username == "Null" or password == "Null":
            print("Adding account failed, please enter correct values")
        else:
            if accounts == "":
                accounts = []
            profile = {"profile": profile_name,"username": username,"password": password}
            accounts.append(profile)
            with open("accounts.json","w") as accfile:
                json.dump(accounts,accfile)


        


def login(index):

    lcu_info = LcuInfo()

    lcu_port = lcu_info.access_port
    lcu_endpoint = f'https://127.0.0.1:{lcu_port}/rso-auth/v1/session/credentials'
    lcu_password = lcu_info.remoting_auth_token
    lcu_user = 'riot'



    payload = {
        'username': accounts[index].get('username'),
        'password': accounts[index].get('password'),
        'persistLogin': False
    }

    response = requests.put(lcu_endpoint, json=payload, verify=False, auth=(lcu_user, lcu_password))

    response = response.json()
    if response.get('error')!="":
        return (response.get('error'))
    else:
        quit()

if __name__ == "__main__":
    app = App()
    app.mainloop()