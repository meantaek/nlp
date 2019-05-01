from keras.models import load_model
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import pickle

#open the saved model with encoded labels and tokenizer
with open("simp_tokenizer.pickle", 'rb') as f:
  tokenizer = pickle.load(f, encoding='latin-1')
with open("simp_encoder.pickle", 'rb') as d:
  encoder = pickle.load(d, encoding='latin-1')
model = load_model("simp_q_classify_model.hdf5")

#new question to predict the question type on
newtext = ["Who is Confucius ?"]

#tokenize and retreive types
newtext = tokenizer.texts_to_matrix(newtext)
text_labels = encoder.classes_

#make prediction and output
predictions = model.predict(np.array(newtext))
label = text_labels[np.argmax(predictions)]
print(label)
