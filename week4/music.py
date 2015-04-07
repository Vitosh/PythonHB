import random


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

    def length(self, seconds=False, minutes=False, hours=False):
        sTotal = self.__length.split(":")

        if seconds:
            if len(sTotal) == 3:
                iHours = int(sTotal[0]) * 3600
                iMinutes = int(sTotal[1]) * 60
                iSeconds = int(sTotal[2])
                return iHours + iMinutes + iSeconds

            iMinutes = int(sTotal[0]) * 60
            iSeconds = int(sTotal[1])
            return iMinutes + iSeconds

        if minutes:
            if len(sTotal) == 3:
                iHours = int(sTotal[0]) * 60
                iMinutes = int(sTotal[1])
                return iHours + iMinutes

            iMinutes = int(sTotal[0])
            return iMinutes

        if hours:
            if len(sTotal) == 3:
                iHours = int(sTotal[0])
                return iHours
            return 0

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
        self.__musicByOrder = []
        self.__name = name
        self.__repeat = repeat
        self.__shuffle = shuffle
        self.__played = []
    
    def artists(self):
        self.__histogram = {}
        for song in self.__music:
            self.__histogram[song.artist()] = 0

        for song in self.__music:
            self.__histogram[song.artist()] += 1

        return self.__histogram

    def total_length(self):
        iSeconds = 0
        for song in self.__music:
            iSeconds += song.length(seconds=True)
        iMinutes = iSeconds // 60
        iHours = iMinutes // 60
        return "%02d:%02d:%02d" % (iHours, iMinutes % 60, iSeconds % 60)

    def show_playlist(self):
        return self.__music

    def add_song(self, song):
        if song in self.__music:
            raise SongAlreadyPresent
        self.__music[song] = [str(song)]

    def remove_song(self, song):
        if song not in self.__music:
            raise SongIsNotPresent
        del self.__music[song]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.__music)
