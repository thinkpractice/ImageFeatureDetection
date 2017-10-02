from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
from keras.callbacks import Callback
from keras.preprocessing.image import ImageDataGenerator
from skimage.io import imread
from skimage.transform import resize
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import glob

def VGG_16(weights_path=None):
    model = Sequential()
    model.add(ZeroPadding2D((1,1),input_shape=(224,224, 3)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(256, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(ZeroPadding2D((1,1)))
    model.add(Conv2D(512, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    #model.add(Dense(1000, activation='softmax'))
    model.add(Dense(2, activation='softmax'))
    #model.add(Dense(1, activation="sigmoid"))

    if weights_path:
        model.load_weights(weights_path)

    return model

class AccuracyHistory(Callback):
    def on_train_begin(self, logs={}):
        self.acc = []

    def on_epoch_end(self, batch, logs={}):
        self.acc.append(logs.get('acc'))

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
    train_datagen = ImageDataGenerator(samplewise_center=True, samplewise_std_normalization=True, rescale=1./255)
#        rescale=1./255,
#        shear_range=0.2,
#        zoom_range=0.2,
#        horizontal_flip=True)

    test_datagen = ImageDataGenerator(samplewise_center=True, samplewise_std_normalization=True, rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        trainDirectory,
        target_size=(224, 224),
        batch_size=batchSize,
        class_mode='categorical')

    validation_generator = test_datagen.flow_from_directory(
        testDirectory,
        target_size=(224, 224),
        batch_size=batchSize,
        class_mode='categorical')

    return train_generator, validation_generator

def main(argv):
    if len(argv) <= 2:
        print("usage: vgg16.py <trainDirectory> <testDirectory>")
        exit(1)

    trainDirectory = argv[1]
    testDirectory = argv[2]

    epochs = 1
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
    sgd = SGD(lr=0.001, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='binary_crossentropy', metrics=["accuracy"])

    print("Training model...")
    history = AccuracyHistory()
    
    model.fit_generator(
        train_generator,
        steps_per_epoch=numberOfTrainingImages/batchSize,
        epochs=epochs,
        verbose=1,
        validation_data=validation_generator,
        validation_steps=numberOfValidationImages/batchSize)

    model.save('zonnepanelen.h5')

    #score = model.evaluate(x_test, y_test, verbose=0)
    #print('Test loss:', score[0])
    #print('Test accuracy:', score[1])
    #out = model.predict(im)
    #print np.argmax(out)
    plt.plot(range(1,epochs + 1),history.acc)
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.show()

if __name__ == "__main__":
    main(sys.argv)
