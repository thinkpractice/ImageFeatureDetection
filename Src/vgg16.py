from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
from keras.callbacks import Callback, ModelCheckpoint, TensorBoard
from keras.preprocessing.image import ImageDataGenerator
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os
import sys
import glob

image_width = 50
image_height = 50

def VGG_16(weights_path=None):
    model = Sequential()
    model.add(Conv2D(128, (3, 3), activation='relu', input_shape=(image_height, image_width, 3)))
    #model.add(MaxPooling2D((2,2)))
    #input 24x24x3
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2)))

    #model.add(Dropout(0.2))
    #model.add(MaxPooling2D((2,2)))

    #input 12x12x3
    model.add(Conv2D(256, (3, 3), activation='relu'))
    #model.add(MaxPooling2D((2,2)))

    #input 6x6x3
    model.add(Conv2D(512, (3, 3), activation='relu'))
    #model.add(Dropout(0.2))
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
     
    #input 4x4x3
    #model.add(Conv2D(256, (3, 3), activation='relu'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))
    #model.add(ZeroPadding2D((1,1)))
    #model.add(Conv2D(256, (3, 3), activation='relu'))
    #model.add(ZeroPadding2D((1,1)))
    #model.add(Conv2D(256, (3, 3), activation='relu'))
    #model.add(ZeroPadding2D((1,1)))
    #model.add(Conv2D(256, (3, 3), activation='relu'))
    #model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(Flatten())
    #model.add(Dense(2048, activation='relu'))
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation="sigmoid"))

    if weights_path:
        model.load_weights(weights_path)

    return model

def getImagesInDirectory(directory, recursive):
    imageDir = directory + "/*.png"
    if recursive:
        imageDir = directory + "/**/*.png"
    for filename in glob.glob(imageDir, recursive=recursive):
        yield os.path.abspath(filename)

def padImage(image, newWidth, newHeight):
    extraRows = newWidth - image.shape[0]
    extraColumns = newHeight - image.shape[1]
    paddedChannels = [np.pad(image[:,:,i],((0, extraRows), (0, extraColumns)), mode="constant",constant_values=0) for i in range(3)]
    return np.stack(paddedChannels, axis = 2)

def loadImages(directory, label):
    labels = []
    images = []
    for filename in getImagesInDirectory(directory, False):
        image = imread(filename) * (1. / 255)
        resizedImage = resize(image, (image_height, image_width))
        images.append(resizedImage)
        labels.append(label)
    return labels, images

def countImages(directory):
    return len([item for item in getImagesInDirectory(directory, True)])

def loadData(trainDirectory, testDirectory, batchSize):
    train_datagen = ImageDataGenerator(rescale=1./255,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest")

    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        trainDirectory,
        target_size=(image_height, image_width),
        batch_size=batchSize,
        class_mode='binary')

    validation_generator = test_datagen.flow_from_directory(
        testDirectory,
        target_size=(image_height, image_width),
        batch_size=batchSize,
        class_mode='binary')

    return train_generator, validation_generator

def getDirectoryNameForRun(epochs, batchSize, learningRate, decay):
    date = datetime.datetime.now().strftime("%d%m%Y-%H:%M")
    return './logs/run_{}_ep={}_bs={}_lr={},dc={}'.format(date, epochs, batchSize, learningRate, decay)

def main(argv):
    if len(argv) <= 2:
        print("usage: vgg16.py <trainDirectory> <testDirectory>")
        exit(1)

    trainDirectory = argv[1]
    testDirectory = argv[2]

    learningRate = 0.01
    decay = 1e-6
    epochs = 200
    #epochs = 20
    batchSize = 32
    print("Loading data...")
    train_generator, validation_generator = loadData(trainDirectory, testDirectory, batchSize)
    numberOfTrainingImages = countImages(trainDirectory)
    print(numberOfTrainingImages)
    numberOfValidationImages = countImages(testDirectory)
    print(numberOfValidationImages)
    # Test pretrained model
    #model = VGG_16('vgg16_weights.h5')
    print("Compiling model...")
    model = VGG_16()
    model.summary()
    sgd = SGD(lr=learningRate, decay=decay, momentum=0.6, nesterov=True)
    model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=["accuracy"])

    print("Training model...")
    modelCheckPoint = ModelCheckpoint("weights.{epoch:02d}-{val_acc:.2f}.hdf", save_best_only=True)

    logDir = getDirectoryNameForRun(epochs, batchSize, learningRate, decay)
    tensorBoard = TensorBoard(log_dir=logDir, batch_size=batchSize, write_images=True)

    model.fit_generator(
        train_generator,
        steps_per_epoch=numberOfTrainingImages/batchSize,
        epochs=epochs,
        verbose=1,
        validation_data=validation_generator,
        validation_steps=numberOfValidationImages/batchSize,
        callbacks=[modelCheckPoint, tensorBoard])


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
