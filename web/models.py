from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()


class Movie(models.Model):
    movie_name = models.CharField(max_length=256)
    gener = models.CharField(max_length=256)


class Room(models.Model):
    room_name = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    movie_id = models.ManyToManyField(Movie)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        User, through='RoomParticipant', related_name='rooms_participated', blank=True)


class RoomParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
