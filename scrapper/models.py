from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    """
    Page model
    """

    user = models.ForeignKey(User, related_name="pages", on_delete=models.CASCADE)
    name = models.CharField(max_length=5096, blank=True, null=True)
    total_links = models.CharField(max_length=100, blank=True, null=True)
    page_link = models.URLField(max_length=5096)

    class Meta:
        unique_together = ("user", "page_link")

    def __str__(self):
        return self.name or self.page_link


class Link(models.Model):
    """
    Link model
    """

    page = models.ForeignKey(Page, related_name="links", on_delete=models.CASCADE)
    name = models.TextField(max_length=5096, blank=True, null=True)
    link = models.URLField(max_length=5096)

    def __str__(self):
        return self.name or self.link
