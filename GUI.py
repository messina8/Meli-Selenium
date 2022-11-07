import tkinter
import tkinter.messagebox
import customtkinter as ctki
import selenium_controller as controller


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

        self.textbox = ctki.CTkTextbox(master=self, state='disabled')
        self.textbox.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 0), sticky="nsew")

        self.tech_check = ctki.CTkCheckBox(master=self, text="Fill Tech", onvalue="on", offvalue="off")
        self.tech_check.grid(row=1, column=0, padx=20, pady=20, sticky='')

        self.price_check = ctki.CTkCheckBox(master=self, text="Change Price", onvalue="on", offvalue="off")
        self.price_check.grid(row=1, column=1, padx=20, pady=20, sticky='')

        self.stock_check = ctki.CTkCheckBox(master=self, text="Change Stock", onvalue="on", offvalue="off")
        self.stock_check.grid(row=1, column=2, padx=20, pady=20, sticky='')

        self.new_price = ctki.CTkEntry(master=self, placeholder_text='Enter new price')
        self.new_price.grid(row=2, column=1, padx=20, pady=20, sticky='ew')

        self.stock_change = ctki.CTkEntry(master=self, placeholder_text='Enter stock change')
        self.stock_change.grid(row=2, column=2, padx=20, pady=20, sticky='ew')

        self.publication = ctki.CTkEntry(master=self, placeholder_text='Enter title or publi ID')
        self.publication.grid(row=3, column=0, columnspan=3, padx=20, pady=20, sticky='ew')

        self.submit = ctki.CTkButton(master=self, text='Go', command=self.single_edit)
        self.submit.grid(row=4, column=1, columnspan=2, padx=20, pady=20, sticky='ew')

        self.mass_edit_button = ctki.CTkButton(master=self, text='Mass edit', command=self.mass_edit)
        self.mass_edit_button.grid(row=4, column=0, padx=20, pady=20, sticky='ew')
        self.mass_edit_button.configure()

        self.log = []

        self.browser = controller.open_driver()
        controller.load_meli(self.browser)

    def mass_edit(self):
        self.print_out('mass edit working')

    def single_edit(self):
        publi_id = self.publication.get()
        self.print_out(f'Looking for {publi_id}')
        if self.price_check.get() == 'on' and self.new_price.get() != '':
            new_price = self.new_price.get()
            self.print_out(f'changing {publi_id} price to {new_price}')
        if self.tech_check.get() == 'on':
            self.print_out(f'filling {publi_id} specs')
        if self.stock_check.get() == 'on' and self.stock_change.get() != '':
            self.print_out(f'Chagning stock by {self.stock_change.get()}')

    def on_closing(self, event=0):
        self.destroy()
        self.browser.close()

    def print_out(self, entry):
        if len(self.log) < 25:
            self.log.append(entry)
        else:
            del self.log[0]
            self.log.append(entry)
        self.textbox.configure(state='normal')
        self.textbox.delete('1.0', 'end')
        self.textbox.insert('0.0', '\n'.join(self.log))
        self.textbox.configure(state='disabled')


app = App()
app.mainloop()
