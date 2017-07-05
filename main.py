from flask import Flask
import pickle
from random import choice

app = Flask(__name__)
lyrics_file = './build-lyrics/all_lyrics.txt'

lyrics = ['yeah     ']
with open(lyrics_file, 'rb') as lyric_file:
    lyrics = pickle.load(lyric_file)

@app.route('/')
def random_lyric():
    return choice(lyrics)

@app.route('/all_lyrics')
def all_lyrics():
    return str(lyrics)
