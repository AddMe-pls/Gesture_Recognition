print('Importing libraries: ', end="")

from tensorflow.python.keras.models import Sequential, load_model
from tensorflow.python.keras.layers.core import Dense, Dropout, Activation, Flatten
from tensorflow.python.keras.layers.convolutional import Conv3D, MaxPooling3D
from tensorflow.python.keras.layers import BatchNormalization
from tensorflow.python.keras.layers import GlobalMaxPool2D
from tensorflow.python.keras.layers import LSTM
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import Reshape
#from tensorflow.python.keras.optimizers import SGD
from tensorflow.python.keras.utils import np_utils, generic_utils
from tensorflow.keras.callbacks import ModelCheckpoint

import pickle
import os
import numpy as np
import cv2
import pyautogui as pag
import win32gui as win
import re
import time
import vlc

time.sleep(2)

print('done')
nb_classes = 27

print('Building model: ', end="")
model = Sequential()
#`channels_last` corresponds to inputs with shape `(batch, spatial_dim1, spatial_dim2, spatial_dim3, channels)`
strides = (1,1,1)
kernel_size = (3, 3, 3)
model.add(Conv3D(32, kernel_size, strides=strides, activation='relu', padding='same', input_shape=(32, 64, 96, 3)))
#print(model.output_shape)
model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(1, 2, 2)))
#print(model.output_shape)

model.add(Conv3D(64, kernel_size, strides=strides, activation='relu',padding='same'))
#print(model.output_shape)
model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(1, 2, 2)))
#print(model.output_shape)

model.add(Conv3D(128, kernel_size, strides=strides, activation='relu',padding='same'))
#print(model.output_shape)
model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(1, 2, 2)))
#print(model.output_shape)

model.add(Conv3D(256, kernel_size, strides=strides, activation='relu',padding='same'))
#print(model.output_shape)
model.add(BatchNormalization())

model.add(Conv3D(256, kernel_size, strides=strides, activation='relu',padding='same'))
#print(model.output_shape)
model.add(BatchNormalization())

model.add(Conv3D(256, kernel_size, strides=strides, activation='relu',padding='same'))
#print(model.output_shape)
model.add(BatchNormalization())

model.add(MaxPooling3D(pool_size=(1,8,12)))
#print(model.output_shape)

model.add(Reshape((32, 256)))
#print(model.output_shape)
model.add(LSTM(256, return_sequences=True))
#print(model.output_shape)
model.add(LSTM(256))
#print(model.output_shape)

model.add(Dense(256, activation='relu'))
#print(model.output_shape)

model.add(Dense(nb_classes, activation='softmax'))
#print(model.output_shape)
print('done')
# model.add(LSTM(256))

to_predict = []
classes = ['Pushing Two Fingers Away',
 'Pushing Hand Away',
 'Doing other things',
 'Turning Hand Clockwise',
 'Zooming In With Two Fingers',
 'Sliding Two Fingers Left',
 'Stop Sign',
 'Pulling Two Fingers In',
 'Drumming Fingers',
 'Sliding Two Fingers Right',
 'Sliding Two Fingers Down',
 'No gesture',
 'Rolling Hand Backward',
 'Swiping Down',
 'Rolling Hand Forward',
 'Turning Hand Counterclockwise',
 'Thumb Down',
 'Swiping Up',
 'Zooming Out With Full Hand',
 'Shaking Hand',
 'Thumb Up',
 'Zooming In With Full Hand',
 'Swiping Right',
 'Zooming Out With Two Fingers',
 'Swiping Left',
 'Sliding Two Fingers Up',
 'Pulling Hand In']

model.load_weights('main.h5')
num_frames = 0
cap = cv2.VideoCapture(0)
cap.set(12, 50)
cap.set(6, 10)

preds = []

classe = ''
import time 

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame_cp = frame

    frame_cp = cv2.resize(frame, (96, 64))

    q = cv2.imread('quite.png')
    to_predict.append(frame_cp)
    to_predict.append(frame_cp)
    
    predict = 0
    if len(to_predict) == 32:

        frame_to_predict = [[]]
        frame_to_predict[0] = np.array(to_predict, dtype=np.float32)


        predict = model.predict(np.array(frame_to_predict))
        classe = classes[np.argmax(predict)]
        if np.argmax(predict) not in [2]:
            if np.amax(predict) > 0.65:
                print('Class = ',classe, 'Precision = ', np.amax(predict)*100,'%')
                preds.append(np.argmax(predict))
                with open('gesture.pkl','wb') as f:
                    pickle.dump(np.argmax(predict), f)

                ##hdwd = win.GetWindowText(win.GetForegroundWindow())
                ##pattern = r"(Microsoft PowerPoint)+"
                    #if classe == 'Thumbs Down':
                    #    pag.hotkey('alt', 'f4')

                    #if classe == 'Thumbs Up':
                    #   pag.hotkey('altleft', 'tab')

                    #if classe == 'Zooming Out With Full Hand':
                    #    pag.hotkey('fn', 'f5')

                    if "PowerPoint" in win.GetWindowText(win.GetForegroundWindow()):
                        print("-----------------------PowerPoint-----------------------")
                        # if classe == 'Pulling Hand In':
                        #    pag.hotkey('alt', 'tab')
                        if classe == 'Thumbs Down':
                            pag.press('esc')

                        if classe == 'Thumbs Up':
                            pag.press('f5')

                        if classe == 'Swiping Left':  # left == right потому что изображение с камеры отзеркалено
                            pag.press('left')

                        if classe == 'Swiping Right':  # left == right потому что изображение с камеры отзеркалено
                            pag.press('right')

                        #if classe == 'Thumb Up':
                        #    pag.press('f5')

                        if classe == 'Sliding Two Fingers Down':
                            pag.press('up')

                        if classe == 'Swiping Up':
                            pag.press('up')

                        if classe == 'Swiping Down':
                            pag.press('down')

                    if "VLC" in win.GetWindowText(win.GetForegroundWindow()):
                        print("-----------------------VLC-----------------------")
                        if classe == 'Stop Sign':
                            pag.press('space')

                        if classe == 'Swiping Left':
                            pag.hotkey('ctrl', 'right')

                        if classe == 'Swiping Right':
                            pag.hotkey('ctrl', 'left')

                        if classe == 'Swiping Up':
                            pag.hotkey('ctrl', 'up')

                        if classe == 'Swiping Down':
                            pag.hotkey('ctrl', 'down')

                        #if classe == 'Zooming Out With Full Hand':
                        #    player = vlc.MediaPlayer()
                        #    player.audio_set_mute(audio_get_mute())

                    if "Teams" in win.GetWindowText(win.GetForegroundWindow()):

                        if classe == 'Zooming In With Full Hand':
                            pag.hotkey('ctrl', 'shift', 'm')

                        if classe == 'Stop sign':
                            pag.hotkey('ctrl', 'shift', 'd')

                    if "Камера" or "Camera" in win.GetWindowText(win.GetForegroundWindow()):

                        if classe == 'Stop sign':
                            pag.press('space')

                    if "Zoom" in win.GetWindowText(win.GetForegroundWindow()):

                        if classe == 'Zooming In With Full Hand':
                            pag.hotkey('ctrl', 'shift', 'm')

                        if classe == 'Stop sign':
                            pag.hotkey('ctrl', 'shift', 'd')

                        if classe == 'Swiping Down':
                            pag.hotkey('alt', 'a')


            if len(preds) >= 10:
                preds = preds[8:9]

        to_predict = []
        print(classe)
        font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, classe, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0.5, 0.5),1,cv2.LINE_AA)

    cv2.imshow('Q', q)
    cv2.imshow('Hand Gesture Recognition',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()