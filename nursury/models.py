from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image

User = get_user_model()

class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="plant_images/")
    price = models.DecimalField(decimal_places=3, max_digits=19)

    def __str__(self):
        return self.name