import cv2
import numpy as np

X = 220
Y = 280
OPAQUE = 0.7
small=7

def merge(original, add, opaque=1.0, gamma=0):
    x_abs, y_abs = X, Y
    add_h, add_w = tuple([int(x/small) for x in add.shape[:2]])
    add=cv2.resize(add, (add_h, add_w))

    patch = original[y_abs:y_abs+add_h, x_abs:x_abs+add_w, :]
    blended = cv2.addWeighted(src1=patch, alpha=1-opaque, src2=add, beta=opaque, gamma=gamma)
    result = original.copy()
    result[y_abs:y_abs+add_h, x_abs:x_abs+add_w, :] = blended
    return result

def main(original, add):
    original = cv2.imread(original)
    add = cv2.imread(add)
    result = merge(original, add, opaque=OPAQUE)
    cv2.imshow("Merge", result)
    cv2.waitKey()
    cv2.destroyAllWindows()

original = "./image/girl.jpg"
add = "./image/icon.png"

if __name__ == "__main__":
    main(original, add)
