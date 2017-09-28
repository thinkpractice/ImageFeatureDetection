from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
from keras.callbacks import Callback
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

    if weights_path:
        model.load_weights(weights_path)

    return model

class AccuracyHistory(Callback):
    def on_train_begin(self, logs={}):
        self.acc = []

    def on_epoch_end(self, batch, logs={}):
        self.acc.append(logs.get('acc'))

def getImagesInDirectory(directory):
    for filename in glob.glob1(directory, "*.png"):
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
    return len(getImagesInDirectory(directory))

def countAllImages(positivesDirectory, negativesDirectory):
    numberOfImages = countImages(positivesDirectory)
    numberOfImages += countImages(negativesDirectory)
    return numberOfImages

def loadDatav(positivesDirectory, negativesDirectory, batchSize):
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        'data/train',
        target_size=(224, 224),
        batch_size=batchSize,
        class_mode='binary')

    validation_generator = test_datagen.flow_from_directory(
        'data/validation',
        target_size=(224, 224),
        batch_size=batchSize,
        class_mode='binary')

#    x = []
#
#    y = []
#
#    positives = 0
#    for image in loadImages(positivesDirectory):
#        x.append(image)
#        positives += 1
#    y.extend([1 for _ in range(positives)])
#
#    negatives = 0
#    for image in loadImages(negativesDirectory):
#        x.append(image)
#        negatives += 1
#    y.extend([0 for _ in range(negatives)])
#
#    x = np.array(x)
#    print(x.shape)
#
#    x_train, x_test, y_train, y_test = train_test_split(x,y)
#    return np.array(x_train), np.array(x_test), np.array(y_train), np.array(y_test)
    return train_generator, validation_generator

def main(argv):
    if len(argv) <= 2:
        print("usage: vgg16.py <positivesDirectory> <negativesDirectory>")
        exit(1)

    positivesDirectory = argv[1]
    negativesDirectory = argv[2]

    epochs = 10
    batch_size=32
    print("Loading data...")
    train_generator, validation_generator = loadData(positivesDirectory, negativesDirectory, batchSize)
    numberOfTrainingImages = countAllImages(positivesDirectory, negativesDirectory)
    numberOfValidationImages = numberOfTrainingImages
    # Test pretrained model
    #model = VGG_16('vgg16_weights.h5')
    print("Compiling model...")
    model = VGG_16()
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=["accuracy"])

    print("Training model...")
    history = AccuracyHistory()
    #model.fit(x_train, y_train,
    #      batch_size=batch_size,
    #      epochs=epochs,
    #      verbose=1,
    #      validation_data=(x_test, y_test),
    #      callbacks=[history])
    
    model.fit_generator(
        train_generator,
        steps_per_epoch=numberOfImages/batchSize,
        epochs=epochs,
        verbose=1,
        validation_data=validation_generator,
        validation_steps=numberOfValidationImages/batchSize)
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    #out = model.predict(im)
    #print np.argmax(out)
    plt.plot(range(1,epochs + 1),history.acc)
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.show()

if __name__ == "__main__":
    main(sys.argv)
