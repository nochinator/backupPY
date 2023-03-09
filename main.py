import shutil
import datetime
import os
import sys
import threading
import time
from tkinter import *
from tkinter import filedialog
import logging
from plyer import notification
import win32com.client

# makes the path work automagicaly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

script_dir = os.path.dirname(os.path.abspath(__file__))
locations = os.path.join(script_dir, "locations.txt")


def add_to_startup():
    # get the startup folder location
    startup_folder = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu",
                                  "Programs", "Startup")
    # create shortcut file name
    app_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    shortcut_name = app_name + ".lnk"
    # create shortcut file path
    shortcut_path = os.path.join(startup_folder, shortcut_name)
    # check if the shortcut file exists in the startup folder
    if not os.path.exists(shortcut_path):
        try:
            # create a new shortcut file
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = os.path.abspath(sys.argv[0])  # use the full path to the EXE file
            shortcut.Arguments = ""  # no command line arguments
            shortcut.WorkingDirectory = os.getcwd()  # use the current working directory
            shortcut.Description = app_name
            shortcut.Save()
            print(f"Added {app_name} to startup folder")
        except Exception as e:
            print(f"Error adding {app_name} to startup folder: {e}")
    else:
        print(f"{app_name} is already in startup folder")


if __name__ == "__main__":
    add_to_startup()


def save():
    global fin_dir, new_entry
    with open(locations, 'w') as f:
        f.write(v.get())
        f.write('\n' + fin_dir.get())  # save the data on the second line
        for button in remove_buttons:
            row = button.grid_info()["row"]
            entry = locations_frame_inner.grid_slaves(row=row, column=0)[0]
            entry_text = entry.get()
            f.write('\n' + entry_text)


def backup():
    with open("log.log", 'w') as f:
        f.write('')
    handler = logging.FileHandler('log.log')
    logger = logging.getLogger()
    logger.addHandler(handler)

    errors = False
    today = datetime.date.today()

    # get save data
    with open(locations) as f:
        try:
            next(f).strip()
            destination_dir = next(f).strip()
            source_dirs = [line.strip() for line in f]
        except:
            pass

    # create folder and name, adds number to end if folder already exists
    backup_folder = os.path.join(destination_dir, today.strftime('%Y-%m-%d'))
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    else:
        index = 1
        while True:
            backup_folder = f"{backup_folder} ({index})"
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
                break
            index += 1

    # Backup each source directory
    for i, source_dir in enumerate(source_dirs, 1):
        logger.info(f"Backing up {source_dir} ({i}/{len(source_dirs)})...")

        # check if directory is valid
        if not os.path.isdir(source_dir):
            errors = True
            logger.exception(f"backup of {source_dir} failed because is not a valid directory")

        else:
            # try to perform backup
            try:
                shutil.copytree(source_dir, os.path.join(backup_folder, os.path.basename(source_dir)))
                logger.info(f"Backup of {source_dir} complete.")

            except Exception as e:
                errors = True
                logger.exception(f"backup of {source_dir} failed with error: {str(e)}")

    # Create a ZIP archive of the backup folder
    logger.info("zipping")
    shutil.make_archive(os.path.join(destination_dir, today.strftime('%Y-%m-%d')), "zip", backup_folder)

    # display a notification if the backup had errors
    if not errors:
        logger.info(
            f"Backup created at {backup_folder} and compressed to {os.path.join(destination_dir, today.strftime('%Y-%m-%d'))}.zip")
        os.remove("log.log")
    else:
        logger.info("there were errors in the backup")
        notification.notify(
            title="The most recent backup had errors",
            message="The most recent backup had errors, please see the file log.log and create a gitHub bug report with"
                    " the file.",
            app_name='backupPY',
            timeout=10)
    backup_button.configure(state="normal")


# Define the source and destination directories
if not os.path.exists(locations):
    open(locations, 'w').close()

# run if launched by windows startup
if len(sys.argv) > 1 and sys.argv[1] == '--startup':
    # loop to run
    while True:
        # Define the source and destination directories
        if not os.path.exists(locations):
            open(locations, 'w').close()

        with open(locations) as f:
            backup_interval = float(next(f).strip())
            destination_dir = next(f).strip()

        # Get the current date
        today = datetime.date.today()

        # Calculate the date of the last backup
        last_backup = today - datetime.timedelta(days=backup_interval)

        # Check if a backup is needed
        if not os.path.exists(os.path.join(destination_dir, last_backup.strftime('%Y-%m-%d'))):
            # Create a new backup folder with the current date
            backup()

        else:
            # Wait for some time before checking again
            time.sleep(1800)  # 30 minutes in seconds


# show GUI if launched by user
else:
    root = Tk()

    # set some configs
    icon = os.path.join(script_dir, 'backupPY.ico')
    root.iconbitmap(icon)
    root.title('backupPY')
    root.configure(bg='#2B2B2B')

    # configure columns
    root.columnconfigure(0, minsize=0)
    root.columnconfigure(1, minsize=115)
    root.columnconfigure(2, minsize=115)
    root.columnconfigure(3, minsize=115)
    for i in range(7):
        root.rowconfigure(i + 1, weight=2)


    # set color when buttons are pressed
    def on_press():
        buttons.configure(background='#362222')


    # set size
    root.geometry("530x300")
    root.resizable(False, True)

    # set labe for radio buttons
    Label(root, text="day to backup on", bg="#2B2B2B", fg="#c7c0c0").grid(row=0, column=0, pady=5)

    # radio button dictionary
    v = StringVar(root, "1")
    values = {
        "Monday": "1",
        "Tuesday": "2",
        "Wednesday": "3",
        "Thursday": "4",
        "Friday": "5",
        "Saturday": "6",
        "Sunday": "7"
    }

    # create radio buttons
    for (text, value) in values.items():
        buttons = Radiobutton(root, text=text, variable=v, value=value, indicator=0, bg="#362222", fg="#c7c0c0",
                              selectcolor="#171010", activebackground="#171010")
        buttons.grid(row=int(value), column=0, sticky="NSEW", padx=5, pady=1)
        buttons.bind('<Button-1>', lambda event: on_press())

    # frame with title for locations to backup
    locations_frame = LabelFrame(root, text="Locations to Backup", bg="#2B2B2B", fg="#c7c0c0")
    locations_frame.grid(row=1, column=1, rowspan=8, columnspan=3, sticky="NSEW", padx=5)

    # canvas to make actual box look
    locations_canvas = Canvas(locations_frame, bg="#2B2B2B")
    locations_canvas.pack(side=LEFT, fill=BOTH, expand=True)

    # frame containing locations text boxes
    locations_frame_inner = Frame(locations_canvas, bg="#2B2B2B")
    locations_canvas.create_window((0, 0), window=locations_frame_inner, anchor="nw")

    # scrollbar
    locations_scroll = Scrollbar(locations_frame, orient=VERTICAL, command=locations_canvas.yview)
    locations_scroll.pack(side=RIGHT, fill=Y)

    # coloring for canvas
    locations_canvas.config(yscrollcommand=locations_scroll.set, highlightbackground='#2B2B2B',
                            highlightcolor='#2B2B2B')
    # make scroll bar not finicky
    locations_scroll.bind_all("<MouseWheel>",
                              lambda event: locations_canvas.yview_scroll(-1 * (event.delta // 120), "units"))

    # list for manageing rows
    remove_buttons = []


    # add textbox for locations
    def add_textbox(dir=None):
        # text box
        new_entry = Entry(locations_frame_inner, width=50, bg="#423F3E", fg="#c7c0c0")
        new_entry.grid(row=len(remove_buttons), column=0, sticky="W")

        # the "X" button
        remove_button = Button(locations_frame_inner, text="X", bg="#423F3E", fg="#c7c0c0", activebackground="#171010",
                               command=lambda: remove_textbox(new_entry, remove_button, browse_button))
        remove_button.grid(row=len(remove_buttons), column=1, padx=5, pady=5, sticky="E")
        remove_buttons.append(remove_button)

        # the "Browse" button
        browse_button = Button(locations_frame_inner, text="Browse", bg="#423F3E", fg="#c7c0c0",
                               activebackground="#171010",
                               command=lambda: browse_directory(new_entry))
        browse_button.grid(row=len(remove_buttons) - 1, column=2, padx=0, pady=5, sticky="E")

        # update canvas
        locations_canvas.update_idletasks()
        # update scrollbar
        locations_canvas.config(scrollregion=locations_canvas.bbox("all"))

        # prefill boxes if there is save data
        if dir is not None:
            new_entry.insert(0, dir)


    # code for the browse button functionality
    def browse_directory(entry):
        directory = filedialog.askdirectory()
        if directory:
            entry.delete(0, END)
            entry.insert(0, directory)


    # code to remove a text box row
    def remove_textbox(entry, button, browse):
        global remove_buttons
        i = remove_buttons.index(button)
        remove_buttons = remove_buttons[:i] + remove_buttons[i + 1:]
        entry.destroy()
        button.destroy()
        browse.destroy()

    # code to trigger a backup on backup button press
    def backup_now():
        backup_thread = threading.Thread(target=backup())
        backup_thread.start()
        backup_button.configure(state="disabled")


    # standard buttons in GUI
    # new location button button
    new_location_button = Button(root, text="New Location", command=add_textbox, bg="#423F3E", fg="#c7c0c0",
                                 activebackground="#171010")
    new_location_button.grid(row=0, column=1, sticky="W", padx=7, pady=5)

    # backup now button
    backup_button = Button(root, text='backup now', command=backup_now, bg="#423F3E", fg="#c7c0c0",
                           activebackground="#171010")
    backup_button.grid(row=0, column=3, sticky="E", padx=7, pady=5)

    # save button
    save_button = Button(root, text='Save', command=save, bg="#423F3E", fg="#c7c0c0", activebackground="#171010")
    save_button.grid(row=9, column=3, sticky="E", padx=7, pady=5)

    # the location to backup data
    # label saying what the textbox is
    fin_dir_label = Label(root, text="location to backup to", bg="#2B2B2B", fg="#c7c0c0")
    fin_dir_label.grid(row=8, column=0)

    # text box for location to backup to
    fin_dir = Entry(root, bg="#423F3E", fg="#c7c0c0")
    fin_dir.grid(row=9, column=0, columnspan=3, sticky="WE", padx=5, pady=5)

    # browse button for backup location
    fin_dir_browse_button = Button(root, text="Browse", bg="#423F3E", fg="#c7c0c0", activebackground="#171010",
                                   command=lambda: browse_directory(fin_dir))
    fin_dir_browse_button.grid(row=9, column=3, padx=4, pady=5, sticky="W")

    # clear button
    # this is a filler button and will be replaced with the option to backup the data to multiple different locations
    clear_fin_dir_button = Button(root, text="Clear", command=lambda: fin_dir.delete(0, END), bg="#423F3E",
                                  fg="#c7c0c0", activebackground="#171010")
    clear_fin_dir_button.grid(row=9, column=3, padx=55, pady=5, sticky="E")

    # fill in data from save file
    with open(locations, "r") as f:
        try:
            lines = f.readlines()
            value = lines[0].strip()
            dir_fin = lines[1].strip()
            for lines in lines[2:]:
                add_textbox(lines.strip())
            v.set(value)
            fin_dir.insert(0, dir_fin)
        except IndexError:
            pass

    root.mainloop()
