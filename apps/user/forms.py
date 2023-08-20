from django import forms
from django.forms import inlineformset_factory
from .models import *
from apps.dashboard.models import *
from django.contrib.auth.forms import UserCreationForm
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'name',
                'placeholder': 'Логин учителя или ученика',
                'aria-describedby': 'basic-addon1'
            }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
                'type': 'password',
                'placeholder': '**********',
                'for': 'password1'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
                'type': 'password',
                'placeholder': '**********',
                'for': 'password2'
    }))
    class Meta:
        model = User
        fields = ['username', 'role', 'password1', 'password2']
        widgets = {
            'role': forms.Select(attrs={
                'class': 'form-control'
            })
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'phone', 'payment', 'group', 'image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'image',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'fullname',
                'placeholder': '...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'id': 'phone',
                'placeholder': '996',
                'value': '996'
            }),
            'payment': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'payment',
                'placeholder': '...',
                'value': '1000'
            }),
            'group': forms.Select(attrs={
                'class': 'form-control',
                'id': 'group',
            }),
        }


class PupilForm(forms.ModelForm):

    class Meta:
        model = Pupil
        fields = ['name', 'phone', 'group', 'image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'image',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'fullname',
                'placeholder': '...'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'id': 'phone',
                'placeholder': '996',
                'value': '996'
            }),

            'group': forms.Select(attrs={
                'class': 'form-control',
                'id': 'group',
            }),
        }
    

class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = ['amount', 'comment', 'created', ]
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment',
                'placeholder': '...',
                'rows': '2'
            }),
            'amount': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'number',
                'id': 'amount',
                'placeholder': '...',
            }),
            'created': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'created',
                'type': 'date'
            }),
        }


class LessonForm(forms.ModelForm):
    
    class Meta:
        model = Lesson
        fields = ['title', 'content', 'access']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'title',
                'placeholder': '...'
            }),

            'content': SummernoteWidget(),
        }


class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['title', 'course', 'days', 'start_time']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'title',
                'placeholder': '...'
            }),

            'course': forms.Select(attrs={
                'class': 'form-control',
                'id': 'course',
            }),
            'days': forms.CheckboxSelectMultiple,
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'value': '12:30:00'
            })

        }
    

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'duration', 'price']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'title',
                'placeholder': '...'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'price',
            }),
            'duration': forms.Select(attrs={
                'class': 'form-control',
                'id': 'price',
            }),

        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'title',
                'placeholder': '...'
            }),
        }


class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ['title', 'is_correct']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'id': 'title',
                'placeholder': 'Ответ'
            }),
            'is_correct': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'type': 'checkbox',
                'id': 'is_correct',
                'placeholder': 'Правильно'
            }),
        }


AnswerFormSet = inlineformset_factory(
    Question, Answer, form=AnswerForm, extra=4 
)

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'price', 'type']

        widgets = {
                'title': forms.TextInput(attrs={
                    'class': 'form-control',
                    'type': 'text',
                    'id': 'title',
                    'placeholder': '...'
                }),
                'price': forms.TextInput(attrs={
                    'class': 'form-control',
                    'id': 'price',
                    'type': 'number'
                }),
                'type': forms.Select(attrs={
                    'class': 'form-control',
                    'id': 'type',
                }),

            }