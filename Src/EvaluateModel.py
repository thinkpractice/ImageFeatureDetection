from keras.models import load_model
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import os
import sys
import glob
import numpy as np

def getImagesInDirectory(directory, recursive):
    imageDir = directory + "/*.png"
    if recursive:
        imageDir = directory + "/**/*.png"
    for filename in glob.glob(imageDir, recursive=recursive):
        yield os.path.abspath(filename)

def loadImages(directory, label):
    labels = []
    images = []
    for filename in getImagesInDirectory(directory, False):
        image = imread(filename) * (1. / 255)
        resizedImage = resize(image, (image_height, image_width))
        images.append(resizedImage)
        labels.append(label)
    return labels, images

def main(argv):
    if len(argv) <= 2:
        print("usage: EvaluateModel.py <modelFilename> <testDirectory>")
        exit(1)

    modelDirectory = argv[1]
    testDirectory = argv[2]

    model = load_model(modelDirectory)
    model.summary()

    positive_labels, positive_images = loadImages(os.path.join(testDirectory, "Positives"), 1)
    negative_labels, negative_images = loadImages(os.path.join(testDirectory, "Negatives"), 0)
    labels = positive_labels
    labels.extend(negative_labels)
    images = positive_images
    images.extend(negative_images)
    
    predictions = model.predict(np.array(images))
    predictions = [round(prediction[0]) for prediction in predictions]
    print(predictions)
   
    classificationReport = classification_report(labels, predictions)
    print("Classification Report: {}".format(classificationReport))

    confusionMatrix = confusion_matrix(labels, predictions)
    print("Confusion Matrix: {}".format(confusionMatrix))

if __name__ == "__main__":
    main(sys.argv)
