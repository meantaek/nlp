#!/usr/bin/env python

'''
Script to build neural network based on Roth and Li data for question classification
'''

import io
from collections import Counter
from keras.layers import Embedding, LSTM, Dense, Conv1D, MaxPooling1D, Dropout, Activation
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras import utils
import numpy as np
from sklearn.preprocessing import LabelBinarizer, LabelEncoder
import pickle

#read in the training and testing data
train = io.open('question_train.txt', 'r', encoding='latin-1')
test = io.open('question_test.txt', 'r', encoding='latin-1')
train = train.readlines()
test = test.readlines()

#extract question classification and plain text
train_q_type = []
train_text = []

for i in range(0,len(train)):
  #extract the labels and text
  train_typ = train[i].split(' ', 1)[0]
  train_txt = train[i].split(' ', 1)[1]

  #append to train and test lists
  train_q_type.append(train_typ)
  train_text.append(train_txt)

#repeat process for testing data
test_q_type = []
test_text = []
for i in range(0, len(test)):
  test_typ = test[i].split(' ', 1)[0]
  test_txt = test[i].split(' ', 1)[1]

  test_q_type.append(test_typ)
  test_text.append(test_txt)

#tokenize and count the words
train_text = ''.join(train_text)
test_text = ''.join(test_text)
train_text = train_text.splitlines()
test_text = test_text.splitlines()

tokenizer = Tokenizer(num_words=10000, char_level=False)
tokenizer.fit_on_texts(train_text)
x_train = tokenizer.texts_to_matrix(train_text)
x_test = tokenizer.texts_to_matrix(test_text)

#convert labels to numbers
encoder = LabelEncoder()
encoder.fit(train_q_type)
y_train = encoder.transform(train_q_type)
y_test = encoder.transform(test_q_type)
num_classes = np.max(y_train) + 1
y_train = utils.to_categorical(y_train, num_classes)
y_test = utils.to_categorical(y_test, num_classes)

print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)
print('y_train shape:', y_train.shape)
print('y_test shape:', y_test.shape)

#create model
batch_size = 40
epochs = 3
model = Sequential()
model.add(Dense(512, input_shape=(10000,)))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

#fit model
model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_split=0.1)
#evaluate model
score = model.evaluate(x_test, y_test, batch_size=batch_size,verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])

#export the model
with open("simp_tokenizer.pickle", 'wb') as f:
  pickle.dump(tokenizer, f)
with open("simp_encoder.pickle", 'wb') as d:
  pickle.dump(encoder, d)
model.save("simp_q_classify_model.hdf5")
