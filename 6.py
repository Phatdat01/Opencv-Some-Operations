import cv2
import numpy as np
def plotHistogram(imgin):
        M,N=imgin.shape[:2]
        imgout=np.ones((M,256),np.uint8) *255
        h= np.zeros(256,np.int64) 
        for x in range (0,M):
            for y in range(0,N):
                r=imgin[x,y]
                h[r]=h[r]+1
        p=h/(M*N)
        scale=4000
        for r in range(0,256):
            cv2.line(imgout,(r,M-1),(r,M-int(scale*p[r])),(0,0,0))

        return imgout

def histogramEqualization(image: str, adjustType: str = "local", colorInfo: str = "color"):
    img = cv2.imread(image)
    if(colorInfo == "gray"):
        img = cv2.imread(image, 0)
    if(img.ndim == 2):
        if(adjustType == 'global'):
            output = cv2.equalizeHist(img)
        else:
            clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(10, 10))
            output = clahe.apply(img)
    else:
        HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        V = HSV[:, :, 2]
        if(adjustType == 'global'):
            equalized = cv2.equalizeHist(V)
        else:
            clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(10, 10))
            equalized = clahe.apply(V)
        HSV[:, :, 2] = equalized
        output = cv2.cvtColor(HSV, cv2.COLOR_HSV2BGR)


    cv2.imshow("intput", img)
    cv2.imshow("output", output)
    inplot=plotHistogram(img)
    cv2.imshow("inplot", inplot)
    outplot=plotHistogram(output)
    cv2.imshow("outplot", outplot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
histogramEqualization("./image/naruto.png")
