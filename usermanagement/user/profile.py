import os
from PIL import Image
from .models import Profile


def size_compress(user):
    user_profile = Profile.objects.get(user=user)
    path = user_profile.photo.path
    img = Image.open(path)
    size_in_byte = os.path.getsize(path)
    if size_in_byte > 1000000:
        img.save(path, optimize=True, quality=10)