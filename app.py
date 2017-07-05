from flask import Flask, send_from_directory
import pickle
from random import choice

app = Flask(__name__)
lyrics_file = './all_lyrics.txt'

lyrics = ['yeah     ']
with open(lyrics_file, 'rb') as lyric_file:
    lyrics = pickle.load(lyric_file)

@app.route('/')
def random_lyric():
    return choice(lyrics)+'\n'

@app.route('/all_lyrics')
def all_lyrics():
    return str(lyrics)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
