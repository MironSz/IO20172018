from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(User):
    class Meta:
        proxy = True

class Domain(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return "{}".format(self.name)


class Comment(models.Model):
    time = models.DateTimeField()

class Word(models.Model):
    word = models.CharField(max_length=30, unique=True)

class WordOccurence(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    place = models.IntegerField()
    word = models.ForeignKey(Word, on_delete=models.CASCADE)


def date_filter(query_set, time_begin, time_end):
    return query_set.filter(time_gte=time_begin, time__lte=time_end)

class WordQuery(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    time = models.DateTimeField()
    word = models.CharField(max_length=200)
    
    @staticmethod
    def count():
        return WordQuery.objects.count()

    @staticmethod
    def interval(time_begin, time_end):
        return date_filter(WordQuery.objects, time_begin, time_end)

    def one_interval(self, time_begin, time_end):
        return date_filter(WordQuery.objects.get(word=self.word), time_begin, time_end)