from flask import Flask, send_from_directory, render_template, url_for, request
import os
import pickle
import profanityfilter
from random import choice

app = Flask(__name__)
lyrics_file = './all_lyrics.txt'

# Placeholder in case unpickling takes too long
lyrics = ['yeah', 'yeah', 'yeah']
with open(lyrics_file, 'rb') as lyric_file:
    lyrics = pickle.load(lyric_file)

def get_lyric(sfw = False):
    chosen_lyric = choice(lyrics)

    if sfw:
        chosen_lyric = profanityfilter.censor(chosen_lyric)
    return chosen_lyric

@app.route('/')
def random_lyric():
    sfw = bool(request.args.get('sfw'))

    chosen_lyric = get_lyric(sfw)
    lyric_lines = chosen_lyric.split('\n')

    return render_template('lyrics.html', lyric_lines=lyric_lines)+'\n'

@app.route('/lyric')
def api_lyric():
    sfw = bool(request.args.get('sfw'))

    return get_lyric(sfw)+'\n'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
