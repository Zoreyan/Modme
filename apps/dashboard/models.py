from django.db import models

class WeekDays(models.Model):
    title = models.CharField(max_length=50)
    day_number = models.IntegerField(null=True)
    def __str__(self):
        return self.title

class Course(models.Model):
    image = models.ImageField(upload_to='course_images/', null=True)
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
    

class Room(models.Model):
    title = models.CharField(max_length=40)

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=40)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    days = models.ManyToManyField(WeekDays)
    color = models.CharField(max_length=10, null=True, default='#10D5D2')
    start_time = models.TimeField(auto_now_add=False, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    @property
    def group_pupil_percentage(self):
        total_pupils = self.pupil_set.count()
        total_percentage = sum([pupil.total_percentage for pupil in self.pupil_set.all()])
        
        return round(total_percentage / total_pupils) if total_pupils else 0

    def __str__(self):
        return self.title


class Support(models.Model):
    name = models.CharField(max_length=20)
    phone = models.IntegerField()
    whatsapp = models.IntegerField()
    is_called = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name