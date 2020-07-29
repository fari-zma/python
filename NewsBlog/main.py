from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox  as tmb
import requests
import urllib.parse
import io

apiKey = ''
url = 'https://newsapi.org/v2/top-headlines?country=in&category=technology&pageSize=10&apiKey=' + apiKey

r = requests.get(url).json()

# create instance
window = Tk()
# set default window size
window.geometry('900x550')
# set min window size
window.minsize(700, 400)
# set max window size
window.maxsize(1100, 600)
# add a title
window.title("News Blog")

def subscribeUser():
    with open('NewsBlogSubscribers.txt', 'a') as f:
        f.write(f"{userName.get(), userEmail.get(), userPhone.get()}\n")


def rateUs():
    a = tmb.askokcancel("Rate", "Would you like to rate us now?")
    if a==True:
        tmb.showinfo("Rated", "Thank you for taking your time to rate us.")
    else:
        tmb.showinfo("Not Rated", "We are looking forward to serve in much better way.\nThank You!")

def help():
    tmb.showinfo("Help","We are glad that you asked for help.\nWe will soon resolve your issue. Kindly wait for some time.\nThank You")

def error():
    tmb.showerror("Error", "This is an error message.")\

def submit():
    #tmb.showinfo("Slider", f"You've selected {myslider.get()} on slider.")
    tmb._show(title='Slider', message=f"You've selected {myslider.get()} on slider.", icon='info')


def getFormattedText(text):
    count = 1
    formattedText = ''
    for ch in text:
        if(count%80 == 0):
            formattedText += '\n'
        formattedText += ch
        count += 1
    return formattedText

frames = []
photos = []

def populate():
    #for i in range(len(r['articles'])):
    for i in range(2):
        frame = Frame(window, borderwidth=4, relief=RIDGE)
        frame.pack(fill=Y, pady=10, padx=10)

        print(r['articles'][i]['urlToImage'])
        raw_data = urllib.request.urlopen(r['articles'][i]['urlToImage']).read()
        image = Image.open(io.BytesIO(raw_data))
        image = image.resize((100, 100), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        photos.append(photo)

        image_label = Label(
                        master=frame,
                        image=photo,
                    )
        image_label.pack(side=LEFT, padx=2, pady=2)

        text_frame = Frame(frame)
        text_frame.pack(side=RIGHT)

        title = Label(text_frame, fg='red',
                    text = getFormattedText(r['articles'][i]['title']),
                    font=("comicsans", 12, "bold"),
                )
        title.pack(padx=5, pady=5)

        desc = Label(text_frame, text = getFormattedText(r['articles'][i]['description']))
        #desc = Label(text_frame, text = r['articles'][i]['content'])
        desc.pack(pady=10)

        date = Label(text_frame, text=r['articles'][i]['publishedAt'])
        date.pack(side=RIGHT, padx=2)

        frames.append(frame)
        frames[i].pack()


# --------------------- Menu Bar ---------------------
myMenuBar = Menu(window)

m1 = Menu(myMenuBar, tearoff=0)
m1.add_command(label='Rate Us', command=rateUs)
m1.add_command(label='Help', command=help)
m1.add_command(label='Error', command=error)

myMenuBar.add_cascade(label='Options', menu=m1)
myMenuBar.add_command(label='Exit', command=quit)
window.config(menu=myMenuBar)


# --------------------- Slider with Button ---------------------
slider_frame = Frame(window)
slider_frame.pack()
#Creating Slider/Scroll Bar
myslider = Scale(slider_frame, from_ = 0, to = 10, tickinterval=2, orient = HORIZONTAL)
myslider.pack(side=LEFT)

#To change the By-Default Value from 0 to 10
myslider.set(1)
Button(slider_frame, text='Submit', command=submit).pack(side=RIGHT)


# --------------------- Add news item to the window ---------------------
populate()


# --------------------- Subscription Form ---------------------
Label(window, text='Subscribe to our blog', font=("comicsans", 15, "bold")).pack()

form_frame = Frame(window)
form_frame.pack(side=LEFT)

userName = StringVar()
userEmail = StringVar()
userPhone = StringVar()

Label(form_frame, text='Name: ', padx=3, pady=3).grid(row=1, column=1)
Label(form_frame, text='Email: ', padx=3, pady=3).grid(row=2, column=1)
Label(form_frame, text='Phone: ', padx=3, pady=3).grid(row=3, column=1)

Entry(form_frame, textvariable=userName).grid(row=1, column=2)
Entry(form_frame, textvariable=userEmail).grid(row=2, column=2)
Entry(form_frame, textvariable=userPhone).grid(row=3, column=2)

Button(form_frame, text='Subscribe', command=subscribeUser).grid(row=4, column=1, padx=10, pady=10)

window.mainloop()