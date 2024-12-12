import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import subprocess
import json
import Pmw
import threading

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Program Launcher and Console")

        # Initialize Balloon for tooltips
        Pmw.initialise(master)
        self.balloon = Pmw.Balloon(master)

        # Create start investigation window
        self.start_window = tk.Toplevel(master)
        self.start_window.title("Start Investigation")
        self.start_window.geometry("400x150")
        self.start_window.position(500,500)
        self.target_label = ttk.Label(self.start_window, text="Enter domain name or select a file:")
        self.target_label.pack(pady=5)
        self.target_entry = ttk.Entry(self.start_window, width=50)
        self.target_entry.pack(pady=5)
        self.browse_button = ttk.Button(self.start_window, text="Browse", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.run_button = ttk.Button(self.start_window, text="Run", command=self.start_investigation)
        self.run_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Create frames
        self.console_frame = ttk.Frame(master)
        self.console_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.target_frame = ttk.Frame(master)
        self.target_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        self.bottom_frame = ttk.Frame(master)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.programs_frame = ttk.Frame(self.bottom_frame, width=30)
        self.programs_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.command_frame = ttk.Frame(self.bottom_frame, width=30)
        self.command_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.launch_frame = ttk.Frame(self.bottom_frame, width=30)
        self.launch_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create widgets for console frame
        self.console_text = tk.Text(self.console_frame, wrap='word', height=20)
        self.console_text.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.console_frame, command=self.console_text.yview)
        self.console_text['yscrollcommand'] = self.scrollbar.set
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create widgets for target frame
        self.target_text = ttk.Entry(self.target_frame, width=50)
        self.target_text.pack(side=tk.LEFT, padx=5)
        self.change_button = ttk.Button(self.target_frame, text="Change!", command=self.change_target)
        self.change_button.pack(side=tk.LEFT)

        # Create widgets for programs frame
        self.programs_listbox = tk.Listbox(self.programs_frame, width=30)
        self.programs_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.add_button = ttk.Button(self.programs_frame, text="Add to Launch List", command=self.add_to_launch_list)
        self.add_button.pack(side=tk.BOTTOM)

        # Help button
        self.help_button = ttk.Button(self.programs_frame, text="?", style="Help.TButton", command=self.show_help)
        self.help_button.place(relx=0.95, rely=0.01, anchor=tk.NE)

        # Create widgets for launch frame
        self.launch_listbox = tk.Listbox(self.launch_frame, width=30)
        self.launch_listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.run_button = ttk.Button(self.launch_frame, text="Run Code List", command=self.run_code_list)
        self.run_button.pack(side=tk.BOTTOM)

        self.remove_button = ttk.Button(self.launch_frame, text="Remove", command=self.remove_from_launch_list)
        self.remove_button.pack(side=tk.BOTTOM)

        self.clear_button = ttk.Button(self.launch_frame, text="Clear", command=self.clear_launch_list)
        self.clear_button.pack(side=tk.BOTTOM)

        # Create widgets for command frame
        self.command_text = tk.Text(self.command_frame, wrap='word', width=30)
        self.command_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Load programs from configuration file
        self.load_programs()

        # Bind events for tooltips and selection changes
        self.programs_listbox.bind('<Motion>', self.show_tooltip)
        self.launch_listbox.bind('<<ListboxSelect>>', self.update_command_text)

        # Style the help button
        style = ttk.Style()
        style.configure("Help.TButton", font=("Helvetica", 12, "bold"), relief=tk.RAISED, borderwidth=2, background="lightblue", foreground="black")

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.target_entry.delete(0, tk.END)
            self.target_entry.insert(0, file_path)

    def start_investigation(self):
        target = self.target_entry.get()
        if os.path.isfile(target):
            target_file = target
            target = os.path.basename(target_file).split('.')[0]
            os.environ['TARGET_FILE'] = target_file
            self.console_text.insert(tk.END, f"Selected file: {target_file}\n")
        else:
            target_file = None
            if os.getcwd() != os.path.expanduser('~/work/'):
                os.chdir(os.path.expanduser('~/work/'))
            if not os.path.exists(target):
                os.makedirs(target)
            os.chdir(target)
            os.environ['TARGET'] = target
            self.console_text.insert(tk.END, f"Created directory {target} and changed into it.\n")
            self.console_text.insert(tk.END, f"Current working directory: {os.getcwd()}\n")

        self.console_text.insert(tk.END, f"Bash global variable set: TARGET={os.environ.get('TARGET', '')}\n")
        self.console_text.insert(tk.END, f"Bash global variable set: TARGET_FILE={os.environ.get('TARGET_FILE', '')}\n")

        self.start_window.destroy()

    def load_programs(self):
        try:
            with open(os.path.expanduser("/home/kali/tools/vizualist/programs.json")) as f:
                self.programs = json.load(f)
            for program in self.programs:
                self.programs_listbox.insert(tk.END, program["name"])
        except FileNotFoundError:
            messagebox.showerror("Error", "The 'programs.json' file was not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "The 'programs.json' file is not valid JSON.")

    def add_to_launch_list(self):
        selected_index = self.programs_listbox.curselection()
        if selected_index:
            selected_program = self.programs[selected_index[0]]
            self.launch_listbox.insert(tk.END, selected_program["name"])
            self.update_command_text()

    def remove_from_launch_list(self):
        selected_index = self.launch_listbox.curselection()
        if selected_index:
            self.launch_listbox.delete(selected_index)
            self.update_command_text()

    def clear_launch_list(self):
        self.launch_listbox.delete(0, tk.END)
        self.update_command_text()

    def run_code_list(self):
        self.console_text.delete(1.0, tk.END)
        threads = []
        for program_name in self.launch_listbox.get(0, tk.END):
            thread = threading.Thread(target=self.run_program, args=(program_name,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def run_program(self, program_name):
        try:
            program = next(p for p in self.programs if p["name"] == program_name)
            command = program["cmd"]
            self.console_text.insert(tk.END, f"Running: {command}\n")
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, error = process.communicate()
            self.console_text.insert(tk.END, f"{program_name} Output:\n{output.decode()}\n")
            self.console_text.insert(tk.END, f"{program_name} Errors:\n{error.decode()}\n")
        except Exception as e:
            self.console_text.insert(tk.END, f"Error running {program_name}: {str(e)}\n")

    def show_tooltip(self, event):
        index = self.programs_listbox.nearest(event.y)
        if index >= 0:
            program = self.programs[index]
            self.balloon.bind(self.programs_listbox, program["description"], program["name"])

    def update_command_text(self, event=None):
        self.command_text.delete(1.0, tk.END)
        for program_name in self.launch_listbox.get(0, tk.END):
            program = next(p for p in self.programs if p["name"] == program_name)
            self.command_text.insert(tk.END, f"{program['cmd']}\n")

    def change_target(self):
        new_target = self.target_text.get()
        if new_target:
            os.environ['TARGET'] = new_target
            self.console_text.insert(tk.END, f"TARGET changed to: {new_target}\n")

    def show_help(self):
        selected_index = self.programs_listbox.curselection()
        if selected_index:
            program_name = self.programs_listbox.get(selected_index)
            program = next(p for p in self.programs if p["name"] == program_name)
            command = program["cmd"].split()[0] + " --help"
            self.console_text.insert(tk.END, f"Running help for: {command}\n")
            try:
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()
                self.console_text.insert(tk.END, f"Help Output:\n{output.decode()}\n")
                self.console_text.insert(tk.END, f"Help Errors:\n{error.decode()}\n")
            except Exception as e:
                self.console_text.insert(tk.END, f"Error running help for {program_name}: {str(e)}\n")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    gui = GUI(root)
    root.mainloop()
