import requests


class Songs:

    def __init__(self, title, artist, album, length):
        self.__title = title
        self.__artist = artist
        self.__album = album
        self.__length = length

    def title(self):
        return self.__title

    def artist(self):
        return self.__artist

    def album(self):
        return self.__album

    def length(self, seconds=False):
        if seconds:
            sSeconds = self.__length.split(":")
            iMinutes = int(sSeconds[0]) * 60
            iSeconds = int(sSeconds[1])
            return iMinutes + iSeconds
        return self.__length

    def __str__(self):
        return "{} - {} from {} - {}".format(self.__title, self.__artist, self.__album, self.__length)

    def __eq__(self, other):
        return self.__title == other.__title and self.__artist == other.__artist and self.__album == other.__album

    def __hash__(self):
        return hash(str(self))


class MusicException(Exception):
    pass


class SongAlreadyPresent(MusicException):

    def __init__(self, value='The Song is already present, it cannot be added.'):
        self.value = value

    def __str__(self):
        return repr(self.value)


class SongIsNotPresent(MusicException):

    def __init__(self, value='The Song is not present, it cannot be removed.'):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Playlist:

    def __init__(self, name, repeat=False, shuffle=False):
        self.__music = {}
        self.__name = name
        self.__repeat = repeat
        self.__shuffle = shuffle

    def add_song(self, song):
        if song in self.__music:
            raise SongAlreadyPresent
        self.__music[song] = [str(song)]

    def remove_song(self, song):
        if song not in self.__music:
            raise SongIsNotPresent
        iIndex = self.__music.index(song)
        self.__music.pop(iIndex)

    def __repr__(self):
        return str(self.__music)

newSong1 = Songs("Blue Marry", "Unknown Artist", "Unknown Album", "3:42")
newSong2 = Songs("Red Marry", "Unknown Artist2", "Unknown Album2", "13:42")
newSong3 = Songs("Funky Marry", "Unknown Artist3", "Unknown Album3", "1:42")

print(str(newSong1))
print(newSong1.length(True))
print(newSong1.length())

code_songs = Playlist(name="Code", repeat=True, shuffle=True)
code_songs.add_song(newSong1)
code_songs.add_song(newSong2)
code_songs.add_song(newSong3)
print(code_songs)
code_songs.remove_song(newSong2)
print(code_songs)
