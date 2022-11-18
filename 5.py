
import cv2 
import matplotlib.pyplot as plt
import numpy as np
import copy

class contrastStretch:
    def __init__(self):
        self.img="";
        self.hisin="";
        self.hisout="";
        self.original_image="";
        self.last_list=[]
        self.L=256
        self.sk=0
        self.k=0
        self.number_of_rows=0;
        self.number_of_cols=0;
        
    
    def stretch(self,input_image):
        self.img=cv2.imread(input_image,0);
        self.original_image=copy.deepcopy(self.img);
        x,y,z=plt.hist(self.img.ravel(),256,[0,256],label='x')
        self.k=np.sum(x)
        for i in range(len(x)):
            prk=x[i]/self.k
            self.sk+=prk
            last=(self.L-1)*self.sk        

            last = int(last)
            self.last_list.append(last)
            self.number_of_rows=(int(np.ma.count(self.img)/self.img[1].size))
            self.number_of_cols=self.img[1].size
        for i in range(self.number_of_cols):
            for j in range(self.number_of_rows):
                num=self.img[j][i]
                if num != self.last_list[num]:
                    self.img[j][i]=self.last_list[num]

    def plotHistogram(self,imgin):
        M,N=imgin.shape
        imgout=np.ones((M,self.L),np.uint8) *(256-1)
        h= np.zeros(self.L,np.int64) 
        for x in range (0,M):
            for y in range(0,N):
                r=imgin[x,y]
                h[r]=h[r]+1
        p=h/(M*N)
        scale=4000
        for r in range(0,self.L):
            cv2.line(imgout,(r,M-1),(r,M-int(scale*p[r])),(0,0,0))
        return imgout
         
    def showImage(self):
        cv2.imshow("Input-Image",self.original_image);
        cv2.imshow("Output-Image",self.img);
        cv2.imshow("In histogram",self.hisin);
        cv2.imshow("Ouput histogram",self.hisout);
        cv2.waitKey()
        cv2.destroyAllWindows()

stretcher=contrastStretch();

stretcher.stretch("./image/luffy.jpg");
stretcher.hisin=stretcher.plotHistogram(stretcher.original_image);
stretcher.hisout=stretcher.plotHistogram(stretcher.img);
stretcher.showImage();