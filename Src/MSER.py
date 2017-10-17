import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

def main(argv):
    filename = argv[1]
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    #blurredImage = cv2.GaussianBlur(image, (3,3), 0)

    mser = cv2.MSER_create()
    mser_areas, _ = mser.detectRegions(image)
    print(len(mser_areas))
    #image2 = image.copy()
    hulls = [cv2.convexHull(p.reshape(-1, 1,2)) for p in mser_areas]
    #cv2.polylines(image2, hulls, 1, (0,255, 0))
    ##cv2.imshow('img', image2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    maskedImages = []
    for contour in hulls:
        mask = np.zeros(image.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, (255,255,255), -1)
        maskedImages.append(cv2.bitwise_and(image, image, mask=mask))

    fig, axes = plt.subplots(1,2+len(maskedImages))
    axes[0].imshow(image)
    axes[1].imshow(image)
    for i in range(len(maskedImages)):
        axes[2+i].imshow(maskedImages[i])
    #axes[1].scatter(hulls[:,0], hulls[:,1])
    plt.show()

if __name__ == "__main__":
    main(sys.argv)

