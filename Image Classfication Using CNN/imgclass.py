import tensorflow as tf
import cv2 as cv
import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
import matplotlib.pyplot as plt
import scipy

img = image.load_img("D:/Work/Imgclas/train/blocks\Screenshot 2023-08-01 155707.png")
plt.imshow(img)
imarr = cv.imread("D:/Work/Imgclas/train/blocks\Screenshot 2023-08-01 155707.png")
imarr.shape
train = ImageDataGenerator(rescale=1.0 / 255)
train_dataset = train.flow_from_directory(
    "D:/Work/Imgclas/train",
    target_size=(300, 400),
    batch_size=3,
    class_mode="binary",
)
train_dataset.class_indices
model = tf.keras.Sequential(
    [
        tf.keras.layers.Conv2D(
            512, (3, 3), activation="relu", input_shape=(300, 300, 3)
        ),
        tf.keras.layers.MaxPool2D(2, 2),
        tf.keras.layers.Conv2D(256, (3, 3), activation="relu"),
        tf.keras.layers.MaxPool2D(2, 2),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
        tf.keras.layers.MaxPool2D(2, 2),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPool2D(2, 2),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(512, activation="relu"),
        tf.keras.layers.Dense(1, activation="sigmoid"),
    ]
)
model.compile(
    loss="binary_crossentropy",
    optimizer=RMSprop(learning_rate=0.01),
    metrics=["accuracy"],
)
model_fit = model.fit(train_dataset, epochs=50, steps_per_epoch=13, batch_size=30)
dir_path = "D:/Work/Imgclas/test"
for i in os.listdir(dir_path):
    img = image.load_img(dir_path + "//" + i, target_size=(300, 400))
    plt.imshow(img)
    plt.show()

    X = image.img_to_array(img)
    X = np.expand_dims(X, axis=0)
    images = np.vstack([X])
    val = model.predict(images)
    if val == 0:
        print("Blocks are detected")
    else:
        print("Blocks are not detected")
