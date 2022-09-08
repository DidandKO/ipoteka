from django.db import models


class BankOffer(models.Model):

    bank_name = models.CharField(max_length=63)
    min_mortgage_rate = models.FloatField(null=True)
    max_mortgage_rate = models.FloatField(null=True)
    term_min = models.IntegerField(null=True)
    term_max = models.IntegerField(null=True)
    price_min = models.IntegerField(null=True)
    price_max = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.bank_name}: ставка {self.min_mortgage_rate}-{self.max_mortgage_rate}'

