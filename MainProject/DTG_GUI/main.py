# -------------------------------- IMPORT MODULES --------------------------------
from tkinter import *
from tkinter import filedialog as tfd
from tkinter import messagebox as tmb
from PIL import ImageTk, Image, ImageDraw, ImageFont
import os


# -------------------------------- COLORS --------------------------------
bgColor = "#237b90"
btnBgColor = "#6c0102"
hintColor = "#b3b3b3"

# -------------------------------- TKINTER SETUP --------------------------------
# Creating an instance of tkinter
root = Tk()
# Adding title
root.title("Directory Tree Generator")
# Setting icon
#root.iconbitmap("icon.ico")
# Setting default size
root.geometry("800x500")
# Setting minimum size
root.minsize(800, 500)
# Setting background
root.configure(bg=bgColor)


# -------------------------------- STRINGS --------------------------------
dir_hint = "Enter Directory"
file_hint = "Enter file name"
empty_dir_msg = "No directory has given."
empty_file_msg = "No file has given.\nPlease Enter file name to search in the given directory."
about_msg = "Directory Tree Generator to map the directory.\n\nChoose directory either by clicking on 'BROWSE DIRECTORY' button or entering the directory path.\nClick on 'RUN' button, tree will be generated for the choosen directory.\n\nYou can search a file in the choosed directoy by entering the file name then click the 'SEARCH FILE' button.\n\n\n\nCreated by farizma (GitHub @fari-zma)"


# -------------------------------- VARIABLES --------------------------------
dirPath = StringVar()
dirPath.set(dir_hint)
fileName = StringVar()
fileName.set(file_hint)


# -------------------------------- FUNCTIONS --------------------------------
def clearDirHint(event):
    if dirPath.get() == dir_hint:
        dir_entry.config(fg="black")
        dirPath.set("")

def clearFileHint(event):
    if fileName.get() == file_hint:
        file_entry.config(fg="black")
        fileName.set("")

def browseEnter(event):
    run()

def searchFileOnEnter(event):
    searchFile()

def browse():
    dir_selected = tfd.askdirectory()
    dir_entry.config(fg="black")
    dirPath.set(dir_selected.replace('/', '\\'))

def isEmpty():
    if dirPath.get() == "" or dirPath.get() == dir_hint:
        textArea.config(state="normal")
        textArea.delete("1.0", END)
        textArea.config(state="disabled")
        tmb.showerror("Directory Tree Generator", empty_dir_msg)
        return True
    else:
        return False

def run():
    if isEmpty()== False:
        textArea.config(state="normal")

        path = dirPath.get()

        textArea.delete("1.0", END)
        textArea.insert(END, path)
        
        for root, dirs, files in os.walk(path):
            root = root.replace(path, "")
            # count the seperator -> it tells the level
            level = root.count(os.sep)

            if level == 0:
                textArea.insert(END, root + "\n")
                for file in files:
                    textArea.insert(END, "  "*level + "|--" + file + "\n")

            else:
                textArea.insert(END, "|" + "--"*level)
                textArea.insert(END, root.replace('\\', '') + "\n")
                for file in files:
                    textArea.insert(END, "|" + "  "*level + "|--" + file + "\n")

            textArea.insert(END, "|\n")
    textArea.config(state="disabled")

def searchFile():
    if isEmpty()== False:
        file_name = fileName.get()
        if file_name == "" or file_name == file_hint:
            tmb.showerror("Directory Tree Generator", empty_file_msg)
        else:
            textArea.config(state="normal")
            textArea.delete("1.0", END)
            for root, dirs, files in os.walk(dirPath.get()):
                for file in files:
                    if file_name in file:
                        textArea.insert(END, os.path.join(root,file) + "\n")
            textArea.config(state="disabled")

def getWidth():
    max_ch = 0
    no_of_char = 0
    for ch in textArea.get("1.0", END):
        if ch == "\n":
            if no_of_char > max_ch:
                max_ch = no_of_char
            no_of_char = 0
        else:
            no_of_char += 1
    return max_ch*9
        

def getHeight():
    lines = 0
    for ch in textArea.get("1.0", END):
        if ch == "\n":
            lines += 1
    return lines*19

def save():
    if (textArea.get("1.0", END)) == "\n":
        tmb.showerror("Cannot save", "Nothing to save.")
        return
        
    font = ImageFont.truetype('bahnschrift.ttf', 18)

    image = Image.new('RGB', (getWidth(), getHeight()), color = 'white')
    draw = ImageDraw.Draw(image)
    draw.text((0,0), textArea.get("1.0", END), fill="black", font=font)

    filename = tfd.asksaveasfilename(initialfile="Untitled.jpg" ,defaultextension=".jpg",
    filetypes=[('JPG file','.jpg'), ('JPEG file','.jpeg'), ('all files','*.*')])
    if filename is None:
        return
    else:
        image.save(filename)
        tmb.showinfo('SAVED', 'File has been saved successfully!')

def clear():
    textArea.config(state="normal")
    textArea.delete("1.0", END)
    textArea.config(state="disabled")
    dir_entry.config(fg=hintColor)
    file_entry.config(fg=hintColor)
    dirPath.set(dir_hint)
    fileName.set(file_hint)

def about():
    tmb.showinfo("About", about_msg)

def exit():
    result = tmb.askquestion("Exit", "Are you sure you want to exit?", icon="warning")
    if result == "yes":
        root.destroy()


# -------------------------------- FRAMES --------------------------------

browse_btn = Button(root, text="BROWSE DIRECTORY", bg="#a6b401", fg="white", command=browse, padx=5)
browse_btn.pack(padx=5, pady=5)

browse_frame = Frame(root, width=600, height=50, bg=bgColor)
browse_frame.pack(padx=5, pady=5)

run_btn = Button(browse_frame, width=10, text="RUN", command=run, bg=btnBgColor, fg="white")
run_btn.pack(side=RIGHT, padx=5, pady=5)

dir_entry = Entry(browse_frame, width=200, bd=2, font="consolas 12", textvariable=dirPath, fg=hintColor)
dir_entry.pack(side=RIGHT, padx=5, pady=5)
dir_entry.bind('<Button-1>', clearDirHint)
dir_entry.bind('<Return>', browseEnter)


file_frame = Frame(root, width=600, height=50, bg=bgColor)
file_frame.pack(padx=5, pady=5)

file_btn = Button(file_frame, width=10, text="SEARCH FILE", command=searchFile, bg=btnBgColor, fg="white")
file_btn.pack(side=RIGHT, padx=5, pady=5)

file_entry = Entry(file_frame, width=200, bd=2, font="consolas 12", textvariable=fileName, fg="#b3b3b3")
file_entry.pack(side=RIGHT, padx=5, pady=5)
file_entry.bind('<Button-1>', clearFileHint)
file_entry.bind('<Return>', searchFileOnEnter)


buttons_frame = Frame(root, width=600, height=50, bg=bgColor)
buttons_frame.pack(padx=5, pady=5)

save_btn = Button(buttons_frame, width=10, text="SAVE", command=save, bg=btnBgColor, fg="white")
save_btn.pack(side=LEFT, padx=5, pady=5)

clear_btn = Button(buttons_frame, width=10, text="CLEAR", command=clear, bg=btnBgColor, fg="white")
clear_btn.pack(side=LEFT, padx=5, pady=5)

about_btn = Button(buttons_frame, width=10, text="ABOUT", command=about, bg=btnBgColor, fg="white")
about_btn.pack(side=LEFT, padx=5, pady=5)

exit_btn = Button(buttons_frame, width=10, text="EXIT", command=exit, bg=btnBgColor, fg="white")
exit_btn.pack(side=LEFT, padx=5, pady=5)


# -------------------------------- RESULT_WINDOW + SCROLLBARS --------------------------------
sby = Scrollbar(root, orient=VERTICAL)
sby.pack(side=RIGHT, fill=Y)

sbx = Scrollbar(root, orient=HORIZONTAL)
sbx.pack(side=BOTTOM, fill=X)

textArea = Text(root, wrap=NONE, state="disabled" ,yscrollcommand=sby.set, xscrollcommand=sbx.set, font="consolas 11")
textArea.pack(side=LEFT, fill=BOTH, expand=1)

sby.config(command=textArea.yview)
sbx.config(command=textArea.xview)

if __name__ == "__main__":
    root.mainloop()