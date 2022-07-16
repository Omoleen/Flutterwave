# from django.db import models
#
#
# class Transaction(models.Model):
#     ID = models.CharField(primary_key=True, max_length=11, unique=True)
#     Amount = models.FloatField()
#     Currency = models.CharField(max_length=10)
#     CustomerEmail = models.EmailField()
#     Balance = models.FloatField(null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.ID}'
#
#
# class SplitInfo(models.Model):
#     Transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='SplitInfo', blank=True)
#     SplitType = models.CharField(choices=(('FLAT', 'FLAT'),
#                                           ('PERCENTAGE', 'PERCENTAGE'),
#                                           ('RATIO', 'RATIO')), max_length=25)
#     SplitValue = models.FloatField()
#     SplitEntityId = models.CharField(max_length=20)
#     Amount = models.FloatField(null=True, blank=True)
#
#     def __str__(self):
#         return f'{self.Transaction}'
