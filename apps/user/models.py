from django.db import models
from apps.dashboard.models import Group, Course
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=140, null=True)
    STATUS = (
        ('1', 'Админ'),
        ('2', 'Студент'),
        ('3', 'Преподаватель')
    )
    role = models.CharField(null=True, choices=STATUS, max_length=140, default='1')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []


class Lesson(models.Model):
    title = models.CharField(max_length=140)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    group_access = models.ManyToManyField(Group, blank=True)
    content = models.TextField(null=True, blank=True)
    access = models.BooleanField(null=True, blank=True, default=False)


    
    def __str__(self):
        return self.title


class Question(models.Model):
    lesson=models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    SKILLS = (
        ('vocabulary', 'Vocabulary'),
        ('grammary', 'Grammary'),
        ('speaking', 'Speaking'),
        ('reading', 'Reading'),
        ('listening', 'Listening'),
    )
    skill = models.CharField(max_length=80, null=True, choices=SKILLS)
    title = models.CharField(max_length=150, null=True)
    marks=models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=20, null=True)
    is_correct = models.BooleanField(default=False ,verbose_name='Правильно')

    def __str__(self):
        return self.title


class TestResult(models.Model):
    pupil = models.ForeignKey('Pupil', on_delete=models.CASCADE, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Question, null=True)
    total_correct_answers = models.IntegerField(null=True)
    total_questions = models.IntegerField(null=True)
    
    vocabulary_score = models.IntegerField(null=True, blank=True, default='0')
    listening_score = models.IntegerField(null=True, blank=True, default='0')
    reading_score = models.IntegerField(null=True, blank=True, default='0')
    grammary_score = models.IntegerField(null=True, blank=True, default='0')
    speaking_score = models.IntegerField(null=True, blank=True, default='0')


    def __str__(self):
        return self.pupil.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='profile_photos', null=True, blank=True)
    phone = models.CharField(max_length=12, default='996')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    payment = models.IntegerField(null=True)
    password = models.CharField(max_length=20, null=True, default=' ')

    def __str__(self):
        return self.name

    @property
    def group_pupil_percentage(self):
        pupils = self.group.pupil_set.all()
        total_percentage = sum([pupil.total_percentage for pupil in pupils])
        return round(total_percentage / len(pupils)) if pupils else 0

class Pupil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='profile_photos', null=True, blank=True)
    phone = models.CharField(max_length=12, default='996')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=20, null=True, default=' ')


    def __str__(self):
        return self.name
    

    @property
    def total_amount(self):
        transactions = self.transaction_set.all()
        total = sum([item.amount for item in transactions])
        return total
    
    @property
    def total_score(self):
        answers = self.testresult_set.all()
        total = sum([item.total_correct_answers for item in answers])
        return total
    
    @property
    def total_questions(self):
        questions = self.testresult_set.all()
        total = sum([item.total_questions for item in questions])
        return total
    
    @property
    def total_percentage(self):
        try:
            return round((self.total_score / self.total_questions) * 100)
        except:
            return  0

    def skill_percentage(self, skill):
        skill_questions = TestResult.objects.filter(
            pupil=self,
            questions__skill=skill
        ).count()
        correct_answers = TestResult.objects.filter(pupil=self)
        total_score = sum(getattr(item, f'{skill}_score') for item in correct_answers)

        if skill_questions != 0:
            skill_percentage = (total_score / skill_questions) * 100
        else:
            skill_percentage = 0

        return round(skill_percentage)

    @property
    def vocabulary_percentage(self):
        return self.skill_percentage('vocabulary')

    @property
    def grammary_percentage(self):
        return self.skill_percentage('grammary')

    @property
    def reading_percentage(self):
        return self.skill_percentage('reading')

    @property
    def speaking_percentage(self):
        return self.skill_percentage('speaking')

    @property
    def listening_percentage(self):
        return self.skill_percentage('listening')


class Transaction(models.Model):
    pupil = models.ForeignKey(Pupil, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField()
    comment = models.TextField(max_length=140)
    created = models.DateField(auto_now_add=False)

