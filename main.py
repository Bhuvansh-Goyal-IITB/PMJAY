import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pdf_maker import make_pdf, FIRST_BOUND, SECOND_BOUND
import tkcalendar
from datetime import datetime, timedelta

import os
import threading
from config import *

def print_pdf(print_button: ttk.Button):
    try:
        pdf_files = [f for f in sorted(os.listdir(OUTPUT_DIR)) if f.endswith(".pdf")]

        for pdf_file in pdf_files:
            pdf_path = os.path.join(OUTPUT_DIR, pdf_file)
            os.startfile(pdf_path, "print")
    except Exception as e:
        messagebox.showerror("Error", f"An error occured: {e}")
    
    print_button.config(state=tk.ACTIVE)

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def add_day_to_date(date_string):
    date_format = "%d/%m/%Y"
    date_object = datetime.strptime(date_string, date_format)
    new_date = date_object + timedelta(days=1)
    new_date_string = new_date.strftime(date_format)

    return new_date_string

def get_day_of_admission(date_of_admission, current_date_string):
    date_format = "%d/%m/%Y"
    date1 = datetime.strptime(date_of_admission, date_format)
    date2 = datetime.strptime(current_date_string, date_format)

    date_difference = date2 - date1
    age = date_difference.days + 1
    return "DAY " + str(age) 
    
def get_age(dob_string, current_date_string):
    date_format = "%d/%m/%Y"
    date1 = datetime.strptime(dob_string, date_format)
    date2 = datetime.strptime(current_date_string, date_format)

    date_difference = date2 - date1
    age = date_difference.days + 1
    return str(age) + (" DAY" if age == 1 else " DAYS")

def clean_output_folder():
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    else:
        output_files = os.listdir(OUTPUT_DIR)
        for file in output_files:
            os.remove(os.path.join(OUTPUT_DIR, file))
    
def save_patient(form_dict):
    pass

def load_patient():
    pass

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PMJAY")
        self.iconbitmap(os.path.join(ASSETS_DIR, "app_icon.ico"))
        self.resizable(False, False)

        self.panel = Panel(self)
        self.panel.pack(expand=True, fill='both', padx=10, pady=(10, 0))   

        self.frame = ttk.Frame(self) 
        self.frame.pack(padx=20, pady=(0, 20))

        self.print_button = ttk.Button(self.frame, command=self.print, text='Print Report')
        self.print_button.pack(side='left', expand=True, padx=20)
        self.print_button.bind('<Return>', lambda event: self.print_button.invoke())

        self.clear_button = ttk.Button(self.frame, command=self.panel.clear, text='Clear')
        self.clear_button.pack(side='left', expand=True, padx=20)
        self.clear_button.bind('<Return>', lambda event: self.clear_button.invoke())

        self.mainloop()
    
    def save(self):
        pass

    def print(self):
        self.print_button.config(state=tk.DISABLED)
        try:
            clean_output_folder()
            form_dict = {widget.label_var.get(): widget.get() for widget in self.panel.widgets}
            
            number_of_reports = int(form_dict["Number of Days"])
            
            form_dict.pop("Number of Days")

            form_dict["Gender"] = f"({form_dict["Gender"]})"
            for i in range(1, number_of_reports + 1):
                form_dict["Day of Admission"] = get_day_of_admission(form_dict["Date of Admission"], form_dict["Date"]) 
                form_dict["Age"] = get_age(form_dict["Date of Birth"], form_dict["Date"])
                make_pdf(form_dict, i)

                form_dict["Weight"] = ""
                form_dict["Date"] = add_day_to_date(form_dict["Date"])

            printing_thread = threading.Thread(target=print_pdf, args=[self.print_button])
            printing_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"An error occured: {e}")
            self.print_button.config(state=tk.ACTIVE)
    
class LabelledEntry(ttk.Frame):
    def __init__(self, master, label_text, is_address, is_date, is_gender):
        super().__init__(master)

        self.entry_var = tk.StringVar()
        self.previous_value = None
        
        if not is_address:
            self.columnconfigure(0, weight=1, uniform='a')
            self.columnconfigure(1, weight=2, uniform='a')
            self.rowconfigure(0, weight=1, uniform='a')

            if label_text == "Age":
                self.entry_var.trace_add("write", self.check_number_entry)
            elif label_text == "Number of Days":
                self.entry_var.trace_add("write", self.check_number_entry)
        else:
            self.columnconfigure(0, weight=1, uniform='a')
            self.columnconfigure(1, weight=5, uniform='a')
            self.rowconfigure(0, weight=1, uniform='a')
        
        self.label_var = tk.StringVar()
        self.label_var.set(label_text)
        self.label = ttk.Label(self, textvariable=self.label_var)
        self.label.grid(row=0, column=0, sticky='e', padx=10)

        if is_date:
            self.entry = tkcalendar.DateEntry(self, textvariable=self.entry_var, date_pattern="dd/mm/yyyy")
        elif label_text == "Number of Days":
            self.entry_var.set(1)
            self.entry = NumberBox(self, self.entry_var)
        elif is_gender:
            self.entry_var.set("Male")
            self.entry = ttk.Combobox(self, textvariable=self.entry_var, values=["Male", "Female"])
        else:
            self.entry = ttk.Entry(self, textvariable=self.entry_var)
        self.entry.grid(row=0, column=1, sticky='ew')

    def clear(self):
        if self.label_var.get() == "Number of Days":
            self.entry_var.set(1)
            return
        if self.label_var.get().split(" ")[0] == "Date":
            self.entry_var.set(datetime.now().strftime("%d/%m/%Y"))
            return
        self.entry_var.set('')

    def get(self):
        return self.entry_var.get()

    def check_number_entry(self, *args):
        value = self.entry_var.get()
        if value == "":
            self.previous_value = None
            self.entry_var.set("")
            return
        
        if value.isdigit():
            self.previous_value = int(value)
            self.entry_var.set(str(self.previous_value)) 
        elif self.previous_value:
            self.entry_var.set(str(self.previous_value)) 
        else:
            self.entry_var.set("")

class NumberBox(ttk.Frame):
    def __init__(self, master, text_variable: tk.StringVar):
        super().__init__(master)

        self.text_variable = text_variable
        self.text_variable.set(1)

        self.columnconfigure((0, 1, 2), weight=1, uniform='c')
        self.rowconfigure(0, weight=1, uniform='c')

        self.subtract_button = ttk.Button(self, text="-", command=self.subtract)
        self.subtract_button.grid(row=0, column=0)

        self.label = ttk.Label(self, textvariable=text_variable)
        self.label.grid(row=0, column=1)

        self.add_button = ttk.Button(self, text="+", command=self.add)
        self.add_button.grid(row=0, column=2)

    def add(self):
        self.text_variable.set(int(self.text_variable.get()) + 1)

    def subtract(self):
        value = int(self.text_variable.get())
        if value > 1:
            self.text_variable.set(value - 1)
        else:
            self.text_variable.set(1)

class Panel(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure((0, 1), weight=1, uniform='b')
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='b')
        
        self.widgets = []
        fields = [field for field in list(FIELDS.keys()) if (field != "Day of Admission" and field != "Age")]
        fields.append("Number of Days")
        for i, field in enumerate(fields):
            widget = LabelledEntry(self, field, i == 2, (i == 1 or i == 4 or i == 5), i == 7)
            if i == 2:
                widget.grid(row=i // 2, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
            else:
                if i >= 3:
                    i += 1
                widget.grid(row=i // 2, column= 0 if i % 2 == 0 else 1, sticky='nsew', padx=5, pady=5)
            self.widgets.append(widget)
    def clear(self):
        for widget in self.widgets:
            widget.clear()

if __name__ == "__main__":
    app = App()