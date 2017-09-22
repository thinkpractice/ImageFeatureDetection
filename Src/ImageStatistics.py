import numpy as np
import math

def normalizeImage(image):
    return image / 255

def imageMean(image):
    return (1 / image.size) * np.sum(image)

def centerImage(image):
    return image - imageMean(image)

def imageCovariance(image1, image2):
    return (1 / image1.size) * np.dot(centerImage(image1).ravel(), centerImage(image2).ravel())

def imageVariance(image):
    return imageCovariance(image, image)

def linearCorrelation(image1, image2):
    return imageCovariance(image1, image2) / math.sqrt(imageVariance(image1) * imageVariance(image2))

def rgbApply(image, function):
    return [function(image[:,:,i]) for i in range(3)]

def rgbImageMean(image):
    return rgbApply(image, lambda imageBand: imageMean(imageBand))

def rgbCenterImage(image):
    return np.stack(rgbApply(image, lambda imageBand: centerImage(imageBand)),axis=2)

def rgbImageVariance(image):
    return rgbApply(image, lambda imageBand: imageVariance(imageBand))

def rgbImageCovarianceMatrix(rgbImage):
    covarianceMatrix = np.zeros([3,3])
    for r in range(3):
        for c in range (3):
            covariance = imageCovariance(rgbImage[:,:,r], rgbImage[:,:,c])
            covarianceMatrix[r, c] = covariance
            covarianceMatrix[c, r] = covariance
    return covarianceMatrix

def flattenImage(rgbImage):
    return rgbImage.reshape(rgbImage.shape[0] * rgbImage.shape[1], 3)

def pca(rgbImage):
    covarianceMatrix = rgbImageCovarianceMatrix(rgbImage)
    return np.linalg.svd(covarianceMatrix)

def pcaTransform(rgbImage):
    u,s,v = pca(rgbImage)
    imageVector = flattenImage(rgbImage)
    transposedVector = imageVector.dot(v)
    return transposedVector.reshape(rgbImage.shape)

def fractionOfInformation(rgbImage):
    pass
