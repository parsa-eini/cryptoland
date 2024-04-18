from django.db import models


class AbstractTime(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    last_modified_date = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
