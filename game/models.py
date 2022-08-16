from django.db import models


class Quote(models.Model):
    source = models.CharField(max_length=150)
    text = models.TextField(max_length=1000)
    tags = models.TextField(max_length=500)
    lang = models.CharField(max_length=7, default='en')

    def __str__(self):
        return f'"{self.text}" — {self.source}'
