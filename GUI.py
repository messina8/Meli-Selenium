import tkinter
import tkinter.messagebox
import customtkinter as ctki


class App(ctki.CTk):
    WIDTH = 600
    HEIGHT = 720

    def __init__(self):
        super().__init__()

        self.title('Melenium')
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.textbox = ctki.CTkTextbox(master=self)
        self.textbox.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 0), sticky="nsew")

        self.tech_check = ctki.CTkCheckBox(master=self, text="Fill Tech", onvalue="on", offvalue="off")
        self.tech_check.grid(row=1, column=0, padx=20, pady=20, sticky='')

        self.price_check = ctki.CTkCheckBox(master=self, text="Change Price", onvalue="on", offvalue="off")
        self.price_check.grid(row=1, column=1, padx=20, pady=20, sticky='')

        self.change_stock = ctki.CTkCheckBox(master=self, text="Change Stock", onvalue="on", offvalue="off")
        self.change_stock.grid(row=1, column=2, padx=20, pady=20, sticky='')

        self.new_price = ctki.CTkEntry(master=self, placeholder_text='Enter new price')
        self.new_price.grid(row=2, column=1, padx=20, pady=20, sticky='ew')

        self.stock_change = ctki.CTkEntry(master=self, placeholder_text='Enter stock change')
        self.stock_change.grid(row=2, column=2, padx=20, pady=20, sticky='ew')

        self.publication = ctki.CTkEntry(master=self, placeholder_text='Enter title or publi ID')
        self.publication.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky='ew')

        self.submit = ctki.CTkButton(master=self, text='Go')
        self.submit.grid(row=4, column=1, columnspan=2, padx=20, pady=20, sticky='ew')

        self.mass_edit = ctki.CTkButton(master=self, text='Mass edit')
        self.mass_edit.grid(row=4, column=0, padx=20, pady=20, sticky='ew')

    def button_event(self):
        pass

    def on_closing(self, event=0):
        self.destroy()


app = App()
app.mainloop()
