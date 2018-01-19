from keras.models import Model
from keras.layers.core import Input, Flatten, Dense, Dropout
from keras.layers.convolutional import UpSampling2D, Conv2D, MaxPooling2D, ZeroPadding2D
from keras.callbacks import Callback, ModelCheckpoint, TensorBoard
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
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
    input_img = Input(shape=(image_height, image_width, 3))
    e = Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
    e = MaxPooling2D((2,2), padding='same')(e)
    #input 24x24x3
    e = Conv2D(32, (3, 3), activation='relu', padding='same')(e)
    e = MaxPooling2D((2,2), padding='same')(e)

    #input 12x12x3
    e = Conv2D(64, (3, 3), activation='relu', padding='same')(e)
    e = MaxPooling2D((2,2), padding='same')(e)

    #input 6x6x3
    e = Conv2D(128, (3, 3), activation='relu', padding='same')(e)
    e = UpSampling2D((2,2), padding='same')(e)

    d = Conv2D(128, (3, 3), activation='relu', padding='same')(e)
    d = UpSampling2D((2,2))(d)

    d = Conv2D(64, (3, 3), activation='relu', padding='same')(d)
    d = UpSampling2D((2,2))(d)

    d = Conv2D(32, (3, 3), activation='relu', padding='same')(d)
    d = UpSampling2D((2,2))(d)

    d = Conv2D(16, (3, 3), activation='relu', padding='same')(d)
    d = UpSampling2D((2,2))(d)

    decoded = Conv2D(1, (3,3), activation='sigmoid', padding='same')(d)
    model = Model(input_img, decoded)
    return model

def getImagesInDirectory(directory):
    imageDir = directory + "/**/*.png"
    print(imageDir)
    for filename in glob.glob(imageDir, recursive=True):
        yield os.path.join(directory, filename)

def loadImages(directory):
    for filename in getImagesInDirectory(directory):
        image = load_image(filename)
        imageArray = img_to_array(image)
        imageArray = imageArray.astype('float32') / 255.
        if image.shape[0] != image_height or image.shape[1] != image_width:
            yield resize(image, (image_height, image_shape))

def countImages(directory):
    return len([item for item in getImagesInDirectory(directory)])

def getDirectoryNameForRun(epochs, batchSize, learningRate, decay):
    date = datetime.datetime.now().strftime("%d%m%Y-%H:%M")
    return './logs/run_{}_ep={}_bs={}_lr={},dc={}'.format(date, epochs, batchSize, learningRate, decay)

def main(argv):
    if len(argv) <= 2:
        print("usage: conv_autoencoder.py <trainDirectory> <testDirectory>")
        exit(1)

    trainDirectory = argv[1]
    testDirectory = argv[2]

    learningRate = 0.1
    decay = 1e-6
    epochs = 50
    batchSize = 32
    print("Loading data...")
    trainingImages = np.array([image for image in loadImages(trainDirectory)])
    numberOfTrainingImages = trainingImages.shape[0]
    print(numberOfTrainingImages)
    validationImages = np.array([image for image in loadImages(testDirectory)])
    numberOfValidationImages = validationImage.shape[0]
    print(numberOfValidationImages)

    print("Compiling model...")
    model = VGG_16()
    model.summary()
    model.compile(optimizer="adadelta", loss='binary_crossentropy')

    print("Training model...")
    modelCheckPoint = ModelCheckpoint("ae_weights.{epoch:02d}-{val_loss:.2f}.hdf", save_best_only=True)

    logDir = getDirectoryNameForRun(epochs, batchSize, learningRate, decay)
    tensorBoard = TensorBoard(log_dir=logDir, batch_size=batchSize, write_images=True)

    model.fit(
        trainingImages, trainingImages,
        epochs=epochs,
        verbose=1,
        validation_data=(validationImages, validationImages),
        callbacks=[modelCheckPoint, tensorBoard])

if __name__ == "__main__":
    main(sys.argv)
