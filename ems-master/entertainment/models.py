from django.db import models
from django.db.models.query import QuerySet
from django.db.models import OuterRef, Subquery
from django.test import TestCase


# Group all Playlists by user id filter Playlists using user id and get their length and return the sum over the agreegation that we implemented in PlaylistQuerySet
class UserQuerySet(QuerySet):
    @classmethod
    def playlists_total_length(cls):
        playlist_annotation = PlaylistQuerySet.songs_total_length()
        
        queryset = Playlist.objects.values('user__id').filter(user__id=OuterRef('id')).values_list(Sum(playlist_annotation))
        return Subquery(queryset=queryset, output_field=IntegerField())

    def collect(self):
        return self.annotate(_playlists_total_length = self.playlists_total_length())

class User(models.Model):
    name = models.CharField(max_length = 200)

    def playlists_total_length(self):
        return sum([p.songs_total_length for p in self.playlists.all()])

    def __str__(self):
        return self.name

#Group all songs and make the agreegation
class PlaylistQuerySet(QuerySet):
    @classmethod
    def songs_total_length(cls):
        queryset = Song.objects.values('playlist__id').filter(playlist__id=OuterRef('id')).values_list(Sum('length'))

        return Subquery(queryset=queryset, output_field=models.IntegerField())

class Playlist(models.Model):
    objects = PlaylistQuerySet.as_manager()
    user = models.ForeignKey(User, related_name = 'playlists', on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)

    # @property
    # def songs_total_length(self):
    #     total_length = 0
    #     for song in self.songs.all():
    #         total_length += song.length
    #     return total_length
    @property
    def songs_total_length(self):
        if hasattr(self, 'songs_total_length'):
            return self._songs_total_length
        return sum([song.length for song in self.songs.all()])

    def __str__(self):
        return self.name

class Song(models.Model):
    playlist = models.ForeignKey(Playlist, related_name = 'songs', on_delete=models.CASCADE)
    title = models.CharField(max_length = 200)
    length = models.PositiveIntegerField()

    def real_length(self):
        if hasattr(self, '_real_length'):
            return self._real_length
        return self.length * 0.8

    def __str__(self):
        return self.title        

class SongTests(TestCase):
    def test_song_length(self):
        length = 120
        real_length = 0.8 * length
        song = Song.objects.create(title = 'PythonDjangoTest', length=120)
        self.assertEqual(real_length, song.real_length)


