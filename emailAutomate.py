#!/usr/bin/env python37

import numpy as np
import pandas as pd 


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule
import time

import tensorflow as tf
import os


path = 'convo.txt'
#Explore the data
text = open(path, "r").read()


maxlen = 60
step = 3
sentences = []
next_chars = []
for i in range(0, len(text)-maxlen, step):
    sentences.append(text[i:i+maxlen])
    next_chars.append(text[i+maxlen])


chars = sorted(list(set(text)))
vocab_len = len(chars)


char_indices = dict((char, chars.index(char)) for char in chars)
char_indices

x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)


for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        x[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1

from tensorflow.keras import layers
model = tf.keras.models.Sequential()
model.add(layers.LSTM(128, input_shape=(maxlen, vocab_len)))

model.add(layers.Dense(vocab_len, activation="softmax"))



model.summary()


model.compile(loss="categorical_crossentropy", optimizer="adam")



def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

import random
import sys
for epoch in range(0, 60):
    print("Epoch ", epoch)
    f = open("epoch_{}.txt".format(epoch), "w")
    f.write("Epoch {}\n".format(epoch))
    model.fit(x,y, batch_size=128)
    start_index = random.randint(0, len(text) - maxlen - 1)
    generated_text = text[start_index: start_index + maxlen]
    print('--- Generating with seed: "' + generated_text + '"')
    f.write("Seed {}\n".format(generated_text))
    for temperature in [0.2, 0.5, 1.0, 1.2]:
        print('------ temperature:', temperature)
        f.write("Temperature {}\n".format(temperature))
        #print(generated_text)
        for i in range(400):
            sampled = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(generated_text):
                sampled[0, t, char_indices[char]] = 1.
            preds = model.predict(sampled, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = chars[next_index]
            generated_text += next_char
            generated_text = generated_text[1:]
           # sys.stdout.write(next_char)
            f.write(next_char)
    f.close()


# def generate_text(model):
#     # Evaluation step (generating text using the learned model)
# # Evaluation step (generating text using the learned model)
#     epoch = 59
#     poem = 0
    
#     for i in range(0,2):
#         poem = i
#         f = open("poem_{}.txt".format(poem), "w")
#         f.write("Poem {}\n".format(poem))
#         start_index = random.randint(0, len(text) - maxlen - 1)
#         generated_text = text[start_index: start_index + maxlen]
#         print(generated_text)
#         f.write(generated_text)
#         temperature = 1
#         #print(generated_text)
#         for i in range(100):
#             sampled = np.zeros((1, maxlen, len(chars)))
#             for t, char in enumerate(generated_text):
#                 sampled[0, t, char_indices[char]] = 1.
#             preds = model.predict(sampled, verbose=0)[0]
#             next_index = sample(preds, temperature)
#             next_char = chars[next_index]
#             generated_text += next_char
#             generated_text = generated_text[1:]
#            # sys.stdout.write(next_char)
#             f.write(next_char)
#     f.close()    
   




def send_mail():

	fromaddr = "dailymeditationsforyou@gmail.com"
	recip = ["amt2893@gmail.com, blaqnbloo@gmail.com"]
	msg = MIMEMultipart()

	msg['From'] = fromaddr
	msg['To'] = ", ".join(recipients)
	msg['Subject'] = "Todays's Poem"

	body = email_poem(model)

	msg.attach(MIMEText(body, 'plain'))




	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "msjwgytvodndaabb")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()


def job():
    print("I'm working...")
    send_mail()

schedule.every().day.at("8:30").do(job)
schedule.every().day.at("12:30").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)	




