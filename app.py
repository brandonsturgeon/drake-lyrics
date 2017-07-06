from flask import Flask, send_from_directory, render_template, url_for
import os
import pickle
from random import choice

app = Flask(__name__)
lyrics_file = './all_lyrics.txt'

# Placeholder in case unpickling takes too long
lyrics = ['yeah', 'yeah', 'yeah']
with open(lyrics_file, 'rb') as lyric_file:
    lyrics = pickle.load(lyric_file)

@app.route('/')
def random_lyric():
    chosen_lyric = choice(lyrics)
    lyric_lines = chosen_lyric.split('\n')
    return render_template('lyrics.html', lyric_lines=lyric_lines)+'\n'

@app.route('/lyric')
def api_lyric():
    return choice(lyrics)+'\n'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
