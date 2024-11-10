from django.db import models

class Car(models.Model):

    brand = models.CharField(max_length=50, verbose_name='Brand')
    model = models.CharField(max_length=50, verbose_name='Model')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    color = models.CharField(max_length=30, verbose_name='Color')
    engine_capacity = models.PositiveIntegerField(verbose_name='Engine Capacity (cc)')
    power = models.PositiveIntegerField(verbose_name='Power (HP)')

    def __str__(self):
        return f"{self.brand} {self.model} {self.price}"

    class Meta:
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
