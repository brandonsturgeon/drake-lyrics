from bs4 import BeautifulSoup, Tag, NavigableString
import pickle
import requests

class GenerateLyrics:
    def __init__(self):
        self.lyrics_file_name = "all_lyrics.txt"

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
            'Views',
            'More-life'
        ]

        self.exclude_track_words = [
            'booklet',
            'trailer',
            'credits'
        ]

        self.lyrics = []

        self.main()


    def main(self):
        for album in self.album_names:
            tracks = self.get_tracks_for_album(album)

            for track in tracks:
                lyrics = self.get_lyrics_for_track(track)

                for lyric in lyrics:
                    if lyric not in self.lyrics:
                        self.lyrics.append(lyric)

        with open(self.lyrics_file_name, 'wb') as save_file:
            pickle.dump(self.lyrics, save_file)


    @staticmethod
    def get_soup_from_url(url):
        doc = requests.get(url, verify=False)
        return BeautifulSoup(doc.text, 'lxml')

    @staticmethod
    def lyric_is_valid(lyric):
        validations = [
            '[' not in lyric,
            lyric is not u'',
            lyric is not None
        ]
        return all(validations)

    def get_lyrics_for_track(self, track_url):
        soup = self.get_soup_from_url(track_url)

        lyric_div = soup.find('div', {'class': 'lyrics'})

        # The a tags contain lyric blocks, or fragments
        a_tags = lyric_div.find_all('a')

        # Get all lyrics which have been commented on
        lyric_fragments = []
        for tag in a_tags:
            spread = tag.text.split("\n")
            fold = []

            # Sometimes there are unacceptable lines in the fragments which we need to remove
            # so we're going to rebuild the fragment containing only what we want
            for line in spread:
                stripped_line = line.strip()
                if self.lyric_is_valid(stripped_line):
                    fold.append(stripped_line)

            fold = "\n".join(fold)

            lyric_fragments.append(fold)

        loose_lyrics = []
        # Get all lyrics which have not been commented on
        for child in lyric_div.children:
            if type(child) == Tag:
                # lyric_div contains many children, only the Tag child has lyrics in it
                for loose_lyric in child.children:
                    # We're only looking for loose lyrics inside of NavigableStrings
                    if type(loose_lyric) == NavigableString:
                        stripped_loose_lyric = loose_lyric.strip()
                        if self.lyric_is_valid(stripped_loose_lyric):
                            loose_lyrics.append(stripped_loose_lyric)

        # All together, now
        combined_lyrics = lyric_fragments + loose_lyrics

        return combined_lyrics

    def get_tracks_for_album(self, album_name):
        url = self.get_album_url(album_name)
        soup = self.get_soup_from_url(url)

        track_list = soup.find_all('div', {'class': 'chart_row-content'})
        all_links = [track.a['href'] for track in track_list]

        # Get all links which don't include excluded words
        links = [link for link in all_links if all([word not in link for word in self.exclude_track_words])]

        return links

    def get_album_url(self, album_name):
        return self.base_album_url.format(album_name)

if __name__ == '__main__':
    GenerateLyrics()
