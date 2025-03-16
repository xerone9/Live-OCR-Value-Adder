from tkinter import *
from pytesseract import pytesseract
import re
import pyautogui
import os
import tempfile
import shutil
import logging
from PIL import Image, ImageTk

logging.basicConfig(filename="logs.txt", level=logging.INFO, format='%(asctime)s: %(message)s')


# Close App
def kill_me(event):
    root.destroy()
    shutil.rmtree(dirpath)


# get cordinates from where you start drawing rectangle
def get_x_and_y(event):
    global startx, starty
    startx, starty = event.x, event.y


# Draw rectangle by mouse movement
def draw_rectangle(event):
    try:
        global startx, starty
        # Global my_rectangle because it will continously delete the old rectangle with new rectangle eitherwise so many rectangles
        # will be made
        global my_rectangle
        canvas.delete(my_rectangle)
        my_rectangle = canvas.create_rectangle(startx, starty, event.x, event.y,
                                outline="#f11", width=2)

        # Crop portion of an image which is needed to be processed
        img = Image.open("range_add.png")
        x1 = startx
        y1 = starty
        x2 = event.x
        y2 = event.y
        if startx > event.x:
            x1 = event.x
            x2 = startx
        if starty > event.y:
            y1 = event.y
            y2 = starty
        area = (x1, y1, x2, y2)
        global dirpath
        dirpath = tempfile.mkdtemp()
        img.crop(area).save(dirpath + "\\croped_portion.png")

        # cropped portion sent to OCR for analysis
        filename = dirpath + '\\croped_portion.png'
        program_files_location = os.environ["ProgramFiles"]
        path_to_tesseract = program_files_location + "/Tesseract-OCR/tesseract.exe"
        pytesseract.tesseract_cmd = path_to_tesseract

        # Passing the image object to image_to_string() function
        # This function will extract the text from the image
        text = pytesseract.image_to_string(filename)

        # Removing additional line space and other values besides numbers and then adding number
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


        # displaing total value calculated right below the rectangle and if it matches the screen height it will go above
        # the rectangle and same mechanics for right side
        cords.place(x=startx, y=event.y + 10)
        if event.y > root.winfo_screenheight() - 60:
            cords.place(x=startx, y=starty - 60)
        if event.x > root.winfo_screenwidth() - 60:
            cords.place(x=startx - 180, y=event.y + 10)
        cords.config(text=str("{:,.2f}".format(amount)))
        close_caption.config(text="")
    except Exception as e:
        logging.info(str(e))



def crop_stuff(event):
    pass
    # for future upgrades (What to do when mouse click is released)


# tkinter window
root = Tk()
root.config(cursor="plus")
root.wm_attributes('-fullscreen','true')
root.wm_attributes('-transparentcolor','pink') #if the bacground color of tkinter widget is pink it will behave as transparent

canvas = Canvas(root, bg='black')

# rectangle with no dimensions will get dimensions from mouse movement
global my_rectangle
my_rectangle = canvas.create_rectangle(0, 0, 0, 0,)
canvas.pack(anchor='nw', fill='both', expand=1)

# where total values will be seen
cords = Label(root, text="", font=("Comic Sans MS", 25, 'bold'))
cords.configure(fg="black", bg="pink")
cords.place(x=5, y=5)

# As tkinter top bar is disabled so we need to tell how to exit
close_caption = Label(root, text="Press F5 To Close", font=("Comic Sans MS", 25, 'bold'))
close_caption.configure(fg="green", bg="black")
close_caption.place(x=root.winfo_screenwidth() / 2, y=root.winfo_screenheight() / 2)

canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_rectangle)
canvas.bind("<ButtonRelease-1>", crop_stuff) # for future upgrades
root.bind("<F5>", kill_me)

# taking screenshot and setting it into the background of Tkinter window
myScreenshot = pyautogui.screenshot()
myScreenshot.save('range_add.png')

image = Image.open("range_add.png")
image = ImageTk.PhotoImage(image)
canvas.create_image(0,0, image=image, anchor="nw")

root.mainloop()