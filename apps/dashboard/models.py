from django.db import models

class WeekDays(models.Model):
    title = models.CharField(max_length=50)
    day_number = models.IntegerField(null=True)
    def __str__(self):
        return self.title

class Course(models.Model):
    title = models.CharField(max_length=140)
    DURATION = (
        ('30', '30 мин'),
        ('40', '40 мин'),
        ('50', '50 мин'),
        ('60', '60 мин'),
        ('70', '70 мин'),
        ('80', '80 мин'),
    )
    duration = models.CharField(max_length=4, null=True, choices=DURATION)
    price = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=40)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    days = models.ManyToManyField(WeekDays)
    start_time = models.TimeField(auto_now_add=False, null=True)

    def __str__(self):
        return self.title
    

class Room(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title
    

class Report(models.Model):
    TYPE = (
        ('plus', 'Приход'),
        ('minus', 'Расход')
    )

    title = models.CharField(max_length=140)
    price = models.FloatField()
    type = models.CharField(choices=TYPE, max_length=40)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title