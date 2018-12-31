from django.db import models

# Create your models here.

class kOptionValueFormModel(models.Model):
    optionStock = models.CharField(max_length=256)
    expiryMonth = models.CharField(max_length=3)
    expiryYear = models.IntegerField()

    class Meta:
        db_table = "OptionValueFormModel"