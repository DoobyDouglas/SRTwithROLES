from multiprocessing import freeze_support
from threading import Thread
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import asstosrt
import pysubs2
import tkinter
import sys
import os
# pyinstaller --noconfirm --onefile --noconsole --add-data 'background.png;.' --add-data 'ico.ico;.' --icon=ico.ico SRTwithROLES.py


def ass_sub_convert(subs: str) -> None:
    with open(subs, 'r', encoding='utf-8') as ass_file:
        srt_sub = asstosrt.convert(ass_file)
    srt_path = subs.replace('.ass', '.srt')
    with open(srt_path, 'w', encoding='utf-8') as srt_file:
        srt_file.write(srt_sub)


def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')

    return os.path.join(base_path, path)


def path_choice() -> str or None:
    defaultextension = 'ass'
    filetypes = [('.ass', '*.ass')]
    title = 'Выберите файл субтитров'
    path = filedialog.askopenfilename(
        defaultextension=defaultextension,
        filetypes=filetypes,
        title=title,
    )
    return path


def subs_edit() -> None:
    subs = path_choice()
    if subs:
        subtitles = pysubs2.load(subs)
        for sub in subtitles.events:
            if sub.name:
                sub.text = f'"{sub.name}": {sub.text}'
        subtitles.save(subs)
        ass_sub_convert(subs)
        os.remove(subs)


def on_start_click():
    thread = Thread(target=subs_edit)
    thread.start()


master = tkinter.Tk()
width = 300
height = 200
s_width = master.winfo_screenwidth()
s_height = master.winfo_screenheight()
upper = s_height // 8
x = (s_width - width) // 2
y = (s_height - height) // 2
master.geometry(f'{width}x{height}+{x}+{y - upper}')
master.resizable(width=False, height=False)
master.title('SRT WITH ROLES v0.03')
master.iconbitmap(default=resource_path('ico.ico'))
master.configure(background='#7ce6ef')
img = Image.open(resource_path('background.png'))
tk_img = ImageTk.PhotoImage(img)
background_label = tkinter.Label(master, image=tk_img)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
button_style = ttk.Style()
button_style.configure('TButton', background='#7ce6ef')
start_bttn = ttk.Button(
    master,
    text='START',
    name='start',
    command=lambda: on_start_click()
)
start_bttn.place(relx=0.5, rely=1.0, anchor="s", y=-9)

if __name__ == '__main__':
    freeze_support()
    master.focus_force()
    master.mainloop()
