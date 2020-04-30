from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse('products:index_by_category',
                       args=[self.slug])

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category,
    related_name='products',
    on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    LINEAR = 'п.м.'
    SQUARE = 'м²'
    UNIT = 'ед.'
    MEASUREMENT_TYPE_CHOICES = [
        (LINEAR, 'п.м.'),
        (SQUARE, 'м²'),
        (UNIT, 'ед.')
    ]
    measure_type = models.CharField(
        max_length=5,
        choices=MEASUREMENT_TYPE_CHOICES
    )
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('products:product_detail',
                       args=[self.id, self.slug])

    def get_short_description(self):
        return self.description[:100] + '... '

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
