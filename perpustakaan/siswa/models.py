from django.db import models

from django.db import models

class Buku(models.Model):
    judul = models.CharField(max_length=100)
    penulis = models.CharField(max_length=100)

    def __str__(self):
        return self.judul