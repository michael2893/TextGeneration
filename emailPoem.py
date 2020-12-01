def email_poem(model):
    # Evaluation step (generating text using the learned model)
# Evaluation step (generating text using the learned model)
    epoch = 59
    poem = 0
    
    for i in range(0,1):
        poem = i
        start_index = random.randint(0, len(text) - maxlen - 1)
        generated_text = text[start_index: start_index + maxlen]
        print(generated_text)
        temperature = 1
        #print(generated_text)
        for i in range(100):
            sampled = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(generated_text):
                sampled[0, t, char_indices[char]] = 1.
            preds = model.predict(sampled, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = chars[next_index]
            generated_text += next_char
            generated_text = generated_text[1:]
           # sys.stdout.write(next_char)
    return generated_text