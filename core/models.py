from django.contrib.auth import get_user_model
from django.db import models
from nursury.models import Plant

User = get_user_model()


class OrderDetails(models.Model):
    plant = models.ForeignKey(
        to=Plant,
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(
        decimal_places=3,
        max_digits=19,
        default=1,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.quantity} of {self.plant}"

    def save(self, *args, **kwargs):
        self.price = self.plant.price * self.quantity
        super().save(*args, **kwargs)


class Order(models.Model):
    placed_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="placed_by"
    )
    details = models.ManyToManyField(
        to=OrderDetails,
        related_name="details"
    )
    completed = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    ordered_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.placed_by} order"
