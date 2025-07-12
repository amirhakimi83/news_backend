from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class News(models.Model):
    title = models.CharField(max_length=200)
    content_news = models.TextField()
    tags = models.ManyToManyField(Tag)
    reference = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.title}"