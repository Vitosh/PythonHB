from music import *
import unittest
import json


class Tests(unittest.TestCase):

    def setUp(self):
        self.newSong1 = Songs(
            "Blue Marry", "Unknown Artist", "Unknown Album", "1:03:10")
        self.newSong2 = Songs(
            "Red Marry", "Unknown Artist2", "Unknown Album2", "09:42")
        self.newSong3 = Songs(
            "Funky Marry", "RealThing", "Unknown Album3", "1:42")
        self.code_songs = Playlist(name="Code", repeat=True, shuffle=True)
        self.code_songs.add_song(self.newSong1)
        self.code_songs.add_song(self.newSong2)
        self.code_songs.add_song(self.newSong3)

    def tearDown(self):
        pass

    def test_title(self):
        self.assertEqual(self.newSong1.title(), "Blue Marry")

    def test_artist(self):
        self.assertEqual(self.newSong2.artist(), "Unknown Artist2")

    def test_album(self):
        self.assertEqual(self.newSong3.album(), "Unknown Album3")

    def test_length_sec(self):
        self.assertEqual(
            self.newSong1.length(seconds=True, minutes=True), 3790)

    def test_length_min(self):
        self.assertEqual(self.newSong1.length(minutes=True, hours=True), 63)

    def test_length_hours(self):
        self.assertEqual(self.newSong1.length(hours=True), 1)

    def test_length_sec_twoDigits(self):
        self.assertEqual(self.newSong2.length(seconds=True, minutes=True), 582)

    def test_length_min_twoDigits(self):
        self.assertEqual(self.newSong2.length(minutes=True, hours=True), 9)

    def test_length_hours_twoDigits(self):
        self.assertEqual(self.newSong2.length(hours=True), 0)

    def test_length_general(self):
        self.assertEqual(self.newSong1.length(False, False, False), "1:03:10")

    def test_str(self):
        self.assertEqual(
            str(self.newSong3), "Funky Marry - RealThing from Unknown Album3 - 1:42")

    def test_eq(self):
        self.assertFalse(self.newSong3 == self.newSong2)

    def test_song_added(self):
        self.assertTrue(
            self.code_songs.__str__() == self.code_songs.__repr__())

    def test_remove_song(self):
        self.code_songs.remove_song(self.newSong2)
        self.assertFalse(self.newSong2 in self.code_songs.show_playlist())

    def test_the_other_song_is_there(self):
        self.assertTrue(self.newSong2 in self.code_songs.show_playlist())

    def test_the_total_length(self):
        self.assertTrue(self.code_songs.total_length() == "01:14:34")

    def test_artists_histogram(self):
        self.newSong31 = Songs(
            "Funky Marry 2", "RealThing", "Unknown Album3", "1:42")
        self.newSong32 = Songs(
            "Funky Marry 3", "RealThing", "Unknown Album3", "1:42")
        self.newSong33 = Songs(
            "Funky Marry 4", "RealThing", "Unknown Album3", "1:42")

        self.code_songs.add_song(self.newSong33)
        self.code_songs.add_song(self.newSong32)
        self.code_songs.add_song(self.newSong31)


if __name__ == '__main__':
    unittest.main()
