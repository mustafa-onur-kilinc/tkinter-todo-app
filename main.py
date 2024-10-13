"""
Resources used while writing this code:
Reblochon Masque 2018, 
"How to position several widgets side by side, on one line, with tkinter?",
Stack Exchange Inc., accessed 11 September 2024, 
<https://stackoverflow.com/a/51631176>

Gaurav Leekha 2024, 
"How to allow Tkinter to generate a listbox from list input?",
Tutorials Point India Private Limited, accessed 11 September 2024,
<https://www.tutorialspoint.com/how-to-allow-tkinter-to-generate-a-listbox-from-list-input>

Tkinter Listbox n.d., Tutorials Point India Private Limited, 
accessed 11 September 2024,
<https://www.tutorialspoint.com/python/tk_listbox.htm>

John W. Shipman 2013, "54.2. Event sequences", accessed 11 September 2024,
<https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/event-sequences.html>

John W. Shipman 2013, "54.3. Event types", accessed 15 September 2024,
<https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/event-types.html>

Dev Prakash Sharma 2021, "How do I create a date picker in tkinter?",
Tutorials Point India Private Limited, accessed 11 September 2024,
<https://www.tutorialspoint.com/how-do-i-create-a-date-picker-in-tkinter>

tkcalendar 1.6.1 n.d., Python Software Foundation, 
accessed 11 September 2024,
<https://pypi.org/project/tkcalendar/#widget-methods-1>

RayLuo 2016, 
"Define functions with too many arguments to abide by PEP8 standard",
Stack Exchange Inc., accessed 15 September 2024, 
<https://stackoverflow.com/a/39217514>

Guido van Rossum et.al. 2024, "Indentation", accessed 15 September 2024,
<https://peps.python.org/pep-0008/#indentation>

Bite code n.d., "How to print a date in a regular format?",
Stack Exchange Inc., accessed 19 September 2024,
<https://stackoverflow.com/a/311655>

Bryan Oakley 2017, "Setting tk.Frame width and height",
Stack Exchange Inc., accessed 16 September 2024,
<https://stackoverflow.com/a/44829742>

Dev Prakash Sharma 2021, 
"How do I create child windows with Python tkinter?",
Tutorials Point India Private Limited, accessed 16 September 2024,
<https://www.tutorialspoint.com/how-do-i-create-child-windows-with-python-tkinter>

tkinter.messagebox — Tkinter message prompts n.d., 
Python Software Foundation, accessed 16 September 2024,
<https://docs.python.org/3/library/tkinter.messagebox.html>

John W. Shipman 2013, "26. Universal widget methods", 
accessed 19 September 2024,
<https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/universal.html>

strftime() and strptime() Format Codes n.d., Python Software Foundation,
accessed 19 September 2024,
<https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>

cullzie 2019, "TypeError: <lambda>() takes 0 positional arguments but 1 
was given due to monkeypatching "input" in a test", Stack Exchange Inc.,
accessed 19 September 2024,
<https://stackoverflow.com/a/54641848>

John W. Shipman 2013, "5.4. Type fonts", accessed 19 September 2024,
<https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/fonts.html>

John W. Shipman 2013, "12. The Label widget", accessed 19 September 2024,
<https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/label.html>

Style Guide n.d., numpydoc maintainers, accessed 11 October 2024,
<https://numpydoc.readthedocs.io/en/latest/format.html#sections>
"""

import os
import json
import yaml
import datetime
import tkinter as tk

from tkcalendar import DateEntry
from tkinter import messagebox
from typing import Union

def parse_yaml_file(yaml_dir: str) -> dict:
    """
    Reads a YAML file, returns its content as a dictionary

    Parameters
    ----------
    yaml_dir : str
        Path of YAML file to read

    Returns
    ----------
    resulting_dict : dict
        Dictionary that includes content of YAML file
    """
    
    with open(yaml_dir, "r") as yaml_file:
        resulting_dict: dict = yaml.safe_load(yaml_file)

    return resulting_dict

class TODO_App_GUI():
    def __init__(self) -> None:
        current_dir = os.path.dirname(__file__)
        yaml_dir = os.path.join(current_dir, "todo_app_config.yaml")
        self.config_dict = parse_yaml_file(yaml_dir)

        save_filename: str = "saved_tasks.json"
        self.json_dir = os.path.join(current_dir, save_filename)

        self.tasks_list: list = []

        self.root = tk.Tk()

        self.init_gui()

        self.load_tasks()

    def init_gui(self) -> None:
        """
        Creates the GUI window and binds functions to keys and keyboard
        shortcuts

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        
        self.root.geometry(self.config_dict["geometry"])
        self.root.title(self.config_dict["window_names"]["main_window"])

        upperside_frame = tk.Frame(
            master=self.root, 
            bg=self.config_dict["bg_color"]["frame_bg_1"],
            name="upperside_frame"
        )
        upperside_frame.pack(fill=tk.X, side=tk.TOP)
    
        create_task_frame = tk.Frame(
            master=upperside_frame, 
            bg=self.config_dict["bg_color"]["frame_bg_1"],
            name="create_task_frame"
        )
        create_task_frame.pack(fill=tk.NONE, anchor=tk.CENTER, ipady=10)
    
        create_task_button = tk.Button(
            master=create_task_frame, 
            bg=self.config_dict["bg_color"]["button_bg"], 
            relief=tk.FLAT, 
            text=self.config_dict["button_texts"]["create_task_button"],
            command=self.open_task_create_window,
            name="create_task_button"
        )
        create_task_button.pack(fill=tk.NONE, side=tk.LEFT, padx=10)

        save_tasks_button = tk.Button(
            master=create_task_frame,
            bg=self.config_dict["bg_color"]["button_bg"],
            relief=tk.FLAT,
            text=self.config_dict["button_texts"]["save_tasks_button"],
            command=self.save_tasks,
            name="save_tasks_button"
        )
        save_tasks_button.pack(fill=tk.NONE, side=tk.LEFT, padx=10)
    
        self.downside_frame = tk.Frame(
            master=self.root, 
            bg=self.config_dict["bg_color"]["frame_bg_3"],
            name="downside_frame"
        )
        self.downside_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.root.bind("<Key-Return>", self.open_task_create_window)
        self.root.bind("<Control-Key-S>", self.save_tasks)

    def save_tasks(self, event: Union[tk.Event, None] = None) -> None:
        """
        Saves tasks in tasks list to a JSON file

        Parameters
        ----------
        event : tk.Event or None, default: None
            A key press event that lets a user saving tasks with a 
            keyboard shortcut. Default is None

        Returns
        ----------
        None
        """
        
        with open(self.json_dir, "w") as json_savefile:
            json.dump(obj=self.tasks_list, fp=json_savefile, indent=2)

    def load_tasks(self) -> None:
        """
        Loads tasks from JSON file, creates task frames for each task

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """
        
        with open(self.json_dir, "r") as json_file:
            self.tasks_list: list = json.load(fp=json_file)

        for task in self.tasks_list:
            deadline: datetime.date = datetime.datetime.strptime(
                task.get("deadline"), "%d-%m-%Y")
            
            task_frame = self.create_task_frame(
                root=self.downside_frame, 
                task_name=task.get("task_name"),
                deadline=deadline,
                task_completed=task.get("completed"),
                bg=self.config_dict["bg_color"]["frame_bg_2"])

            task_frame.pack(fill=tk.X, side=tk.TOP, padx=6, pady=3)

    def open_task_create_window(
            self, 
            event: Union[tk.Event, None] = None) -> None:
        """
        Opens a separate window for user to enter task name and deadline
        of a task they want to create

        Parameters
        ----------
        event : tk.Event or None, default: None
            A key press event that lets a user saving tasks with a 
            keyboard shortcut. Default is None

        Returns
        ----------
        None
        """
        
        self.task_creation_window = tk.Toplevel(
            master=self.root, 
            bg=self.config_dict["bg_color"]["frame_bg_3"],
            name="task_creation_window"
        )
        self.task_creation_window.geometry("300x250")
        self.task_creation_window.title(
            self.config_dict["window_names"]["task_create_window"]
        )

        task_data_frame = tk.Frame(
            master=self.task_creation_window,
            bg=self.config_dict["bg_color"]["frame_bg_3"],
            name="task_data_frame"
        )
        task_data_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        create_task_button_frame = tk.Frame(
            master=self.task_creation_window,
            bg=self.config_dict["bg_color"]["frame_bg_3"],
            name="create_task_button_frame"
        )
        create_task_button_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.task_name_var = tk.StringVar(name="task_name")
        create_task_entry = tk.Entry(
            master=task_data_frame, 
            bg=self.config_dict["bg_color"]["entry_bg"], 
            relief=tk.FLAT,
            textvariable=self.task_name_var,
            name="create_task_entry"
        )
        create_task_entry.pack(fill=tk.NONE, side=tk.LEFT, padx=10)

        self.create_task_date = DateEntry(
            master=task_data_frame,
            bg=self.config_dict["bg_color"]["entry_bg"],
            name="create_task_date"
        )
        self.create_task_date.pack(fill=tk.NONE, side=tk.LEFT, padx=10)

        create_task_button = tk.Button(
            master=create_task_button_frame, 
            bg=self.config_dict["bg_color"]["button_bg"], 
            relief=tk.FLAT, 
            text=self.config_dict["button_texts"]["create_task_button"],
            command=self.add_task,
            name="create_task_button"
        )
        create_task_button.pack(fill=tk.NONE, side=tk.TOP, padx=10)

        create_task_entry.focus()

        self.task_creation_window.bind(
            sequence="<Key-Return>", func=self.add_task
        )

    def add_task(self, event: Union[tk.Event, None] = None) -> None:
        """
        Adds user entered task to tasks list, calls create_task_frame
        function for the task, closes the task creation window

        Parameters
        ----------
        event : tk.Event or None, default: None
            A key press event that lets a user saving tasks with a 
            keyboard shortcut. Default is None

        Returns
        ----------
        None
        """

        task_name: str = self.task_name_var.get()
        deadline: datetime.date = self.create_task_date.get_date()

        if not self.is_user_input_valid(task_name=task_name, deadline=deadline):
            return
            
        task_entry: dict = {"task_name": task_name, 
                            "deadline": deadline.strftime(format="%d-%m-%Y"),
                            "completed": False}
        self.tasks_list.append(task_entry)

        task_frame = self.create_task_frame(
            root=self.downside_frame, task_name=task_name,
            deadline=deadline, bg=self.config_dict["bg_color"]["frame_bg_2"])
        task_frame.pack(fill=tk.X, side=tk.TOP, padx=6, pady=3)

        self.task_creation_window.destroy()

    def create_task_frame(
            self, 
            root: tk.Frame, 
            task_name: str, 
            deadline: datetime.date,
            bg: str,
            task_completed: bool = False) -> tk.Frame:
        """
        Opens a separate window for user to enter task name and deadline
        of a task

        Parameters
        ----------
        root : tk.Frame
            Parent frame for the tkinter frame created here
        task_name : str
            Name of task to create
        deadline : datetime.date
            Deadline of task to create
        bg : str
            Background color of tkinter frame created here
        task_completed : bool, default: False
            Info of whether a task is marked as finished or unfinished.
            Important when loading tasks from JSON file

        Returns
        ----------
        task_frame : tk.Frame
            A tkinter frame that includes a checkbox, task info and
            edit and delete buttons
        """

        task_frame = tk.Frame(master=root, bg=bg)

        checkbutton_variable = tk.IntVar(master=task_frame)
        checkbutton_variable.set(1 if task_completed else 0)

        task_finished_checkbutton = tk.Checkbutton(
            master=task_frame, 
            bg=self.config_dict["bg_color"]["frame_bg_2"],
            variable=checkbutton_variable,
            name="task_finished_checkbox"
        )
        task_finished_checkbutton.pack(fill=tk.NONE, side=tk.LEFT, padx=5)

        task_info_frame = tk.Frame(
            master=task_frame, 
            bg=self.config_dict["bg_color"]["frame_bg_2"],
            name="task_info_frame"
        )
        task_info_frame.pack(fill=tk.NONE, side=tk.LEFT, padx=5, ipadx=2)

        task_name_label = tk.Label(
            master=task_info_frame, 
            bg=self.config_dict["bg_color"]["frame_bg_2"],
            fg=self.config_dict["text_color"]["primary"], 
            font=("Arial", 15, "bold"), text=task_name,
            name="task_name_label"
        )
        task_name_label.pack(fill=tk.NONE, side=tk.TOP)

        formatted_deadline: str = deadline.strftime(format="%d-%m-%Y")
        task_deadline_label = tk.Label(
            master=task_info_frame, 
            bg=self.config_dict["bg_color"]["frame_bg_2"],
            fg=self.config_dict["text_color"]["secondary"],
            font=("Arial", 10, "normal"), text=formatted_deadline,
            name="task_deadline_label"
        )
        task_deadline_label.pack(fill=tk.NONE, side=tk.TOP)

        task_buttons_frame = tk.Frame(
            master=task_frame, 
            bg=self.config_dict["bg_color"]["frame_bg_2"],
            name="buttons_frame"
        )
        task_buttons_frame.pack(fill=tk.NONE, side=tk.RIGHT, padx=5)

        task_delete_button = tk.Button(
            master=task_buttons_frame, 
            bg=self.config_dict["bg_color"]["frame_bg_1"],
            fg=self.config_dict["text_color"]["inverted"], 
            font=("Arial", 12, "normal"), 
            text=self.config_dict["button_texts"]["delete_task_button"],
            relief=tk.FLAT,
            command=lambda: self.delete_task_frame(
                checkbutton_variable, task_frame, 
                task_name_label, task_deadline_label
            ),
            name="delete_button"
        )
        task_delete_button.pack(fill=tk.NONE, side=tk.RIGHT, padx=1)

        task_edit_button = tk.Button(
            master=task_buttons_frame, 
            bg=self.config_dict["bg_color"]["button_bg"],
            fg=self.config_dict["text_color"]["primary"], 
            font=("Arial", 12, "normal"),
            text=self.config_dict["button_texts"]["edit_task_button"],
            relief=tk.FLAT, 
            name="edit_button",
            command=lambda: self.open_edit_task_window(
                checkbutton_variable, task_name_label, task_deadline_label
            )
        )
        task_edit_button.pack(fill=tk.NONE, side=tk.RIGHT, padx=1)

        task_finished_checkbutton.config(
            command=lambda: self.checkbutton_function(
                checkbutton_variable, task_name_label, task_deadline_label
            )
        )

        if task_completed:
            task_name_label.config(
                font=("Arial", 15, "overstrike"), 
                fg=self.config_dict["text_color"]["secondary"]
            )
        else:
            task_name_label.config(
                font=("Arial", 15, "bold"),
                fg=self.config_dict["text_color"]["primary"]
            )

        return task_frame
    
    def checkbutton_function(
            self, 
            checkbutton_variable: tk.IntVar, 
            task_name_label: tk.Label,
            task_deadline_label: tk.Label) -> None:
        """
        Changes task name's appearance and its info in tasks list 
        according to whether the user has checked or unchecked the
        checkbutton

        Parameters
        ----------
        checkbutton_variable : tk.IntVar
            Used to determine whether a task is marked as finished or
            unfinished
        task_name_label : tk.Label
            tkinter label of task's name. Its font is changed according
            to the checkbutton_variable's value
        task_deadline_label : tk.Label
            tkinter label of task's deadline. Its content is used to
            find the task in tasks list

        Returns
        ----------
        None
        """

        if checkbutton_variable.get():
            task_name_label.config(
                font=("Arial", 15, "overstrike"), 
                fg=self.config_dict["text_color"]["secondary"]
            )
            is_task_completed: bool = False
        else:
            task_name_label.config(
                font=("Arial", 15, "bold"),
                fg=self.config_dict["text_color"]["primary"]
            )
            is_task_completed: bool = True

        removed_task_index: int = self.remove_task_from_list(
            task_name_label=task_name_label,
            task_deadline_label=task_deadline_label,
            is_task_completed=is_task_completed
        )
        
        self.insert_task_to_list(
            task_name_label=task_name_label,
            task_deadline_label=task_deadline_label,
            is_task_completed=not is_task_completed,
            index_to_insert=removed_task_index
        )
            
    def open_edit_task_window(
            self, 
            checkbutton_variable: tk.IntVar, 
            task_name_label: tk.Label, 
            task_deadline_label: tk.Label) -> None:
        """
        Opens a separate window for user to edit task name and deadline
        of an existing task

        Parameters
        ----------
        checkbutton_variable : tk.IntVar
            Used to determine whether a task is marked as finished or
            unfinished. Necessary for edit_task function called within 
            this function.
        task_name_label : tk.Label
            Used to update task in task list and its content is updated
            according to what the user has entered. Necessary for 
            edit_task function called within this function
        task_deadline_label : tk.Label
            Used to update task in task list and its content is updated
            according to what the user has entered. Necessary for 
            edit_task function called within this function

        Returns
        ----------
        None
        """

        self.task_edit_window = tk.Toplevel(
            master=self.root, bg=self.config_dict["bg_color"]["frame_bg_3"],
            name="task_edit_window"
        )
        self.task_edit_window.geometry("300x250")
        self.task_edit_window.title(
            self.config_dict["window_names"]["task_edit_window"]
        )

        task_data_frame = tk.Frame(
            master=self.task_edit_window,
            bg=self.config_dict["bg_color"]["frame_bg_3"],
            name="task_data_frame"
        )
        task_data_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        edit_task_button_frame = tk.Frame(
            master=self.task_edit_window,
            bg=self.config_dict["bg_color"]["frame_bg_3"],
            name="edit_task_button_frame"
        )
        edit_task_button_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.task_name_var = tk.StringVar(name="task_name")
        self.task_name_var.set(task_name_label.cget("text"))
        edit_task_entry = tk.Entry(
            master=task_data_frame, 
            bg=self.config_dict["bg_color"]["entry_bg"], 
            relief=tk.FLAT,
            textvariable=self.task_name_var,
            name="edit_task_entry"
        )
        edit_task_entry.pack(fill=tk.NONE, side=tk.LEFT, padx=10)

        self.edit_task_date = DateEntry(
            master=task_data_frame,
            bg=self.config_dict["bg_color"]["entry_bg"],
            name="edit_task_date"
        )
        self.edit_task_date.pack(fill=tk.NONE, side=tk.LEFT, padx=10)

        task_deadline: datetime.datetime = datetime.datetime.strptime(
            task_deadline_label.cget("text"), "%d-%m-%Y"
        )
        self.edit_task_date.set_date(task_deadline)

        edit_task_button = tk.Button(
            master=edit_task_button_frame, 
            bg=self.config_dict["bg_color"]["button_bg"], 
            relief=tk.FLAT, 
            text=self.config_dict["button_texts"]["edit_task_button"],
            command=lambda: self.edit_task(
                checkbutton_variable, task_name_label, task_deadline_label
            ),
            name="edit_task_button"
        )
        edit_task_button.pack(fill=tk.NONE, side=tk.TOP, padx=10)

        edit_task_entry.focus()

        self.task_edit_window.bind(
            sequence="<Key-Return>", 
            func=lambda x: self.edit_task(
                checkbutton_variable, task_name_label, task_deadline_label
            )
        )

    def edit_task(
            self, 
            checkbutton_variable: tk.IntVar, 
            task_name_label: tk.Label, 
            task_deadline_label: tk.Label, 
            event: Union[tk.Event, None] = None) -> None:
        """
        Edits task name and task deadline in a task frame, updates task
        in task list, closes task edit window

        Parameters
        ----------
        checkbutton_variable : tk.IntVar
            Used to determine whether a task is marked as finished or
            unfinished. This info will be used to find task in tasks
            list.
        task_name_label : tk.Label
            Used to update task in task list and its content is updated
            according to what the user has entered
        task_deadline_label : tk.Label
            Used to update task in task list and its content is updated
            according to what the user has entered
        event : tk.Event or None, default: None
            A key press event that lets a user saving tasks with a 
            keyboard shortcut. Default is None

        Returns
        ----------
        None
        """
        
        task_name = self.task_name_var.get()
        deadline: datetime.date = self.edit_task_date.get_date()

        if not self.is_user_input_valid(task_name=task_name, deadline=deadline):
            return
            
        if checkbutton_variable.get():
            is_task_completed: bool = True
        else:
            is_task_completed: bool = False

        edited_task_index: int = self.remove_task_from_list(
            task_name_label=task_name_label,
            task_deadline_label=task_deadline_label,
            is_task_completed=is_task_completed
        )

        task_name_label.config(text=task_name)
        task_deadline_label.config(text=deadline.strftime("%d-%m-%Y"))

        self.insert_task_to_list(
            task_name_label=task_name_label, 
            task_deadline_label=task_deadline_label,
            is_task_completed=is_task_completed,
            index_to_insert=edited_task_index
        )
            
        self.task_edit_window.destroy()

    def delete_task_frame(
            self,
            checkbutton_variable: tk.IntVar, 
            task_frame: tk.Frame, 
            task_name_label: tk.Label, 
            task_deadline_label: tk.Label) -> None:
        """
        Removes a task from tasks list, deletes task's frame

        Parameters
        ----------
        checkbutton_variable : tk.IntVar
            Its value is used to find task in tasks list
        task_frame : tk.Frame
            Task frame to delete
        task_name_label : tk.Label
            Its content is used to find task in tasks list
        task_deadline_label : tk.Label
            Its content is used to find task in tasks list

        Returns
        ----------
        None

        Raises
        ----------
        ValueError
            If there's no task with the entered name and deadline in 
            tasks list
        """
        
        if checkbutton_variable.get():
            is_task_completed: bool = True
        else:
            is_task_completed: bool = False

        task_entry: dict = {"task_name": task_name_label.cget("text"),
                            "deadline": task_deadline_label.cget("text"),
                            "completed": is_task_completed}
        
        try:
            self.tasks_list.remove(task_entry)
        except ValueError:
            raise ValueError(f"{task_entry} not found in self.tasks_list")
        
        task_frame.pack_forget()
        task_frame.destroy()

    def is_user_input_valid(
            self, task_name: str, deadline: datetime.date) -> bool:
        """
        Checks if user has entered a task name that is not empty or only
        whitespace, if user enters a deadline in the past asks them if
        they wish to keep the deadline

        Parameters
        ----------
        task_name : str
            User entered task name. If it is empty or only whitespace
            False is returned
        deadline : datetime.date
            User entered task deadline. If it is in the past, a warning
            message is sent to the user, asking if they wish to keep
            the deadline. If they choose "Cancel", False is returned
        
        Returns
        ----------
        result : bool
            Result of user input evaluation. If input task name is a 
            valid string and if deadline is in the future or if user is
            okay with a deadline in the past, True is returned. Else 
            False is returned
        """
        
        result: bool = True

        if not task_name or task_name.isspace():
            messagebox.showerror(
                title="No task name", message="Task name required."
            )
            
            result = False
        
        if deadline < datetime.date.today():
            user_choice = messagebox.askokcancel(
                title="Deadline in the past", 
                message="Deadline is in the past. Do you want to proceed?"
            )

            if not user_choice:
                result = False
            
        return result
    
    def remove_task_from_list(
            self, 
            task_name_label: tk.Label,
            task_deadline_label: tk.Label,
            is_task_completed: bool) -> int:
        """
        Removes a task from tasks list using task information provided 
        as parameters. Removed task's index is returned.

        Parameters
        ----------
        task_name_label : tk.Label
            tkinter label to get task name from. Used to find task in
            tasks list.
        task_deadline_label : tk.Label
            tkinter label to get task deadline from. Used to find task
            in tasks list.
        is_task_completed : bool
            Boolean variable that shows if a task is marked as finished
            or unfinished. Used to find task in tasks list.

        Returns
        ----------
        removed_task_index : int
            Used to insert a new task to the list at the removed task's 
            index

        Raises
        ----------
        ValueError
            If there's no task with the entered name and deadline in 
            tasks list
        """
        
        task_entry: dict = {"task_name": task_name_label.cget("text"),
                            "deadline": task_deadline_label.cget("text"),
                            "completed": is_task_completed}
        
        try:
            removed_task_index: int = self.tasks_list.index(task_entry)
            self.tasks_list.remove(task_entry)
        except ValueError:
            raise ValueError(f"{task_entry} not found in self.tasks_list")
        
        return removed_task_index
    
    def insert_task_to_list(
            self,
            task_name_label: tk.Label,
            task_deadline_label: tk.Label,
            is_task_completed: bool,
            index_to_insert: int) -> None:
        """
        Inserts a task to tasks list using task information and index
        provided as parameters.

        Parameters
        ----------
        task_name_label : tk.Label
            tkinter label to get task name from. Used to create new task 
            for tasks list.
        task_deadline_label : tk.Label
            tkinter label to get task deadline from. Used to create new 
            task for tasks list.
        is_task_completed : bool
            Boolean variable that shows if a task is marked as finished
            or unfinished. Used to create new task for tasks list.
        index_to_insert : int
            Used to update a task at that index.

        Returns
        ----------
        None

        Raises
        ----------
        ValueError
            If there's no task with the entered name and deadline in 
            tasks list
        """
        
        task_entry: dict = {"task_name": task_name_label.cget("text"),
                            "deadline": task_deadline_label.cget("text"),
                            "completed": is_task_completed}
        
        try:
            self.tasks_list.insert(index_to_insert, task_entry)
        except ValueError:
            raise ValueError(f"{task_entry} not found in self.tasks_list")

    def main(self) -> None:
        self.root.mainloop()
    

if __name__ == "__main__":
    application = TODO_App_GUI()

    application.main()