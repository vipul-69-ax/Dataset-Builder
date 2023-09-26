import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import time
import os
import threading
from scrape import *

def onSubmit(save_path, search_query, num_pages, include_csv, enhance):
    image_links = scrape_images(search_query, int(num_pages))
    save_images(save_path, image_links)
    if include_csv == "Yes":
        write_array_to_csv(image_links, f"{save_path}/image_output.csv")

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:  
        folder_entry.delete(0, tk.END)  
        folder_entry.insert(0, folder_path)

def clear_inputs():
    folder_entry.delete(0, tk.END)
    numerical_entry.delete(0, tk.END)
    string_entry.delete(0, tk.END)
    include_csv_var.set("")
    enhance_images_var.set(False)

def run_onSubmit(folder_path, string_input, numerical_input, include_csv, enhance):
    thread = threading.Thread(target=onSubmit, args=(
        folder_path, string_input, numerical_input, include_csv, enhance))
    thread.start()
    thread.join()
    clear_inputs()
    submit_button.config(state=tk.NORMAL)

def submit():
    folder_path = folder_entry.get()
    numerical_input = numerical_entry.get()
    string_input = string_entry.get()
    include_csv = include_csv_var.get()  
    enhance_images_check = enhance_images_var.get()

    if not numerical_input.isdigit():
        result_label.config(
            text="Numerical Input must be a valid number.", foreground="red")
        return

    submit_button.config(state=tk.DISABLED)
    root.update()

    if folder_path and string_input and numerical_input:
        run_onSubmit(folder_path, string_input, numerical_input, include_csv, enhance_images_check)


    submit_button.config(state=tk.NORMAL)

root = tk.Tk()
root.title("Image Dataset Builder")
root.configure(bg="white")

style = ttk.Style()
style.configure("TFrame", background="white")
style.configure("TLabel", font=("Helvetica", 14), background="white", padding=10)
style.configure("TEntry", font=("Helvetica", 14), padding=(10, 5))
style.configure("TButton", font=("Helvetica", 14), padding=10)

input_frame = ttk.Frame(root)
input_frame.pack(pady=20)

folder_label = ttk.Label(input_frame, text="Select a Folder:")
folder_entry = ttk.Entry(input_frame, width=40)
browse_button = ttk.Button(input_frame, text="Browse", command=browse_folder)

numerical_label = ttk.Label(input_frame, text="Number of pages to search:")
numerical_entry = ttk.Entry(input_frame, width=40)

string_label = ttk.Label(input_frame, text="Enter a String:")
string_entry = ttk.Entry(input_frame, width=40)

include_csv_label = ttk.Label(input_frame, text="Include CSV:")
include_csv_var = tk.StringVar()
include_csv_combobox = ttk.Combobox(input_frame, textvariable=include_csv_var, values=["Yes", "No"])

enhance_images_label = ttk.Label(input_frame, text="Enhance Image(Time Consuming):")
enhance_images_var = tk.BooleanVar()
enhance_images_checkbox = ttk.Checkbutton(input_frame, variable=enhance_images_var)

submit_button = ttk.Button(input_frame, text="Submit", command=submit, width=15)

result_label = ttk.Label(root, text="", wraplength=400, font=("Helvetica", 14))
result_label.pack(fill="both", expand=True, padx=20, pady=20)

folder_label.grid(row=0, column=0, padx=(10, 5), pady=(10, 0), sticky="w")
folder_entry.grid(row=0, column=1, padx=(0, 5), pady=(10, 0))
browse_button.grid(row=0, column=2, pady=(10, 0))

numerical_label.grid(row=1, column=0, padx=(10, 5), sticky="w")
numerical_entry.grid(row=1, column=1, padx=(0, 5))
string_label.grid(row=2, column=0, padx=(10, 5), sticky="w")
string_entry.grid(row=2, column=1, padx=(0, 5))

include_csv_label.grid(row=3, column=0, padx=(10, 5), pady=(10, 0), sticky="w")
include_csv_combobox.grid(row=3, column=1, padx=(0, 5), pady=(10, 0))

enhance_images_label.grid(row=4, column=0, padx=(10, 5), pady=(10, 0), sticky="w")
enhance_images_checkbox.grid(row=4, column=1, padx=(0, 5), pady=(10, 0))

submit_button.grid(row=5, column=1, pady=(20, 0))

input_frame.grid_rowconfigure(6, weight=1)
input_frame.grid_columnconfigure((0, 1, 2), weight=1)

def on_resize(event):
    result_label.config(wraplength=root.winfo_width() - 40)

root.bind("<Configure>", on_resize)

root.mainloop()
