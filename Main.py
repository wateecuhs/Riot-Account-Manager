import tkinter
from tkinter import messagebox
import customtkinter

from LCU import LcuInfo
from iconStray import *

customtkinter.deactivate_automatic_dpi_awareness()
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
path = os.path.join(os.getenv('APPDATA')[:-8], 'Local', 'Riot Account Manager', 'accounts.json')
stay_logged_in = True


class App(customtkinter.CTk):
    def __init__(self):
        global button_dict, window_rect, window_rect_1, window_rect_2

        if os.path.exists(path):
            with open(path, "r") as account_file:
                accounts = json.load(account_file)
        else:
            with open(path, "w") as create_account_file:
                accounts = []
                json.dump(accounts, create_account_file)

        customtkinter.deactivate_automatic_dpi_awareness()
        super().__init__()
        self.grid_columnconfigure((0, 1), weight=0)
        if len(accounts) > 0:
            self.grid_rowconfigure((0, 1), weight=0)
        else:
            self.grid_rowconfigure((0, 1), weight=0)
        self.overrideredirect(False)
        self.title("Riot Login Selector")
        self.iconbitmap(ICON_PATH)

        window_handle = FindWindow(None, "Riot Client Main")
        window_rect = GetWindowRect(window_handle)
        window_rect_1 = (window_rect[2] - window_rect[0]) * 0.27
        window_rect_2 = (window_rect[3] - window_rect[1]) * 0.05
        added_size = 70 * (len(accounts) - 7) if 10 > len(accounts) > 7 else 0 if len(accounts) < 7 else 70 * 3
        added_size2 = 170 * int(len(accounts)/10)
        self.geometry(f"{340 + added_size2}x{400 + added_size}+{int(window_rect[0] + window_rect_1)}+{window_rect_2 + window_rect[1]}")

        self.button_add_account = customtkinter.CTkButton(master=self, text="Manage profiles",
                                                          command=self.create_window, fg_color="#125748",
                                                          hover_color="#1f7d69")
        self.button_add_account.grid(row=0, column=1 if len(accounts) < 10 else (int(len(accounts)/10)+1), padx=(10, 20), pady=15)

        self.checkbox = customtkinter.CTkCheckBox(master=self, text="Stay signed in", command=signed_in_checkbox,
                                                  checkbox_height=25, checkbox_width=25)
        self.checkbox.grid(row=1, column=1 if len(accounts) < 10 else (int(len(accounts)/10)+1), sticky="ns")
        self.checkbox.select()
        for x in range(len(accounts)):
            customtkinter.CTkButton(self, text=accounts[x].get('profile'), command=lambda number=x: login(number)
                                    ).grid(column=0 if x < 10 else int(x/10), row=int(repr(x)[-1]), padx=(20, 10), pady=15)

    def create_window(self):
        global window
        window = customtkinter.CTkToplevel(self)
        window.geometry("330x200")
        window.grid_columnconfigure((0, 1), weight=0)
        window.grid_rowconfigure((0, 1), weight=0)
        window.title("Manage profiles")
        customtkinter.CTkButton(window, text="Add a profile", command=self.add_account_window
                                ).grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="ns")
        remove_profile = customtkinter.CTkButton(window, text="Remove a profile", command=self.remove_account
                                                 ).grid(column=1, row=1, padx=10, pady=10, sticky="nsew")
        edit_profile = customtkinter.CTkButton(window, text="Edit a profile", command=self.edit_account
                                               ).grid(column=0, row=1, padx=10, pady=10, sticky="nsew")
        with open(path, "r") as account_file:
            accounts = json.load(account_file)
        if len(accounts) == 0:
            edit_profile.configure(state="disabled")
            remove_profile.configure(state="disabled")

    def edit_account_window(self):
        global window3, entry_edit1, entry_edit2, entry_edit3
        window3 = customtkinter.CTkToplevel(window)
        window3.geometry("330x200")
        window3.grid_columnconfigure((0, 1), weight=1)
        window3.grid_rowconfigure((0, 1, 2, 3), weight=0)
        window3.title("Edit a profile")

        entry_edit1 = customtkinter.CTkEntry(window3, placeholder_text="Type in the profile name you want to use")
        entry_edit1.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        entry_edit2 = customtkinter.CTkEntry(window3, placeholder_text="Type in your account's username")
        entry_edit2.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        entry_edit3 = customtkinter.CTkEntry(window3, placeholder_text="Type in your password", show="*")
        entry_edit3.grid(column=0, row=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkButton(window3, text="Add Account", command=edit_update
                                ).grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky="ns")

    def remove_account(self):
        global account_to_remove
        with open(path, "r") as account_file:
            accounts = json.load(account_file)
        account_to_remove = accounts[0]['profile']
        customtkinter.CTkOptionMenu(master=window, values=[account['profile'] for account in accounts],
                                    command=option_menu_callback1).grid(column=1, row=2, padx=10, pady=10,
                                                                        sticky="nsew")
        customtkinter.CTkButton(master=window, text="Confirm", command=remove_account
                                ).grid(column=1, row=3, padx=10, pady=10, sticky="nsew")

    def create_error_window(self, error):
        error_window = customtkinter.CTkToplevel(self)
        error_window.geometry(
            f"250x100+{int(window_rect[0] + window_rect_1) + 100}+{window_rect_2 + window_rect[1] + 100}")
        if error == "auth_failure":
            error = "Incorrect login credentials."
        error_label = customtkinter.CTkLabel(error_window, title='Error', text=f"Error: \n {error}")
        error_label.pack(side="top", expand=True, padx=10, pady=10)

        ok_button = customtkinter.CTkButton(error_window, text="OK", command=error_window.destroy)
        ok_button.pack(side="top", expand=True, padx=10, pady=10)

    def edit_account(self):
        global account_to_edit
        with open(path, "r") as account_file:
            accounts = json.load(account_file)
        account_to_edit = accounts[0]['profile']
        customtkinter.CTkOptionMenu(master=window, values=[account['profile'] for account in accounts],
                                    command=option_menu_callback2).grid(column=0, row=2, padx=10, pady=10,
                                                                        sticky="nsew")
        customtkinter.CTkButton(master=window, text="Confirm", command=self.edit_account_window
                                ).grid(column=0, row=3, padx=10, pady=10, sticky="nsew")

    def add_account_window(self):
        global window2, entry1, entry2, entry3
        window2 = customtkinter.CTkToplevel(window)
        window2.geometry("330x200")
        window2.grid_columnconfigure((0, 1), weight=1)
        window2.grid_rowconfigure((0, 1, 2, 3), weight=0)
        window2.title("Add a profile")

        entry1 = customtkinter.CTkEntry(window2, placeholder_text="Type in the profile name you want to use")
        entry1.grid(column=0, row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        entry2 = customtkinter.CTkEntry(window2, placeholder_text="Type in your account's username")
        entry2.grid(column=0, row=1, columnspan=2, padx=10, pady=10, sticky="nsew")
        entry3 = customtkinter.CTkEntry(window2, placeholder_text="Type in your password", show="*")
        entry3.grid(column=0, row=2, columnspan=2, padx=10, pady=10, sticky="nsew")
        customtkinter.CTkButton(window2, text="Add Account", command=add_account
                                ).grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky="ns")


def add_account():
    profile_name = entry1.get()
    username = entry2.get()
    password = entry3.get()
    with open(path, "r") as account_file:
        accounts = json.load(account_file)
    if accounts == "":
        accounts = []
    profile = {"profile": profile_name, "username": username, "password": password}
    accounts.append(profile)
    with open(path, "w") as account_file:
        json.dump(accounts, account_file)
    window2.withdraw()
    window.withdraw()
    refresh()


def refresh():
    global app
    app.withdraw()
    app.quit()
    time.sleep(1)
    app = App()
    app.protocol('WM_DELETE+_WINDOW', hide_window)
    app.mainloop()


def signed_in_checkbox():
    global stay_logged_in
    if app.checkbox.get() == 1:
        stay_logged_in = True
    elif app.checkbox.get() == 0:
        stay_logged_in = False


def edit_update():
    profile_name = entry_edit1.get()
    username = entry_edit2.get()
    password = entry_edit3.get()
    profile = {"profile": profile_name, "username": username, "password": password}
    with open(path, "r") as account_file:
        accounts = json.load(account_file)
    for account in accounts:
        if account_to_edit == account['profile']:
            accounts.remove(account)
    accounts.append(profile)
    with open(path, "w") as account_file:
        json.dump(accounts, account_file)
    window3.withdraw()
    window.withdraw()
    refresh()


def remove_account():
    with open(path, "r") as account_file:
        accounts = json.load(account_file)
    for account in accounts:
        if account['profile'] == account_to_remove:
            accounts.remove(account)
    with open(path, "w") as account_file:
        json.dump(accounts, account_file)
    window.withdraw()
    refresh()


def option_menu_callback1(choice):
    global account_to_remove
    print("optionmenu dropdown clicked:", choice)
    account_to_remove = choice
    print(account_to_remove)


def option_menu_callback2(choice):
    global account_to_edit
    print("optionmenu dropdown clicked:", choice)
    account_to_edit = choice
    print(account_to_edit)


def login(index):
    global app
    lcu_info = LcuInfo()

    lcu_port = lcu_info.access_port
    lcu_endpoint = f'https://127.0.0.1:{lcu_port}/rso-auth/v1/session/credentials'
    lcu_password = lcu_info.remoting_auth_token
    lcu_user = 'riot'

    with open(path, "r") as account_file:
        accounts = json.load(account_file)

    payload = {
        'username': accounts[index].get('username'),
        'password': accounts[index].get('password'),
        'persistLogin': stay_logged_in
    }

    response = requests.put(lcu_endpoint, json=payload, verify=False, auth=(lcu_user, lcu_password))

    if response.status_code == 201:
        response_content = response.json()
        if response_content.get('error') == "":
            app.withdraw()
            app.quit()
            time.sleep(3)
            wait_for_client()
            print(2)
            app = App()
            app.protocol('WM_DELETE+_WINDOW', hide_window)
            app.after(2000, app.mainloop())
        else:
            app.create_error_window(response_content.get('error'))
            print(f"error : {response_content.get('error')}")
    else:
        print(f"error {response.status_code}")


def wait_for_client():
    isloginavailable = "no"
    while FindWindow(None, "Riot Client Main") == 0 or isloginavailable == "no":
        print('loop')
        if FindWindow(None, "Riot Client Main") != 0:
            print(FindWindow(None, "Riot Client Main"))
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
                if response_content.get('error') == "auth_failure":
                    isloginavailable = "yes"
                else:
                    print(f"error : {response_content.get('error')}")
                    isloginavailable = "no"
            else:
                print(f"error {response.status_code}")
                isloginavailable = "no"
        time.sleep(2)


def hide_window():
    global app
    app.withdraw()


def main():
    global app
    init_icon()
    run_icon()
    wait_for_client()
    app = App()
    app.protocol('WM_DELETE+_WINDOW', hide_window)
    app.mainloop()


if __name__ == '__main__':
    main()
