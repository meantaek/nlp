from keras.models import load_model
from keras.layers import Embedding, LSTM, Dense, Conv1D, MaxPooling1D, Dropout, Activation
from keras.models import Sequential
import numpy as np
import pickle
import os


class QuestionClassifierService():
    """ """
    def __init__(self):

        # open the saved model with encoded labels and tokenizer
        with open(os.path.abspath("./configs/simp_tokenizer.pickle"), 'rb') as f:
            self.tokenizer = pickle.load(f)
        with open(os.path.abspath("./configs/simp_encoder.pickle"), 'rb') as d:
            self.encoder = pickle.load(d)

        model = Sequential()
        model.add(Dense(512, input_shape=(10000,)))
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.encoder.classes_)))
        model.add(Activation('softmax'))

        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        model.load_weights(os.path.abspath("./configs/simp_q_classify_weights.h5"))
        self.model = model

    def classify(self, sentence):
        #new question to predict the question type on
        newtext = [sentence.plaintext]

        #tokenize and retreive types
        newtext = self.tokenizer.texts_to_matrix(newtext)
        text_labels = self.encoder.classes_

        #make prediction and output
        predictions = self.model.predict(np.array(newtext))
        label = text_labels[np.argmax(predictions)]
        return label


QuestionClassifier = QuestionClassifierService()
