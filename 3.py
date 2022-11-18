import cv2
import numpy as np

def main(mainimg, bground):
      image = cv2.imread(mainimg)
      image_copy = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      lower_blue = np.array([0, 0, 100])
      upper_blue = np.array([120, 100, 255]) 
      mask = cv2.inRange(image_copy, lower_blue, upper_blue)
      masked_image = np.copy(image)
      masked_image[mask != 0] = [0, 0, 0]
      
      # ## background
      background_image = cv2.imread(bground)
      crop_background = background_image[0:720, 0:1280]
      crop_background[mask == 0] = [0, 0, 0]
      final_image = crop_background + masked_image
      cv2.imshow("merge no background of tree",final_image)
      cv2.waitKey()
      cv2.destroyAllWindows()

mainimg="./image/item.jpg"
bground="./image/bg.jpg"

if __name__ == "__main__":
    main(mainimg, bground)