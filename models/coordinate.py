from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Coordinate(models.Model):
    x = models.IntegerField(0)
    y = models.IntegerField(0)
    carrier = models.ForeignKey(to='Carrier', on_delete=models.CASCADE, default=None, blank=True, null=True)
    destroyer = models.ForeignKey(to='Destroyer', on_delete=models.CASCADE, default=None, blank=True, null=True)
    frigate = models.ForeignKey(to='Frigate', on_delete=models.CASCADE, default=None, blank=True, null=True)
    submarine = models.ForeignKey(to='Submarine', on_delete=models.CASCADE, default=None, blank=True, null=True)

    # tag = models.SlugField()
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    #
    # def __str__(self):
    #     return self.tag


    #class Meta:
    #    abstract = True
