from django.db import models


class Toy(models.Model):
    """Create the toy object."""
    name = models.CharField(max_length=150, db_index=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=150, blank=False, default="")
    release_date = models.DateTimeField(auto_now_add=True)
    included_at_home = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
