import json
import nltk
import random 
import pickle
import numpy as np 
import tensorflow as tf 
from tensorflow.keras.models import load_model


class Chatbot:
# A basic chatbot built using tensorflow and nltk. It saves the models to a pickle file, and 
# --------------------------------------------------------------------------------------------
# loads the model if it has been trained already.

    def __init__(self):
        self.lemmatizer = nltk.stem.WordNetLemmatizer()
        
        with open('intents.json') as file_:
            intents_file = file_.read()

        self.intents = json.loads(intents_file)
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_char = ['!', '?', '.', ',']
        self.model = None

    def preprocess(self):
        try:
            with open('data.pickle', 'rb') as f:
                print("data has already been processed")
                self.words, self.classes, self.documents = pickle.load(f)
        
         # Tokenize and lemmatize the words for the chatbot
        except:
            print("processing the data...")
            for intent in self.intents['intents']:
                for pattern in intent['patterns']:
                    tokenized = nltk.word_tokenize(pattern)
                    self.words.extend(tokenized)
                    self.documents.append((tokenized, intent['tag']))
                    if intent['tag'] not in self.classes:
                        self.classes.append(intent['tag'])


            self.words = [self.lemmatizer.lemmatize(w.lower()) for w in self.words if w not in self.ignore_char]
            self.words = sorted(list(set(self.words)))
            self.classes = sorted(list(set(self.classes)))
            
            with open('data.pickle', 'wb') as f:
                pickle.dump((self.words, self.classes, self.documents), f)
                
    # Training, compiling, and saving the model
    def train_model(self):
        try:
            self.model = load_model('chatbot.h5')
            print("reading model...")
        
        except:
            output_empty = [0]* len(self.classes)
            training = []

            for doc in self.documents:
                bag = []
                tokenized_pattern = doc[0]
                tokenized_pattern = [self.lemmatizer.lemmatize(p.lower()) for p in tokenized_pattern]

                for word in self.words:
                    bag.append(1) if word in tokenized_pattern else bag.append(0)
                
                output_row = output_empty[:]
                output_row[self.classes.index(doc[1])] = 1
                training.append([bag, output_row])
            
            random.shuffle(training)
            training = np.array(training)
            
            train_word = list(training[:,0])
            train_class = list(training[:,1])

            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(units=128, input_shape=(len(train_word[0]),), activation='relu'),
                tf.keras.layers.Dropout(rate=0.5),
                tf.keras.layers.Dense(units=64, activation='relu'),
                tf.keras.layers.Dropout(rate=0.5),
                tf.keras.layers.Dense(units=len(train_class[0]), activation='softmax')
            ])


            self.model.compile(
                optimizer=tf.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )

            history = self.model.fit(
                np.array(train_word),
                np.array(train_class),
                epochs=200,
                batch_size=5, 
                verbose=1
            )
            self.model.save('chatbot.h5', history)
            print("Model created")

    def run_model(self):
        print("Bot activate! (type 'q' to quit)")
        while True:
            inp = input('You: ')
            if inp.lower() == 'q':
                break 
            
            results = self.model.predict(np.array([self.convert_to_bag(inp, self.words)]))
            results_index = np.argmax(results)
            tag = self.classes[results_index]

            for tg in self.intents['intents']:
                if tg['tag'] == tag:
                    responses = tg['responses']
            if responses == ["Alright, let's do it", 'Ok, here it is', 'Buckle your seats', 'Here we go']:
                print(f'Bot:  Product 1 or 2?')
            else:
                print(f'Bot: {random.choice(responses)}')

    def convert_to_bag(self, inp, words):
        bag = [0 for _ in range(len(words))]
        tokenized_pattern = nltk.word_tokenize(inp)
        tokenized_pattern = [self.lemmatizer.lemmatize(w.lower()) for w in tokenized_pattern]

        for pat in tokenized_pattern:
            for i, w in enumerate(words):
                if w == pat:
                    bag[i] = 1 
        
        return np.array(bag)



