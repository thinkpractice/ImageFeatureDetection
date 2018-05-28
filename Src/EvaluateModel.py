from keras.models import load_model
from keras.utils import to_categorical
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import os
import sys
import glob
import numpy as np

def getImmediateSubdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def getImagesInDirectory(directory, recursive):
    imageDir = directory + "/*.png"
    if recursive:
        imageDir = directory + "/**/*.png"
    for filename in glob.glob(imageDir, recursive=recursive):
        yield os.path.abspath(filename)

def loadImages(directory, label, image_width, image_height):
    labels = []
    images = []
    for filename in getImagesInDirectory(directory, False):
        image = imread(filename) * (1. / 255)
        resizedImage = resize(image, (image_height, image_width, 3))
        images.append(resizedImage)
        labels.append(label)
    return labels, images

def main(argv):
    image_width = 50
    image_height = 50

    if len(argv) <= 2:
        print("usage: EvaluateModel.py <modelFilename> <testDirectory> {image_width} {image_height}")
        exit(1)

    if len(argv) >= 5:
        image_width = int(argv[3])
        image_height = int(argv[4])

    modelDirectory = argv[1]
    testDirectory = argv[2]

    model = load_model(modelDirectory)
    model.summary()

    labels = []
    images = []
    numberOfLabels = 0
    for index, categoryDir in enumerate(getImmediateSubdirectories(testDirectory)):
        category_labels, category_images = loadImages(os.path.join(testDirectory, categoryDir), index, image_width, image_height)
        labels.extend(category_labels)
        images.extend(category_images)
        numberOfLabels += 1
    
    if numberOfLabels > 2:
        labels = to_categorical(labels)

    predictions = model.predict(np.array(images))
    class_predictions = [round(prediction[0]) for prediction in predictions]
    if numberOfLabels > 2:
        class_predictions = [np.argmax(prediction) for prediction in predictions]
        labels = [np.argmax(label) for label in labels]
    print(class_predictions)

    classificationReport = classification_report(labels, class_predictions)
    print("Classification Report: {}".format(classificationReport))

    confusionMatrix = confusion_matrix(labels, class_predictions)
    print("Confusion Matrix: {}".format(confusionMatrix))

if __name__ == "__main__":
    main(sys.argv)
