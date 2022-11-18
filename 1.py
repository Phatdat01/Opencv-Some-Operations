import cv2
import numpy as np

def nothing (x):
    pass

# Create a black background window
# img = np.zeros ((300,512,3), np.uint8)
img=cv2.imread("./image/naruto.png")
cv2.namedWindow (' image ')

# Create scroll bars that change colors
cv2.createTrackbar (' R ', ' image ', 0,255,nothing)
cv2.createTrackbar (' G ', ' image ', 0,255,nothing)
cv2.createTrackbar (' B ', ' image ', 0,255,nothing)

flag=0
if img!=np.zeros ((300,512,3), np.uint8):
    flag=1
filter=[0,0,0]
while(1):
    cv2.imshow (' image ', img)
    k = cv2.waitKey (1) & 0xFF
    if k ==27: 
        break
    
    r = cv2.getTrackbarPos (' R ', ' image ')
    g = cv2.getTrackbarPos (' G ', ' image ')
    b = cv2.getTrackbarPos (' B ', ' image ')
    if (flag==1):
        if filter!=[b,g,r]:
            temp=filter
            filter=[b,g,r]
            img[:] = img[:]+filter-temp
    else:
        img[:] = [b,g,r]

cv2.destroyAllWindows ()