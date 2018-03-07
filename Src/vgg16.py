from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
from keras.callbacks import Callback, ModelCheckpoint, TensorBoard
from keras.preprocessing.image import ImageDataGenerator
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
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
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(image_height, image_width, 3)))
    #model.add(MaxPooling2D((2,2)))
    #input 24x24x3
    model.add(Conv2D(32, (3, 3), activation='relu'))
    #model.add(Dropout(0.2))
    #model.add(MaxPooling2D((2,2)))

    #input 12x12x3
    model.add(Conv2D(64, (3, 3), activation='relu'))
    #model.add(MaxPooling2D((2,2)))

    #input 6x6x3
    model.add(Conv2D(128, (3, 3), activation='relu'))
    #model.add(Dropout(0.2))
    model.add(MaxPooling2D((2,2)))
     
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
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation="sigmoid"))

    if weights_path:
        model.load_weights(weights_path)

    return model

def getImagesInDirectory(directory):
    imageDir = directory + "/**/*.png"
    print(imageDir)
    for filename in glob.glob(imageDir, recursive=True):
        yield os.path.join(directory, filename)

def padImage(image, newWidth, newHeight):
    extraRows = newWidth - image.shape[0]
    extraColumns = newHeight - image.shape[1]
    paddedChannels = [np.pad(image[:,:,i],((0, extraRows), (0, extraColumns)), mode="constant",constant_values=0) for i in range(3)]
    return np.stack(paddedChannels, axis = 2)

def loadImages(directory):
    for filename in getImagesInDirectory(directory):
        image = imread(filename)
        if image.shape[0] > 224 or image.shape[1] > 224:
            yield resize(image, (224, 224))
        else:
            yield padImage(image, 224, 224)

def countImages(directory):
    return len([item for item in getImagesInDirectory(directory)])

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

    learningRate = 0.1
    decay = 1e-6
    epochs = 100
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
    sgd = SGD(lr=0.1, decay=1e-6) # , momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=["accuracy"])

    print("Training model...")
    modelCheckPoint = ModelCheckpoint("weights.{epoch:02d}-{val_loss:.2f}.hdf", save_best_only=True)

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

if __name__ == "__main__":
    main(sys.argv)
