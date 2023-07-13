import random
import string
import urllib.request

from django.conf import settings


def build_generator():
    url = settings.TODOS_URL
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8-sig')
    text = data.lower().translate(str.maketrans("", "", string.punctuation))
    words = text.split()

    pairs = {}
    for i in range(len(words) - 1):
        pair = (words[i], words[i + 1])
        if pair not in pairs:
            pairs[pair] = []
        if len(words) > i + 2:
            pairs[pair].append(words[i + 2])
    return pairs


def generate_text(generator, length):
    seed = random.choice(list(generator.keys()))
    words = list(seed)
    for i in range(length):
        try:
            next_word = random.choice(generator[seed])
            words.append(next_word)
            seed = (seed[1], next_word)
        except KeyError:
            break
    return ' '.join(words)
