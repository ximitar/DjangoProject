import random
import string

from typing import Any
from django.core.management.base import BaseCommand
from web.models import Room, User


def generate_random_name(length=8):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        user = User.objects.first()
        for i in range(30):
            password = generate_random_password()
            name = generate_random_name()
            room = Room.objects.create(
                room_name=name,
                password=password,
                creator=user,
            )
            room.participants.add(user)
