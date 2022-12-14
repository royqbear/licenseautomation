from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import *
import tkinter.font as font
from tkinter import ttk
from tkinter import messagebox
from time import sleep
from time import sleep
import os
import webbrowser


class Window:
    def __init__(self):
        self.window = Tk()
        self.window.eval('tk::PlaceWindow . center')
        self.background = '#edfbff'
        self.window.config(background=self.background)
        self.welcome_label = Label(self.window).place(relx=0.5, rely=0.5, anchor='center')
        self.frame = Frame(self.window, background=self.background)
        self.frame2 = Frame(self.window, background=self.background)
        self.window.geometry("500x500")
        self.window.title("License MarketPlace")
        #user\pass for website:
        self.username = "******"
        self.password = "******"

        # creating webdriver for chrome
        try:
             self.options = webdriver.ChromeOptions()
            self.options.add_argument('--headless')
            self.chrome_service = ChromeService('chromedriver')
            self.chrome_service.creationflags = CREATE_NO_WINDOW
            self.driver = webdriver.Chrome(options=self.options,service=self.chrome_service)
            self.session_id = self.driver.session_id
        except Exception:
            messagebox.showerror("Version update required",
                                 'Please update Chronium\nfile needs to be placed where the EXE file is located.')
            webbrowser.open('https://chromedriver.chromium.org/downloads')  # Go to example.com
            self.window.destroy()
        #defininf all gui variables
        self.companies = self.scrap()  # getting list of companies from scrap class
        self.company_list = Listbox(self.frame, exportselection=False, height=len(self.companies))
        self.choices = ['Buy', 'Cancel']
        # button creation = lambda calling multiple functions
        self.btn = Button(self.frame2, text='Submit', command=self.button_methods)
        self.buy_cancel = ttk.Combobox(self.frame2, values=self.choices,width=20)
        self.buy_cancel.current(0)
        self.user_input = Entry(self.frame2,width=30)
        self.userIn_label = Label(self.frame2, text="Enter name for the license",background=self.background)
        self.buy_cancel_label = Label(self.frame2, text="Do you want to Buy or Cancel?",background=self.background)
        self.mainlabel = Label(self.frame, text="Choose company please",background=self.background)
        self.numeric = Spinbox(self.frame2, from_=1, to_=100, width=10)

        self.userIn_label.grid(row=3, column=0, pady=5)
        self.user_input.grid(row=4, column=0, pady=5)


    #getting the list of licenses from the website, based on user name entered
    def scrap(self):

        try:
            self.driver.get("https://shop.cms1.co.il/my-subscriptions/?viewId=718")
        except Exception:
            print("cannot load website, refreshing")
        else:
            self.driver.get("https://shop.cms1.co.il/login/")

        login_user = self.driver.find_element(By.NAME, "fld-login-username")
        login_user.send_keys(self.username)
        login_pass = self.driver.find_element(By.NAME, "fld-login-password")
        login_pass.send_keys(self.password)
        self.driver.find_element(By.NAME, "fld-login-submit").click()
        active_subs = self.driver.find_element(By.CLASS_NAME, "greenbtn")
        active_subs.click()
        table = self.driver.find_elements(By.XPATH, "//a[@class='align-middle']")
        lis = []
        for i in table:
            lis.append(i.text)
        return lis

    def return_to_license_page(self):
        self.driver.get("https://shop.cms1.co.il/my-subscriptions/?viewId=718")

#automation code for buying license
    def buy_lic(self):
        self.return_to_license_page()
        company_name_from_app = self.list_pick()
        name_for_new_lic = self.get_user_input()
        amount_to_buy = self.get_spinbox()

        try:
            el = self.driver.find_element(By.XPATH,
                                     f"//*[@id='iw-subscription-context']/table/tbody/tr[{company_name_from_app}]/td[12]/div/button")
            el.click()
        except Exception:
            print("trying other method")
        try:
            el = self.driver.find_element(By.XPATH,
                                     f"//*[@id='iw-subscription-context']/table/tbody/tr[{company_name_from_app}]/td[11]/div/button")
            el.click()
        except Exception:
            print("input is not in scope")
            # messagebox.showerror("Error", "Coding needed - input given to scrap is not in scope")
        sleep(3)
        try:
            buy = self.driver.find_element(By.XPATH, f'//*[@id="iw-subscription-context"]/table/tbody/tr[{company_name_from_app}]/td[12]/div/div/button[1]')
            buy.click()
        except Exception:
            print('tryin again')

        try:
            buy = self.driver.find_element(By.XPATH, f'//*[@id="iw-subscription-context"]/table/tbody/tr[{company_name_from_app}]/td[11]/div/div/button[1]')
            buy.click()
        except Exception:
            print("cannot find")
            messagebox.showerror("Error","I dont know what to do with myself...")
        popup = self.driver.find_element(By.CLASS_NAME, "modal-content")
        sleep(3)
        amount = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/div/div/div/div/div[2]/div/input')
        print(amount.text)
        amount.send_keys(Keys.CONTROL + "a")
        amount.send_keys(Keys.DELETE)
        amount.send_keys(amount_to_buy)
        submit_buy = self.driver.find_element(By.XPATH, '//*[@id="buylicense-modal___BV_modal_footer_"]/div/button[2]')
        submit_buy.click()
        sleep(3)
        input_user_name_fromapp = self.driver.find_element(By.XPATH,
                                                      '/html/body/form/main/div[2]/div/div/section/div[3]/div/div/div[2]/div/div[3]/div[3]/fieldset/div[3]/div/div/input')
        input_user_name_fromapp.send_keys(name_for_new_lic)
        approve_buy = self.driver.find_element(By.XPATH,
                                          '//*[@id="checkout-step-1"]/div[3]/div/div/div[2]/div/div[4]/div[2]/button')
        approve_buy.click()
        final_click = self.driver.find_element(By.XPATH,
                                          '//*[@id="checkout-step-2"]/div[3]/div/div/div[2]/div/div[2]/div/div/div/button[2]')
        final_click.click()
        messagebox.showinfo("Success","Operation completed")
        sleep(2)

#automation code for cancelling a license
    def cancel_license_scrap(self):
        self.return_to_license_page()
        company_name_from_app = self.list_pick()
        name_for_new_lic =  self.get_user_input()
        cancel_amount = self.get_spinbox()
        try:
            company_row = self.driver.find_element(By.XPATH,
                                              f"//*[@id='iw-subscription-context']/table/tbody/tr[{company_name_from_app}]/td[12]/div/button")
            company_row.click()
        except Exception:
            print("trying other method")
        try:
            company_row = self.driver.find_element(By.XPATH,
                                              f"//*[@id='iw-subscription-context']/table/tbody/tr[{company_name_from_app}]/td[11]/div/button")
            company_row.click()
        except Exception:
            print("input is not in scope")
            # messagebox.showerror("Error", "Coding needed - input given to scrap is not in scope")

        try:
            cancel = self.driver.find_element(By.XPATH,
                                         f'//*[@id="iw-subscription-context"]/table/tbody/tr[{company_name_from_app}]/td[11]/div/div/button[3]')
            cancel.click()
        except Exception:
            pass
        try:
            cancel = self.driver.find_element(By.XPATH,
                                         f'//*[@id="iw-subscription-context"]/table/tbody/tr[{company_name_from_app}]/td[12]/div/div/button[3]')
            cancel.click()
        except Exception:
            print('code error')
        sleep(3)
        amount_to_cancel = self.driver.find_element(By.XPATH, '//*[@id="__BVID__29"]')
        amount_to_cancel.send_keys(Keys.CONTROL + "a")
        amount_to_cancel.send_keys(Keys.DELETE)
        amount_to_cancel.send_keys(cancel_amount)
        cancel_button = self.driver.find_element(By.XPATH,
                                            '//*[@id="cancel-subscription-modal___BV_modal_footer_"]/div/div/button[2]')
        cancel_button.click()
        messagebox.showinfo("Success", "Operation Completed")
        sleep(2)

#creating the app
    def app(self):
        # creating a frame for the lists
        self.frame.grid(row=0, column=0)
        self.frame2.grid(row=0, column=1)
        # frame1
        self.mainlabel.grid(row=0, column=0, padx=50, pady=10)
        self.company_list.grid(row=1, column=0, pady=10)

        # Frame2
        self.buy_cancel_label.grid(row=1, column=0, pady=10)
        self.buy_cancel.grid(row=2, column=0, pady=10)
        self.numeric.grid(row=5, column=0, pady=10)
        # adding items to the list (visually)
        for company in range(len(self.companies)):
            self.company_list.insert(END, self.companies[company])
        self.btn.grid(row=6, column=0)
        self.buy_cancel.bind("<<ComboboxSelected>>", self.user_input_if)
        self.window.mainloop()

    # deal with user input if to show or not based on the dropbox input
    def user_input_if(self, e):
        user_inp = self.buy_cancel.get()
        if user_inp == "Cancel":
            self.hide_input()
        elif user_inp == "Buy":
            self.userIn_label.grid(row=3, column=0, pady=10)
            self.user_input.grid(row=4, column=0, pady=10)
        else:
            messagebox.showwarning("OH OH !", "You need to choose option(Buy or Cancel)")
# approve action complete
    def button_popup(self):
        messagebox.showinfo("Done!", "Operation successful")

#hide input if cancel is chosen
    def hide_input(self):
        self.user_input.grid_remove()
        self.userIn_label.grid_remove()
    # picking company from the list for buying
    def list_pick(self):
        company_name = self.company_list.get(ANCHOR)
        if company_name not in self.companies:
            messagebox.showerror("Selection Error", "Please select company")
            return False
        else:
            print(company_name)
            return self.companies.index(company_name)+1

#code for the choice of the user, if buy then do this, if cancel then do this.
    def pick_buy_cancel(self):
        if self.buy_cancel.get() == "Buy":
            self.buy_lic()
            

        elif self.buy_cancel.get() == "Cancel":
            self.cancel_license_scrap()

#user input for new license
    def get_user_input(self):
        license_username = self.user_input.get()
        print(license_username)
        return license_username

#getting the amount of licenses frm user
    def get_spinbox(self):
        number_of_lics = self.numeric.get()
        if number_of_lics == 0:
            messagebox.showerror("Amount Error", "Please choose amount")
        print(number_of_lics)
        return number_of_lics

#like self.driver code for the submit button.
    def button_methods(self):
        if not self.list_pick():
            pass
        else:
            self.get_user_input()
            self.get_spinbox()
            self.pick_buy_cancel()



#login window and validation
class Login:
    def __init__(self,useros,userpassos):
        self.useros = useros
        self.userpassos = userpassos
        self.tkWindow = Tk()
    def load(self):

        self.tkWindow.geometry('200x150')
        self.tkWindow.title('Login')
        self.tkWindow.eval('tk::PlaceWindow . center')
        background = '#edfbff'
        self.tkWindow.configure(background=background)
        myfont = font.Font(family="segoe print", size=10)
        # username label and text entry box
        usernameLabel = Label(self.tkWindow, text="User Name", background=background, font=myfont).grid(row=0, column=0)
        username = StringVar()
        usernameEntry = Entry(self.tkWindow, textvariable=username, ).grid(row=0, column=1)

        # password label and password entry box
        passwordLabel = Label(self.tkWindow, text="Password", background=background, font=myfont).grid(row=1, column=0)
        password = StringVar()
        passwordEntry = Entry(self.tkWindow, textvariable=password, show='*').grid(row=1, column=1)
        loginButton = Button(self.tkWindow, background=background, font=myfont, text="Login", command=lambda:[self.validateLogin(username,password)]).grid(row=4, column=0, pady=20)
        self.tkWindow.mainloop()

    def close_login_window(self):
        self.tkWindow.destroy()

    def validateLogin(self,username,password):
        user_from_input = username.get()
        pass_from_input = password.get()
        if user_from_input == useros and pass_from_input == userpassos:
            messagebox.showinfo("Login Success", "Welcome\nApp is loading, wait a moment.\n:) :) :)")
            print("good")
            self.close_login_window()
            app = Window()
            app.app()
        else:
            messagebox.showerror("Login Error", "Please enter correct login info")
            print("error")
            self.load()

if __name__ == "__main__":
    useros = os.environ.get('youruserid')
    userpassos = os.environ.get("yourpass")
    login = Login(useros,userpassos)
    login.load()



