from tkinter import *
from pytesseract import pytesseract
import re
import pyautogui
import logging
from PIL import Image, ImageTk

logging.basicConfig(filename="logs.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

def kill_me(event):
    root.destroy()


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_smth(event):
    global lasx, lasy
    # canvas.create_line((lasx, lasy, event.x, event.y),
    #                   fill='red',
    #                   width=2)
    global blue
    canvas.delete(blue)
    blue = canvas.create_rectangle(lasx, lasy, event.x, event.y,
                            outline="#f11", width=2)


    img = Image.open("range_add.png")
    x1 = lasx
    y1 = lasy
    x2 = event.x
    y2 = event.y
    if lasx > event.x:
        x1 = event.x
        x2 = lasx
    if lasy > event.y:
        y1 = event.y
        y2 = lasy
    area = (x1, y1, x2, y2)
    img.crop(area).save("haider.png")

    filename = 'haider.png'
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    pytesseract.tesseract_cmd = path_to_tesseract

    # Passing the image object to image_to_string() function
    # This function will extract the text from the image
    text = pytesseract.image_to_string(filename)

    # Displaying the extracted text
    translated = str(text[:-1]).split("\n")
    amount = 0

    for i in translated:
        value = i.replace(",", "")
        x = [float(x) for x in re.findall(r'-?\d+\.?\d*', value)]
        total_x = sum(x)
        try:
            amount += float(total_x)
        except ValueError:
            pass


    cords.place(x=lasx, y=event.y + 10)
    if event.y > root.winfo_screenheight() - 60:
        cords.place(x=lasx, y=lasy - 60)
    if event.x > root.winfo_screenwidth() - 60:
        cords.place(x=lasx - 180, y=event.y + 10)
    cords.config(text=str("{:,.2f}".format(amount)))
    close_caption.config(text="")


def crop_stuff(event):
    pass


root = Tk()
root.config(cursor="plus")
root.wm_attributes('-fullscreen','true')
root.wm_attributes('-transparentcolor','pink')

canvas = Canvas(root, bg='black')

global blue
blue = canvas.create_rectangle(0, 0, 0, 0,)
canvas.pack(anchor='nw', fill='both', expand=1)

cords = Label(root, text="", font=("Comic Sans MS", 25, 'bold'))
cords.configure(fg="black", bg="pink")
cords.place(x=5, y=5)

close_caption = Label(root, text="Press F5 To Close", font=("Comic Sans MS", 25, 'bold'))
close_caption.configure(fg="green", bg="black")
close_caption.place(x=root.winfo_screenwidth() / 2, y=root.winfo_screenheight() / 2)

canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_smth)
canvas.bind("<ButtonRelease-1>", crop_stuff)
root.bind("<F5>", kill_me)

myScreenshot = pyautogui.screenshot()
myScreenshot.save('range_add.png')

image = Image.open("range_add.png")
image = ImageTk.PhotoImage(image)
canvas.create_image(0,0, image=image, anchor="nw")

root.mainloop()