from django.db import models


class Link(models.Model):

    url = models.TextField()
    short_url = models.TextField(blank=True)
    view_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'link'

