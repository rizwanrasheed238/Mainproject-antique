from django.db import models
from antiqueapp.models import Account




# Create your models here.
class seller_product(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    name=models.CharField(max_length=250,unique=True)
    descripton = models.TextField(blank=True)
    price=models.FloatField(default=0)
    category=models.CharField(max_length=250)
    stock=models.IntegerField(default=1)
    image=models.ImageField()


    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name


def __str__(self):
    return '{}'.format(self.name)
