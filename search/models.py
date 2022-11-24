from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    handle = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    email = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name + ' : ' + self.email
