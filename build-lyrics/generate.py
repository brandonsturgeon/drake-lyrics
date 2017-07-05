from bs4 import BeautifulSoup
import requests

class GenerateLyrics:
    def __init__(self):
        self.base_album_url = 'https://genius.com/albums/Drake/{}'
        self.album_names = [
            'Room-for-improvement',
            'Comeback-season',
            'Born-successful',
            'Dead-perspective',
            'So-far-gone',
            'So-far-gone-ep',
            'AM-pm-series',
            'Thank-me-later',
            'Young-sweet-jones-2',
            'Take-care',
            'Nothing-was-the-same',
            'If-you-re-reading-this-it-s-too-late',
            'Ovo-sound-radio-tracklists',
            'Views',
            'More-life'
        ]

        self.get_tracks_for_album('Views')

    def get_tracks_for_album(self, album_name):
        url = self.get_album_url(album_name)
        doc = requests.get(url, verify=False)
        soup = BeautifulSoup(doc.text, 'lxml')

        tracks = soup.find_all('album-tracklist-row')
        for track in tracks:
            container = track.div
            row_content = container.find('div', 'char_row-content')
            url = row_content.a
            print url

    def main(self):
        self.get_tracks_for_album('Views')

    def get_album_url(self, album_name):
        return self.base_album_url.format('Views')
        #return self.base_album_url.format(album_name)

if __name__ == '__main__':
    GenerateLyrics()
