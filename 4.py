# import required modules
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename,asksaveasfilename
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os
# contrast border thumbnail 
root = Tk()
root.title("demo 3.6")
root.geometry("640x640")

def blur(event):
    global img_path, img1, imgg
    for m in range(0, v1.get()+1):
            img = Image.open(img_path)
            img.thumbnail((350, 350))
            imgg = img.filter(ImageFilter.BoxBlur(m))
            img1 = ImageTk.PhotoImage(imgg) 
            canvas2.create_image(300, 210, image=img1)
            canvas2.image=img1

def brightness(event):
    global img_path, img2, img3
    for m in range(0, v2.get()+1):
            img = Image.open(img_path)
            img.thumbnail((350, 350))
            imgg = ImageEnhance.Brightness(img)
            img2 = imgg.enhance(m)
            img3 = ImageTk.PhotoImage(img2)
            canvas2.create_image(300, 210, image=img3)
            canvas2.image=img3

def contrast(event):
    global img_path, img4, img5
    for m in range(0, v3.get()+1):
            img = Image.open(img_path)
            img.thumbnail((350, 350))
            imgg = ImageEnhance.Contrast(img)
            img4 = imgg.enhance(m)
            img5 = ImageTk.PhotoImage(img4)
            canvas2.create_image(300, 210, image=img5)
            canvas2.image=img5

def rotate_image(event):
        global img_path, img6, img7
        img = Image.open(img_path)
        img.thumbnail((350, 350))
        img6 = img.rotate(int(rotate_combo.get()))
        img7 = ImageTk.PhotoImage(img6)
        canvas2.create_image(300, 210, image=img7)
        canvas2.image=img7
        
def flip_image(event):
        global img_path, img8, img9
        img = Image.open(img_path)
        img.thumbnail((350, 350))
        if flip_combo.get() == "LEFT TO RIGHT":
            img8 = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        elif flip_combo.get() == "TOP TO BOTTOM":
            img8 = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        else:
            img8=img
        img9 = ImageTk.PhotoImage(img8)
        canvas2.create_image(300, 210, image=img9)
        canvas2.image=img9   

def image_border(event):
    global img_path, img10, img11
    img = Image.open(img_path)
    img.thumbnail((350, 350))
    if border_combo.get() == "0":
        img11=img
    else:
        img10 = ImageOps.expand(img, border=int(border_combo.get()), fill=95)
        img11 = ImageTk.PhotoImage(img10)
        canvas2.create_image(300, 210, image=img11)
    canvas2.image=img11    
    
rotate = Label(root, text="Rotate:", font=("ariel 17 bold"))
rotate.place(x=60, y=3)
values = [0, 90, 180, 270]
rotate_combo = ttk.Combobox(root, values=values, font=('ariel 10 bold'),state="readonly")
rotate_combo.current(0)
rotate_combo.place(x=150, y=10)
rotate_combo.bind("<<ComboboxSelected>>", rotate_image)
flip = Label(root, text="Flip:", font=("ariel 17 bold"))
flip.place(x=90, y=47)
values1 = ["NORMAL","LEFT TO RIGHT", "TOP TO BOTTOM"]
flip_combo = ttk.Combobox(root, values=values1, font=('ariel 10 bold'),state= "readonly")
flip_combo.current(0)
flip_combo.place(x=150, y=55)
flip_combo.bind("<<ComboboxSelected>>", flip_image)
border = Label(root, text="Add border:", font=("ariel 17 bold"))
border.place(x=10, y=92)
values2 = [i for i in range(0, 45, 5)]
border_combo = ttk.Combobox(root, values=values2, font=("ariel 10 bold"),state= "readonly")
border_combo.current(0)
border_combo.place(x=150, y=100)
border_combo.bind("<<ComboboxSelected>>", image_border)

# Display image
canvas2 = Canvas(root, width="600", height="420", relief=RIDGE, bd=2)
canvas2.place(x=15, y=150)

blurr = Label(root, text="Blur:", font=("ariel 17 bold"), width=9, anchor='e')
blurr.place(x=320, y=8)
v1 = IntVar()
scale1 = ttk.Scale(root, from_=0, to=10, variable=v1, orient=HORIZONTAL, command=blur) 
scale1.place(x=460, y=15)
bright = Label(root, text="Brightness:", font=("ariel 17 bold"))
bright.place(x=315, y=50)
v2 = IntVar()   
scale2 = ttk.Scale(root, from_=0, to=10, variable=v2, orient=HORIZONTAL, command=brightness) 
scale2.place(x=460, y=55)
cont = Label(root, text="Contrast:", font=("ariel 17 bold"))
cont.place(x=340, y=92)
v3 = IntVar()   
scale3 = ttk.Scale(root, from_=0, to=10, variable=v3, orient=HORIZONTAL, command=contrast) 
scale3.place(x=460, y=100)


img_path = "./image/girl.jpg"
img = Image.open(img_path)
img.thumbnail((350, 350))
img1 = ImageTk.PhotoImage(img)
canvas2.create_image(300, 210, image=img1)
canvas2.image=img1 
root.mainloop()