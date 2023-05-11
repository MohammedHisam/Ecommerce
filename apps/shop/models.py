from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
class Categories(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('product_category', args=[self.slug])

    def __str__(self):
        return '{}'.format(self.name)


class Fruits(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    img = models.ImageField(upload_to='fruits')
    desc = models.TextField()
    stock = models.IntegerField()
    available = models.BooleanField()
    price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'fruit'
        verbose_name_plural = 'fruits'

    def get_url(self):
        return reverse('details', args=[self.category.slug, self.slug])

    def __str__(self):
        return '{}'.format(self.name)
