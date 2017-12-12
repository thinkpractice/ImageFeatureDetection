from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D, ZeroPadding2D
from keras.optimizers import SGD
from keras.callbacks import Callback
from keras.preprocessing.image import ImageDataGenerator
import sys

def cnn():
    model = Sequential()
    return model

def dataGeneratorFor(directory, batchSize, classMode):
    dataGenerator = ImageDataGenerator(rescale=1./255)
    generator = dataGenerator.flow_from_directory(directory, target_size=(224,224), batch_size=batchSize, class_mode=classMode))
    return generator

def trainModel(model, epochs, batchSize):
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9)#, nesterov=True)
    model.compile(optimizer=sgd, loss='categorical_crossentropy', metrics=["accuracy"])
    
    modelCheckpoint = ModelCheckpoint("cnn_{epoch:02d}_{val_acc:.2f}.hdf5", monitor="val_acc", verbose=1, save_best_only=True)

    model.fit_generator(
        train_generator,
        steps_per_epoch=numberOfTrainingImages/batchSize,
        epochs=epochs,
        verbose=1,
        validation_data=validation_generator,
        validation_steps=numberOfValidationImages/batchSize,
        callbacks=[modelCheckpoint])

def main(argv):
    if len(argv) <= 3:
        print("usage: cnn.py <trainDirectory> <testDirectory> <#epochs>")
        exit(1)

    trainDirectory = argv[1]
    testDirectory = argv[2]
    epochs = int(argv[3])
    batchSize = 30

    trainData = dataGeneratorFor(trainDirectory, batchSize, "categorical")
    testData = dataGeneratorFor(testDirectory, batchSize, "categorical")

    model = cnn()
    trainModel(model, epochs, batchSize)

if __name__ == "__main__":
    main(sys.argv)
