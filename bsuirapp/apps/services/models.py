from django.db import models


# Create your models here.

class ServiceType(models.Model):
    title = models.CharField('Названия типа услуги', max_length=100)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип услуги'
        verbose_name_plural = 'Типы услуг'


class Service(models.Model):
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE)
    title = models.CharField('Название услуги', max_length=100)
    price = models.FloatField('Стоимость услуги')
    LINEAR = 'п.м.'
    SQUARE = 'м²'
    MEASUREMENT_TYPE_CHOICES = [
        (LINEAR, 'п.м.'),
        (SQUARE, 'м²')
    ]
    measure_type = models.CharField(
        max_length=5,
        choices=MEASUREMENT_TYPE_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
