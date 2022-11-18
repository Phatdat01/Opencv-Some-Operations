from tkinter import *
import os
import PIL.Image
import ctypes
from PIL import ImageTk
from PIL import ImageOps
from tkinter.filedialog import *
import tkinter.messagebox
import imghdr
from PIL import ImageDraw
from collections import*

def drawOnImage(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=True
    drawWindow=Toplevel(canvas.data.mainWindow)
    drawWindow.title="Draw"
    drawFrame=Frame(drawWindow)
    redButton=Button(drawFrame, bg="red", width=2, \
                     command=lambda: colourChosen(drawWindow,canvas, "red"))
    redButton.grid(row=0,column=0)
    blueButton=Button(drawFrame, bg="blue", width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "blue"))
    blueButton.grid(row=0,column=1)
    greenButton=Button(drawFrame, bg="green",width=2, \
                       command=lambda: colourChosen(drawWindow,canvas, "green"))
    greenButton.grid(row=0,column=2)
    magentaButton=Button(drawFrame, bg="magenta", width=2,\
                         command=lambda: colourChosen(drawWindow,canvas, "magenta"))
    magentaButton.grid(row=1,column=0)
    cyanButton=Button(drawFrame, bg="cyan", width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "cyan"))
    cyanButton.grid(row=1,column=1)
    yellowButton=Button(drawFrame, bg="yellow",width=2,\
                        command=lambda: colourChosen(drawWindow,canvas, "yellow"))
    yellowButton.grid(row=1,column=2)
    orangeButton=Button(drawFrame, bg="orange", width=2,\
                        command=lambda: colourChosen(drawWindow,canvas, "orange"))
    orangeButton.grid(row=2,column=0)
    purpleButton=Button(drawFrame, bg="purple",width=2, \
                        command=lambda: colourChosen(drawWindow,canvas, "purple"))
    purpleButton.grid(row=2,column=1)
    brownButton=Button(drawFrame, bg="brown",width=2,\
                       command=lambda: colourChosen(drawWindow,canvas, "brown"))
    brownButton.grid(row=2,column=2)
    blackButton=Button(drawFrame, bg="black",width=2,\
                       command=lambda: colourChosen(drawWindow,canvas, "black"))
    blackButton.grid(row=3,column=0)
    whiteButton=Button(drawFrame, bg="white",width=2, \
                       command=lambda: colourChosen(drawWindow,canvas, "white"))
    whiteButton.grid(row=3,column=1)
    grayButton=Button(drawFrame, bg="gray",width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "gray"))
    grayButton.grid(row=3,column=2)
    drawFrame.pack(side=BOTTOM)


def colourChosen(drawWindow, canvas, colour):
    if canvas.data.image!=None:
        canvas.data.drawColour=colour
        canvas.data.mainWindow.bind("<B1-Motion>",\
                                    lambda event: drawDraw(event, canvas))
    drawWindow.destroy()
    

def drawDraw(event, canvas):
    if canvas.data.drawOn==True:
        x=int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
        y=int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
        draw = ImageDraw.Draw(canvas.data.image)
        draw.ellipse((x-3, y-3, x+ 3, y+3), fill=canvas.data.drawColour,\
                     outline=None)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def closeHistWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.histWindowClose=True

def histogram(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    histWindow=Toplevel(canvas.data.mainWindow)
    histWindow.title("Histogram")
    canvas.data.histCanvasWidth=350
    canvas.data.histCanvasHeight=475
    histCanvas = Canvas(histWindow, width=canvas.data.histCanvasWidth, \
                        height=canvas.data.histCanvasHeight)
    histCanvas.pack()
    # provide sliders to the user to manipulate red, green and blue amounts in the image
    redSlider=Scale(histWindow, from_=-100, to=100, \
                    orient=HORIZONTAL, label="R")
    redSlider.pack()
    blueSlider=Scale(histWindow, from_=-100, to=100,\
                     orient=HORIZONTAL, label="B")
    blueSlider.pack()
    greenSlider=Scale(histWindow, from_=-100, to=100,\
                      orient=HORIZONTAL, label="G")
    greenSlider.pack()
    OkHistFrame=Frame(histWindow)
    OkHistButton=Button(OkHistFrame, text="OK", \
                        command=lambda: closeHistWindow(canvas))
    OkHistButton.grid(row=0,column=0)
    OkHistFrame.pack(side=BOTTOM)
    initialRGB=(0,0,0)
    changeColours(canvas, redSlider, blueSlider, \
                  greenSlider, histWindow, histCanvas, initialRGB)


def changeColours(canvas, redSlider, blueSlider, \
                  greenSlider, histWindow, histCanvas, previousRGB):
    if canvas.data.histWindowClose==True:
        histWindow.destroy()
        canvas.data.histWindowClose=False
    else:
        # the slider value indicates the % by which the red/green/blue
        # value of the pixels of the image need to incresed (for +ve values)
        # or decreased (for -ve values)
        if canvas.data.image!=None and histWindow.winfo_exists() :
            R, G, B= canvas.data.image.split()
            sliderValR=redSlider.get()
            (previousR, previousG, previousB)= previousRGB
            scaleR=(sliderValR-previousR)/100.0
            R=R.point(lambda i: i+ int(round(i*scaleR)))
            sliderValG=greenSlider.get()
            scaleG=(sliderValG-previousG)/100.0
            G=G.point(lambda i: i+ int(round(i*scaleG)))
            sliderValB=blueSlider.get()
            scaleB=(sliderValB-previousB)/100.0
            B=B.point(lambda i: i+ int(round(i*scaleB)))
            canvas.data.image = PIL.Image.merge(canvas.data.image.mode, (R, G, B))
            
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            displayHistogram(canvas, histWindow, histCanvas)
            previousRGB=(sliderValR, sliderValG, sliderValB)
            canvas.after(200, lambda: changeColours(canvas, redSlider,\
                blueSlider, greenSlider,  histWindow, histCanvas, previousRGB))

def displayHistogram(canvas,histWindow, histCanvas):
    histCanvasWidth=canvas.data.histCanvasWidth
    histCanvasHeight=canvas.data.histCanvasHeight
    margin=50
    if canvas.data.image!=None:
        histCanvas.delete(ALL)
        im=canvas.data.image
        #x-axis 
        histCanvas.create_line(margin-1, histCanvasHeight-margin+1,\
                               margin-1+ 258, histCanvasHeight-margin+1)
        xmarkerStart=margin-1
        for i in range(0,257,64):
            xmarker="%d" % (i)
            histCanvas.create_text(xmarkerStart+i,\
                                   histCanvasHeight-margin+7, text=xmarker)
        #y-axis
        histCanvas.create_line(margin-1, \
                               histCanvasHeight-margin+1, margin-1, margin)
        ymarkerStart= histCanvasHeight-margin+1
        for i in range(0, histCanvasHeight-2*margin+1, 50):
            ymarker="%d" % (i)
            histCanvas.create_text(margin-1-10,\
                                   ymarkerStart-i, text=ymarker)
            
        R, G, B=im.histogram()[:256], im.histogram()[256:512], \
                 im.histogram()[512:768]
        for i in range(len(R)):
            pixelNo=R[i]
            histCanvas.create_oval(i+margin, \
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin, \
                                   fill="red", outline="red")
        for i in range(len(G)):
            pixelNo=G[i]
            histCanvas.create_oval(i+margin, \
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin, \
                                   fill="green", outline="green")
        for i in range(len(B)):
            pixelNo=B[i]
            histCanvas.create_oval(i+margin,\
                            histCanvasHeight-pixelNo/100.0-1-margin, i+2+margin,\
                            histCanvasHeight-pixelNo/100.0+1-margin,\
                                   fill="blue", outline="blue")

def colourPop(canvas):
    canvas.data.cropPopToHappen=False
    canvas.data.colourPopToHappen=True
    canvas.data.drawOn=False
    tkinter.messagebox.showinfo(title="Colour Pop", message="Click on a part of the image which you want in colour" , parent=canvas.data.mainWindow)
    if canvas.data.cropPopToHappen==False:
        canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: getPixel(event, canvas))


def getPixel(event, canvas):

    try: 
        if canvas.data.colourPopToHappen==True and \
           canvas.data.cropPopToHappen==False and canvas.data.image!=None :
            data=[]
            canvas.data.pixelx=\
            int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
            canvas.data.pixely=\
            int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
            pixelr, pixelg, pixelb= \
            canvas.data.image.getpixel((canvas.data.pixelx, canvas.data.pixely))
            tolerance=60 
            for y in range(canvas.data.image.size[1]):
                for x in range(canvas.data.image.size[0]):
                    r, g, b= canvas.data.image.getpixel((x, y))
                    avg= int(round((r + g + b)/3.0))
                    if (abs(r-pixelr)>tolerance or
                        abs(g-pixelg)>tolerance or
                        abs(b-pixelb)>tolerance ):
                        R, G, B= avg, avg, avg
                    else:
                        R, G, B=r,g,b
                    data.append((R, G, B))
            canvas.data.image.putdata(data)
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
    except:
        pass
    canvas.data.colourPopToHappen=False
  
def rotateFinished(canvas, rotateWindow, rotateSlider, previousAngle):
    if canvas.data.rotateWindowClose==True:
        rotateWindow.destroy()
        canvas.data.rotateWindowClose=False
    else:
        if canvas.data.image!=None and rotateWindow.winfo_exists():
            canvas.data.angleSelected=rotateSlider.get()
            if canvas.data.angleSelected!= None and \
               canvas.data.angleSelected!= previousAngle:
                canvas.data.image=\
                canvas.data.image.rotate(float(canvas.data.angleSelected))
                canvas.data.imageForTk=makeImageForTk(canvas)
                drawImage(canvas)
        canvas.after(200, lambda:rotateFinished(canvas,\
                    rotateWindow, rotateSlider, canvas.data.angleSelected) )


def closeRotateWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.rotateWindowClose=True
    
def rotate(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    rotateWindow=Toplevel(canvas.data.mainWindow)
    rotateWindow.title("Rotate")
    rotateSlider=Scale(rotateWindow, from_=0, to=360, orient=HORIZONTAL)
    rotateSlider.pack()
    OkRotateFrame=Frame(rotateWindow)
    OkRotateButton=Button(OkRotateFrame, text="OK",\
                          command=lambda: closeRotateWindow(canvas))
    OkRotateButton.grid(row=0,column=0)
    OkRotateFrame.pack(side=BOTTOM)
    rotateFinished(canvas, rotateWindow, rotateSlider, 0)

def closeBrightnessWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.brightnessWindowClose=True

def changeBrightness(canvas, brightnessWindow, brightnessSlider, \
                     previousVal):
    if canvas.data.brightnessWindowClose==True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose=False
        
    else:
        if canvas.data.image!=None and brightnessWindow.winfo_exists():
            sliderVal=brightnessSlider.get()
            scale=(sliderVal-previousVal)/100.0
            canvas.data.image=canvas.data.image.point(\
                lambda i: i+ int(round(i*scale)))  
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.after(200, \
            lambda: changeBrightness(canvas, brightnessWindow, \
                                     brightnessSlider, sliderVal))

       
def brightness(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    brightnessWindow=Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Brightness")
    brightnessSlider=Scale(brightnessWindow, from_=-100, to=100,\
                           orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame=Frame(brightnessWindow)
    OkBrightnessButton=Button(OkBrightnessFrame, text="OK", \
                              command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0,column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider,0)
    brightnessSlider.set(0)

def reset(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.originalImage.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def mirror(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.mirror(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def flip(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.flip(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)


def transpose(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        imageData=list(canvas.data.image.getdata())
        newData=[]
        newimg=PIL.Image.new(canvas.data.image.mode,\
                (canvas.data.image.size[1], canvas.data.image.size[0]))
        for i in range(canvas.data.image.size[0]):
            addrow=[]
            for j in range(i, len(imageData), canvas.data.image.size[0]):
                addrow.append(imageData[j])
            addrow.reverse()
            newData+=addrow 
        newimg.putdata(newData)
        canvas.data.image=newimg.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def keyPressed(canvas, event):
    if event.keysym=="z":
        undo(canvas)
    elif event.keysym=="y":
        redo(canvas)
        
def undo(canvas):
    if len(canvas.data.undoQueue)>0:
        lastImage=canvas.data.undoQueue.pop()
        canvas.data.redoQueue.appendleft(lastImage)
    if len(canvas.data.undoQueue)>0:
        canvas.data.image=canvas.data.undoQueue[-1]
    save(canvas)
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

def redo(canvas):
    if len(canvas.data.redoQueue)>0:
        canvas.data.image=canvas.data.redoQueue[0]
    save(canvas)
    if len(canvas.data.redoQueue)>0:
        lastImage=canvas.data.redoQueue.popleft()
        canvas.data.undoQueue.append(lastImage)
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)
    
def saveAs(canvas):
    # ask where the user wants to save the file
    if canvas.data.image!=None:
        filename=asksaveasfilename(defaultextension=".jpg")
        im=canvas.data.image
        im.save(filename)

def save(canvas):
    if canvas.data.image!=None:
        im=canvas.data.image
        im.save(canvas.data.imageLocation)

def newImage(canvas):
    imageName=askopenfilename()
    filetype=""
    try: filetype=imghdr.what(imageName)
    except:
        tkinter.messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)
    if filetype in ['jpeg', 'bmp', 'png', 'tiff']:
        canvas.data.imageLocation=imageName
        im= PIL.Image.open(imageName)
        canvas.data.image=im
        canvas.data.originalImage=im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize=im.size
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)
    else:
      tkinter.messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)

def makeImageForTk(canvas):
    im=canvas.data.image
    if canvas.data.image!=None:
        imageWidth=canvas.data.image.size[0] 
        imageHeight=canvas.data.image.size[1]
        if imageWidth>imageHeight:
            resizedImage=im.resize((canvas.data.width,\
                int(round(float(imageHeight)*canvas.data.width/imageWidth))))
            canvas.data.imageScale=float(imageWidth)/canvas.data.width
        else:
            resizedImage=im.resize((int(round(float(imageWidth)*canvas.data.height/imageHeight)),\
                                    canvas.data.height))
            canvas.data.imageScale=float(imageHeight)/canvas.data.height
        canvas.data.resizedIm=resizedImage
        return ImageTk.PhotoImage(resizedImage)
 
def drawImage(canvas):
    if canvas.data.image!=None:
        # make the canvas center and the image center the same
        canvas.create_image(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0,
                        canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX=int(round(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0))
        canvas.data.imageTopY=int(round(canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0))

def init(root, canvas):

    buttonsInit(root, canvas)
    menuInit(root, canvas)
    canvas.data.image=None
    canvas.data.angleSelected=None
    canvas.data.rotateWindowClose=False
    canvas.data.brightnessWindowClose=False
    canvas.data.brightnessLevel=None
    canvas.data.histWindowClose=False
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.endCrop=False
    canvas.data.drawOn=True
    
    canvas.data.undoQueue=deque([], 10)
    canvas.data.redoQueue=deque([], 10)
    canvas.pack()

def buttonsInit(root, canvas):
    backgroundColour="white"
    buttonWidth=14
    buttonHeight=2
    toolKitFrame=Frame(root)
    rotateButton=Button(toolKitFrame, text="Rotate",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: rotate(canvas))
    rotateButton.grid(row=1,column=0)
    brightnessButton=Button(toolKitFrame, text="Brightness",\
                            background=backgroundColour ,\
                            width=buttonWidth, height=buttonHeight,\
                            command=lambda: brightness(canvas))
    brightnessButton.grid(row=2,column=0)
    histogramButton=Button(toolKitFrame, text="Histogram",\
                           background=backgroundColour ,\
                           width=buttonWidth,height=buttonHeight, \
                           command=lambda: histogram(canvas))
    histogramButton.grid(row=3,column=0)
    colourPopButton=Button(toolKitFrame, text="Colour Pop",\
                           background=backgroundColour, \
                           width=buttonWidth,height=buttonHeight, \
                           command=lambda: colourPop(canvas))
    colourPopButton.grid(row=4,column=0)
    mirrorButton=Button(toolKitFrame, text="Mirror",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: mirror(canvas))
    mirrorButton.grid(row=5,column=0)
    flipButton=Button(toolKitFrame, text="Flip",\
                      background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight, \
                      command=lambda: flip(canvas))
    flipButton.grid(row=6,column=0)
    transposeButton=Button(toolKitFrame, text="Transpose",\
                           background=backgroundColour, width=buttonWidth,\
                           height=buttonHeight,command=lambda: transpose(canvas))
    transposeButton.grid(row=7,column=0)
    drawButton=Button(toolKitFrame, text="Draw",\
                      background=backgroundColour ,width=buttonWidth,\
                      height=buttonHeight,command=lambda: drawOnImage(canvas))
    drawButton.grid(row=8,column=0)
    resetButton=Button(toolKitFrame, text="Reset",\
                       background=backgroundColour ,width=buttonWidth,\
                       height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=9,column=0)
    toolKitFrame.pack(side=LEFT)

def menuInit(root, canvas):
    menubar=Menu(root)
    menubar.add_command(label="New", command=lambda:newImage(canvas))
    menubar.add_command(label="Save", command=lambda:save(canvas))
    menubar.add_command(label="Save As", command=lambda:saveAs(canvas))
    ## Edit pull-down Menu
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo   Z", command=lambda:undo(canvas))
    editmenu.add_command(label="Redo   Y", command=lambda:redo(canvas))
    menubar.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menubar)
    root.config(menu=menubar)
    


def run():
    root = Tk()
    root.title("Image Editor")
    canvasWidth=500
    canvasHeight=500
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, \
                    background="gray")
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    canvas.data.mainWindow=root
    init(root, canvas)
    root.bind("<Key>", lambda event:keyPressed(canvas, event))
    root.mainloop() 


run()