from tkinter import messagebox, ttk, StringVar, Button, Tk, X, BOTH

from datanxt.application_window_template import ApplicationWindowTemplate
from datanxt.home import Home
from datanxt.install import Install
from datanxt.session_details import SessionDetails
from datanxt.services import test_connection, check_application_installation_Status
from datanxt.application_constants import ApplicationConstants


class DataNxtLogin(ApplicationWindowTemplate):
    def __init__(self, master):
        # Build Frame from Parent
        super().__init__(master)
        # Build Header Frame Label with Message
        self.show_header_message(self.app_constants.APPLICATION_HEADER_FRAME_LABEL)

        self.content = ttk.Frame(self.master, style='Content.TFrame')

        # Build Content Frame
        self.loginwelcome = ttk.Label(self.content, text="Connect to Staging Datasource (Microsoft SQL Server)",
                                      style='Content.TLabel')
        self.loginwelcome.place(x=150, y=30)

        self.servernamelbl = ttk.Label(self.content, text="Server name", style='Content.TLabel',
                                       width=self.app_constants.APPLICATION_LABEL_WIDTH)
        self.servernamelbl.place(x=150, y=90)

        self.servernametxt = ttk.Entry(self.content, width=30)
        self.servernametxt.focus_set()
        self.servernametxt.place(x=300, y=90)

        self.authenticationlbl = ttk.Label(self.content, text="Authentication", style='Content.TLabel',
                                           width=self.app_constants.APPLICATION_LABEL_WIDTH)
        self.authenticationlbl.place(x=150, y=120)

        self.authenticationopt = StringVar(self.master)
        self.authenticationopt.set(self.app_constants.APPLICATION_AUTHENTICATION_SQL)

        self.authenticationsqlopt = ttk.Radiobutton(self.content, text=self.app_constants.APPLICATION_AUTHENTICATION_SQL,
                                                    variable=self.authenticationopt,
                                                    value=self.app_constants.APPLICATION_AUTHENTICATION_SQL,
                                                    style='Content.TRadiobutton',
                                                    command=self.func_change_authentication)
        self.authenticationsqlopt.place(x=300, y=120)

        self.authenticationwinopt = ttk.Radiobutton(self.content,
                                                    text=self.app_constants.APPLICATION_AUTHENTICATION_WINDOWS,
                                                    variable=self.authenticationopt,
                                                    value=self.app_constants.APPLICATION_AUTHENTICATION_WINDOWS,
                                                    style='Content.TRadiobutton',
                                                    command=self.func_change_authentication)
        self.authenticationwinopt.place(x=300, y=140)

        self.useridlbl = ttk.Label(self.content, text="User id", style='Content.TLabel',
                                   width=self.app_constants.APPLICATION_LABEL_WIDTH)
        self.useridlbl.place(x=150, y=170)

        self.useridtxt = ttk.Entry(self.content, width=30)
        self.useridtxt.place(x=300, y=170)

        self.passwordlbl = ttk.Label(self.content, text="Password", style='Content.TLabel',
                                     width=self.app_constants.APPLICATION_LABEL_WIDTH)
        self.passwordlbl.place(x=150, y=200)

        self.passwordtxt = ttk.Entry(self.content, show="*",
                                     width=self.app_constants.APPLICATION_LABEL_ENTRY_BUTTON_WIDTH)
        self.passwordtxt.place(x=300, y=200)

        self.connectbtn = Button(self.content, text="Connect", width=self.app_constants.APPLICATION_BUTTON_WIDTH,
                                 command=self.func_connect)
        self.connectbtn.place(x=300, y=230)

        self.header.pack(fill=X)
        self.content.pack(fill=BOTH, expand=True)

    def func_change_authentication(self):
        if self.authenticationopt.get() == self.app_constants.APPLICATION_AUTHENTICATION_WINDOWS:
            self.useridtxt.config(state='disabled')
            self.passwordtxt.config(state='disabled')

        if self.authenticationopt.get() == self.app_constants.APPLICATION_AUTHENTICATION_SQL:
            self.useridtxt.config(state='normal')
            self.passwordtxt.config(state='normal')

    def func_connect(self):
        self.sessiondetails = SessionDetails(self.servernametxt.get(), self.authenticationopt.get(),
                                             self.useridtxt.get(), self.passwordtxt.get())
        # self.func_unit_test()
        # Validate Input Fields
        self.func_validate()
        if self.error != "":
            self.show_error()
        else:
            self.error = test_connection(self.sessiondetails)

            if self.error != "":
                self.show_error()
                self.reset_to_default()
            else:
                if check_application_installation_Status(self.sessiondetails):
                    self.master.destroy()
                    homepage = Tk()
                    homepage.focus_force()
                    Home(homepage, self.sessiondetails)
                else:
                    self.master.destroy()
                    installpage = Tk()
                    installpage.focus_force()
                    Install(installpage, self.sessiondetails)


    def func_validate(self):
        if len(self.sessiondetails.getHost()) == 0:
            self.error = "Please enter server name."
        elif self.sessiondetails.isWindowsAuthenticated() != 1 and len(self.sessiondetails.getUser()) == 0:
            self.error = "Please enter user id."
        elif self.sessiondetails.isWindowsAuthenticated() != 1 and len(self.sessiondetails.getPassword()) == 0:
            self.error = "Please enter password."


def main():
    root = Tk()
    root.focus_force()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    DataNxtLogin(root)
    appconstants = ApplicationConstants()
    root.title(appconstants.APPLICATION_TITLE)
    # root.iconbitmap(appconstants.APPLICATION_ICON)
    root.geometry(appconstants.APPLICATION_LOGIN_GEOMETRY)
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == '__main__':
    main()
