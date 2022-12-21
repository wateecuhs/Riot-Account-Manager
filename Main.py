import tkinter, customtkinter, win32gui, json, requests, time
from win32gui import FindWindow, GetWindowRect
from requests.auth import HTTPBasicAuth
from LCU import LcuInfo


customtkinter.set_appearance_mode("dark") 
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    global self

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

        self.button_addaccount = customtkinter.CTkButton(master = self, text="Manage Accounts",command=self.create_window,fg_color="#125748",hover_color="#1f7d69")
        self.button_addaccount.grid(row=0, column=1, padx=(10,20), pady=15)
        with open("accounts.json","r") as accfile:
            accounts = json.load(accfile)
        for x in range(len(accounts)):
            customtkinter.CTkButton(self, text=accounts[x].get('profile'), command=lambda number=x: login(number)
        ).grid(column=0, row=x, padx=(20,10), pady=15)
            


    def create_window(self):
        global window
        window = customtkinter.CTkToplevel(self)
        window.geometry("330x200")
        window.grid_columnconfigure((0, 1), weight=0)
        window.grid_rowconfigure((0, 1, 2, 3), weight=0)

        customtkinter.CTkButton(window,text="Add a profile", command=self.add_account_window).grid(column=0,row=0,columnspan=2,padx=(10),pady=(10),sticky="ns")
        customtkinter.CTkButton(window,text="Remove a profile", command=self.remove_account).grid(column=1,row=1,padx=(10),pady=(10),sticky="nsew")
        editprofile = customtkinter.CTkButton(window,text="Edit a profile", command=self.edit_account).grid(column=0,row=1,padx=(10),pady=(10),sticky="nsew")
        with open("accounts.json","r") as accfile:
            accounts = json.load(accfile)
        if len(accounts) == 0:
            editprofile.configure(state="disabled")


    def edit_account_window(self):
        global window3,entry_edit1,entry_edit2,entry_edit3
        window3 = customtkinter.CTkToplevel(window)
        window3.geometry("330x200")
        window3.grid_columnconfigure((0, 1), weight=1)
        window3.grid_rowconfigure((0, 1, 2, 3), weight=0)
        
        entry_edit1= customtkinter.CTkEntry(window3,placeholder_text="Type in the profile name you want to use")
        entry_edit1.grid(column=0,row=0,columnspan=2,padx=10,pady=10,sticky="nsew")
        entry_edit2= customtkinter.CTkEntry(window3,placeholder_text="Type in your account's username")
        entry_edit2.grid(column=0,row=1,columnspan=2,padx=10,pady=10,sticky="nsew")
        entry_edit3= customtkinter.CTkEntry(window3,placeholder_text="Type in your password",show="*")
        entry_edit3.grid(column=0,row=2,columnspan=2,padx=10,pady=10,sticky="nsew")
        customtkinter.CTkButton(window3,text="Add Account",command=updateacc).grid(column=0,row=3,columnspan=2,padx=10,pady=10,sticky="ns")        

        
    def remove_account(self):
        with open("accounts.json","r") as accfile:
            accounts = json.load(accfile)
        customtkinter.CTkOptionMenu(master=window,values=[account['profile'] for account in accounts],command=optionmenu_callback1).grid(column=1,row=2,padx=10,pady=10,sticky="nsew")
        customtkinter.CTkButton(master=window,text="Confirm",command=removeaccount).grid(column=1,row=3,padx=10,pady=10,sticky="nsew")
        
    def edit_account(self):
        with open("accounts.json","r") as accfile:
            accounts = json.load(accfile)
        customtkinter.CTkOptionMenu(master=window,values=[account['profile'] for account in accounts],command=optionmenu_callback2).grid(column=0,row=2,padx=10,pady=10,sticky="nsew")
        customtkinter.CTkButton(master=window,text="Confirm",command=self.edit_account_window).grid(column=0,row=3,padx=10,pady=10,sticky="nsew")

    def add_account_window(self):
        global window2,entry1,entry2,entry3
        window2 = customtkinter.CTkToplevel(window)
        window2.geometry("330x200")
        window2.grid_columnconfigure((0, 1), weight=1)
        window2.grid_rowconfigure((0, 1, 2, 3), weight=0)
        
        entry1= customtkinter.CTkEntry(window2,placeholder_text="Type in the profile name you want to use")
        entry1.grid(column=0,row=0,columnspan=2,padx=10,pady=10,sticky="nsew")
        entry2= customtkinter.CTkEntry(window2,placeholder_text="Type in your account's username")
        entry2.grid(column=0,row=1,columnspan=2,padx=10,pady=10,sticky="nsew")
        entry3= customtkinter.CTkEntry(window2,placeholder_text="Type in your password",show="*")
        entry3.grid(column=0,row=2,columnspan=2,padx=10,pady=10,sticky="nsew")
        customtkinter.CTkButton(window2,text="Add Account",command=add_account).grid(column=0,row=3,columnspan=2,padx=10,pady=10,sticky="ns")

    
def add_account():
    pfName = entry1.get()
    username = entry2.get()
    password = entry3.get()
    with open("accounts.json","r") as accfile:
        accounts = json.load(accfile)
    if accounts == "":
        accounts = []
    profile = {"profile": pfName,"username": username,"password": password}
    accounts.append(profile)
    with open("accounts.json","w") as accfile:
        json.dump(accounts,accfile)
    window2.withdraw()
    window.withdraw()
    refresh(app)

def refresh(self):
    self.quit()
    time.sleep(0.5)
    app = App()
    app.mainloop()

def optionmenu_callback2(choice):
    global account_to_edit
    account_to_edit = choice

def updateacc():
    pfName = entry_edit1.get()
    username = entry_edit2.get()
    password = entry_edit3.get()
    profile = {"profile": pfName,"username": username,"password": password}
    with open("accounts.json","r") as accfile:
        accounts = json.load(accfile)
    for account in accounts:
        if pfName == account['profile']:
            accounts.remove(account)
    accounts.append(profile)
    with open("accounts.json","w") as accfile:
            json.dump(accounts,accfile)
    window3.withdraw()
    window.withdraw()
    refresh(app)

def removeaccount():
    with open("accounts.json","r") as accfile:
        accounts = json.load(accfile)
    for account in accounts:
        if account['profile'] == account_to_remove:
            accounts.remove(account)
    with open("accounts.json","w") as accfile:
        json.dump(accounts,accfile)
    window.withdraw()
    refresh(app)


def optionmenu_callback1(choice):
    global account_to_remove
    account_to_remove = choice


def login(index):
    global app
    lcu_info = LcuInfo()

    lcu_port = lcu_info.access_port
    lcu_endpoint = f'https://127.0.0.1:{lcu_port}/rso-auth/v1/session/credentials'
    lcu_password = lcu_info.remoting_auth_token
    lcu_user = 'riot'

    with open("accounts.json","r") as accfile:
        accounts = json.load(accfile)

    payload = {
        'username': accounts[index].get('username'),
        'password': accounts[index].get('password'),
        'persistLogin': False
    }

    response = requests.put(lcu_endpoint, json=payload, verify=False, auth=(lcu_user, lcu_password))

    if response.status_code == 201:
        response_content = response.json()
        if response_content.get('error')=="":
            isloginavailable = "no"
            app.withdraw()
            wait_for_client()
            time.sleep(2)
            app = App()
            app.mainloop()
        else:
            print(f"error : {response_content.get('error')}")
    else:
        print(f"error {response.status_code}")


def wait_for_client():
    isloginavailable = "no"
    while FindWindow(None, "Riot Client Main")==0 or isloginavailable == "no":
        print('loop')
        time.sleep(2)
        
        if FindWindow(None,"Riot Client Main")!=0:
            lcu_info = LcuInfo()

            lcu_port = lcu_info.access_port
            lcu_endpoint = f'https://127.0.0.1:{lcu_port}/rso-auth/v1/session/credentials'
            lcu_password = lcu_info.remoting_auth_token
            lcu_user = 'riot'

            payload = {
                'username': "isloginavailable",
                'password': "isloginavailable",
                'persistLogin': False
            }

            response = requests.put(lcu_endpoint, json=payload, verify=False, auth=(lcu_user, lcu_password))
            
            if response.status_code == 201:
                response_content = response.json()
                if response_content.get('error')=="auth_failure":
                    isloginavailable = "yes"
                else:
                    print(f"error : {response_content.get('error')}")
                    isloginavailable = "no"
            else:
                print(f"error {response.status_code}")
                isloginavailable = "no"

        

if __name__ == "__main__":
    wait_for_client()
    time.sleep(1)
    app = App()
    app.mainloop()
