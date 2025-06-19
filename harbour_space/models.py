from django.db import models


# Create your models here.
class StorageServer(models.Model):
    address = models.CharField(max_length=255)


class File(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Chunk(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name="chunks")
    index = models.IntegerField()
    storage_servers = models.ManyToManyField(StorageServer)
    checksum = models.CharField(max_length=64, blank=True)
