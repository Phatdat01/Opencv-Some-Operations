import numpy as np
import cv2
import time

# http://www.librow.com/articles/article-9

def gkern(l=15, sig=1.5):
    ax = np.linspace(-int(l - 1) / 2., int(l - 1) / 2., l)
    gauss= 1/(sig*(2*np.pi)**-2)*np.exp(-0.5*ax**2/sig**2)
    fx= (-ax/sig**2)*1/(sig*(2*np.pi)**-2)*np.exp(-0.5*ax**2/sig**2)
    # kernel = np.outer(gauss, gauss)
    kernel = np.outer(fx, fx)

    return kernel / np.sum(kernel)

def convolution (img, kernel):
    img_w, img_h = img.shape[:2]
    kernel_w, kernel_h = kernel.shape[:2]

#rgb
    if(len(img.shape) == 3):
        image_pad = np.pad(img, pad_width=(\
            (kernel_h // 2, kernel_h // 2),(kernel_w // 2,\
            kernel_w // 2),(0,0)), mode='constant',\
            constant_values=0).astype(np.float32)

#gray
    if(len(img.shape) == 2):
        image_pad = np.pad(img, pad_width=(\
            (kernel_h // 2, kernel_h // 2),(kernel_w // 2,\
            kernel_w // 2)), mode='constant',\
            constant_values=0).astype(np.float32)

    h = kernel_h // 2
    w = kernel_w // 2

    image_conv = np.zeros(image_pad.shape)

    for i in range(h, image_pad.shape[0] - h):
        for j in range(w, image_pad.shape[1] - w):
            # sum = 0
            if len(image_pad.shape) == 3:
                for lo in range(3):
                    x = image_pad[i - h:i + h+1, j - w:j +w+1,lo]
                    x = x * kernel
                    image_conv[i,j,lo] = x.sum()

    h_end = -h
    w_end = -w

    if (h == 0):
        return image_conv[h:, w:w_end]
    if (w == 0):
        return image_conv[h:h_end, w:]

    return image_conv[h:h_end, w:w_end,:]

if __name__ == "__main__":
    file = "./image/girl.jpg"
    print(f"getting image")
    start_time = time.time()
    m = cv2.imread(file)
    print(f"time ended. Took {time.time()- start_time}")

    print(m.shape)
    w, h = m.shape[:2]
    print(f"starting kernel process")
    start_time = time.time()
    kernel = gkern()
    print(f"kernel ended. Took {time.time()- start_time}")

    output = np.zeros(m.shape)

    print(f"starting convolution")
    start_time = time.time()
    out = (convolution(m,kernel))
    print(f"convolution ended. Took {time.time() -start_time}")

    cv2.imshow("",out.astype(np.uint8))
    cv2.waitKey()
    cv2.destroyAllWindows()