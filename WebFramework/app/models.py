"""
Definition of models.
"""

from django.db import models

class kSpotValueModel(models.Model):

    date = models.IntegerField(primary_key=True)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    sharesTraded = models.IntegerField()
    turnover = models.FloatField()

    class Meta:
        db_table = "SpotValueOfNifty"

    def __str__(self):
        return str(self.date)

class kOptionValueModel(models.Model):

    date = models.IntegerField()
    optionType = models.CharField(max_length=2)
    strikePrice = models.FloatField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    noOfContracts = models.IntegerField()
    turnOver = models.FloatField()
    openInterest = models.IntegerField()
    changeInOI = models.IntegerField()

    class Meta:
        db_table = "OptionValueOfNiftyJan2018"

    def __str__(self):
        return str(self.date) + self.optionType + str(self.strikePrice)
