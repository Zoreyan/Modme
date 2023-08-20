from django.shortcuts import render, redirect
from apps.user.models import *
from apps.user.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
import random
from django.http import JsonResponse
import string

# Home
@login_required(login_url='login')
def home(request):
    context = {

    }
    return render(request, 'dashboard/home.html', context)

def calendar_view(request):
    if request.user.role == '3':
        teacher = Teacher.objects.get(user=request.user)
        groups = Group.objects.filter(teacher=teacher)
    elif request.user.role == '2':
        pupil = Pupil.objects.get(user=request.user)
        groups = Group.objects.filter(pupil=pupil)
    else:
        groups = Group.objects.all()
    events = []

    for group in groups:
        for day in group.days.all():

            event = {
                'title': group.title,
                'startTime': group.start_time.strftime("%H:%M:%S"),
                'daysOfWeek': [day.day_number],
                'url': f'/group-detail/{group.id}',
            }
            events.append(event)

    return JsonResponse(events, safe=False)

# Teacher
@login_required(login_url='login')
def teacher_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    teachers = Teacher.objects.all().order_by('-id')
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user = User.objects.create_user(username=username, password=password, role=3, name=request.POST.get('name'))
            form.instance.user = user
            form.instance.password = password
            form.save()
    
    search_q = request.GET.get('teacher_q', '')

    if search_q:
        teachers = Teacher.objects.filter(name__icontains=search_q)
    else:
        teachers = Teacher.objects.all().order_by('-id')
    
    context = {
        'teachers': teachers,
        'form': form,
    }
    return render(request, 'dashboard/teacher_list.html', context)

# Pupil
@login_required(login_url='login')
def pupil_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    pupils = Pupil.objects.all().order_by('-id')
    form = PupilForm()
    if request.method == 'POST':
        form = PupilForm(request.POST, request.FILES)
        if form.is_valid():
            username = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            user = User.objects.create_user(username=username, password=password, role=2, name=request.POST.get('name'))
            form.instance.user = user
            form.instance.password = password
            form.save()
    
    search_q = request.GET.get('pupil_q', '')

    if search_q:
        pupils = Pupil.objects.filter(name__icontains=search_q)
    else:
        pupils = Pupil.objects.all().order_by('-id')
    context = {
        'pupils': pupils,
        'form': form,
    }
    return render(request, 'dashboard/pupil_list.html', context)

# Lessons
@login_required(login_url='login')
def lesson_list(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    course = Course.objects.get(id=pk)
    lessons = Lesson.objects.filter(course=course).order_by('-id')
    
    if request.method == 'POST' and 'delete' in request.POST:
        lesson_id = request.POST.get('lesson')
        lesson = Lesson.objects.get(id=lesson_id)
        lesson.delete()
        return redirect('lesson-list', pk=pk)

    context = {
        'lessons': lessons,
        'course': course,
    }
    return render(request, 'dashboard/lesson_list.html', context)

@login_required(login_url='login')
def lesson_detail(request, pk):
    lesson = Lesson.objects.get(id=pk)
    questions = Question.objects.filter(lesson=lesson)
    if request.user.role == '2' and not lesson.access:
        return redirect('pupil-lessons')

    # Разрешение доступа к уроку
    if request.user.role == '3':
        teacher = Teacher.objects.get(user=request.user)
        if request.method == 'POST' and 'access' in request.POST:
            if lesson.access:
                lesson.access = False
                lesson.group_access.clear()
            else:
                lesson.access = True
                lesson.group_access.add(teacher.group)
            lesson.save()

    
    # Удаление урока
    if request.method == 'POST' and 'delete' in request.POST:
        lesson.delete()
        return redirect('lesson-list')

    
    # Создание вопроса и ответа ответа
    answer_form_set = AnswerFormSet()
    if request.method == 'POST' and 'accept_question' in request.POST:
        answer_form_set = AnswerFormSet(request.POST)
        if answer_form_set.is_valid():
            question = Question.objects.create(
                lesson=lesson,
                title=request.POST.get('title'),
                marks=5,
                skill=request.POST.get('skill')
            )
            answer_form_set.instance = question
            answer_form_set.save()
            return redirect('lesson-detail', pk=pk)
    
    # Обработка ответов
    if (request.user.role == '2' and request.method == 'POST' and 'answer_submit' in request.POST):
        answer_list = request.POST.getlist('answer_id')
        answers = Answer.objects.filter(
            question__lesson=lesson, 
            is_correct=True, 
            id__in=answer_list
        )

        skill_scores = {
            'grammary': 0,
            'speaking': 0,
            'listening': 0,
            'vocabulary': 0,
            'reading': 0
        }

        for answer in answers:
            skill = answer.question.skill
            if skill in skill_scores:
                skill_scores[skill] += 1

        total_correct_answers = len(answers)

        result = TestResult(
            lesson=lesson,
            pupil=Pupil.objects.get(user=request.user),
            total_correct_answers=total_correct_answers,
            total_questions=questions.count(),
            vocabulary_score=skill_scores['vocabulary'],
            listening_score=skill_scores['listening'],
            grammary_score=skill_scores['grammary'],
            reading_score=skill_scores['reading'],
            speaking_score=skill_scores['speaking']
        )
        result.save()
        result.questions.add(*questions)

    test_result_access = TestResult.objects.filter(pupil=request.user.pupil, lesson=lesson).exists() if request.user.role == '2' else 0
    context = {
        'lesson': lesson,
        'questions': questions,
        'formset': answer_form_set,
        'test_result_access': test_result_access
    }
    return render(request, 'dashboard/lesson_detail.html', context)

@login_required(login_url='login')
def lesson_create(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    course = Course.objects.get(id=pk)
    form = LessonForm()
    if request.method == 'POST':
        form = LessonForm(request.POST)
        form.instance.course = course

        if form.is_valid():
            form.save()
            return redirect('lesson-list', pk=pk)
    context = {
        'form': form,
        'course': course
    }
    return render(request, 'dashboard/lesson_create.html', context)

@login_required(login_url='login')
def lesson_update(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    lesson = Lesson.objects.get(id=pk)
    form = LessonForm(instance=lesson)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('lesson-detail', pk=pk)
    context = {
        'form': form
    }
    return render(request, 'dashboard/lesson_update.html', context)

# Groups
def group_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    groups = Group.objects.all().order_by('-id')
    form = GroupForm()
    

    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    context = {
        'groups': groups,
        'form': form
    }
    return render(request, 'dashboard/group_list.html', context)

def group_detail(request, pk):
    group = Group.objects.get(id=pk)
    pupils = Pupil.objects.filter(group=group)
    teachers = Teacher.objects.filter(group=group)
    if request.method == 'POST' and 'delete' in request.POST:
        group.delete()
        return redirect('group-list')
    context = {
        'group': group,
        'pupils': pupils,
        'teachers': teachers
    }
    return render(request, 'dashboard/group_detail.html', context)

def group_update(request, pk):
    group = Group.objects.get(id=pk)
    form = GroupForm(instance=group)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group-detail', pk=pk)
    context = {
        'group': group,
        'form': form
    }
    return render(request, 'dashboard/group_update.html', context)

# Rooms
def room_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    rooms = Room.objects.all().order_by('-id')
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room-list')
    context = {
        'rooms': rooms,
        'form': form
    }
    return render(request, 'dashboard/room_list.html', context)

# Courses
def course_list(request):
    if not request.user.is_superuser:
        return redirect('home')

    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
    courses = Course.objects.all().order_by('-id')
    context = {
        'courses': courses,
        'form': form
    }
    return render(request, 'dashboard/course_list.html', context)

def course_detail(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
    course = Course.objects.get(id=pk)
    groups = Group.objects.filter(course=course).order_by('-id')
    pupils = Pupil.objects.filter(group__course=course)
    teachers = Teacher.objects.filter(group__course=course)
    context = {
        'groups': groups,
        'course': course,
        'pupils': pupils,
        'teachers': teachers,
    }
    return render(request, 'dashboard/course_detail.html', context)


# Reports
def report_view(request):
    if not request.user.role=='1':
        return redirect('home')
    
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if date_from and date_to:
        reports_plus = Report.objects.filter(created__gte=date_from,
                              created__lte=date_to, type='plus')
        reports_minus = Report.objects.filter(created__gte=date_from,
                              created__lte=date_to, type='minus')
    else:
        reports_plus = Report.objects.filter(type='plus')
        reports_minus = Report.objects.filter(type='minus')

    total_plus = sum([item.price for item in reports_plus])
    total_minus = sum([item.price for item in reports_minus])

    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report-view')
    
    if request.method == 'POST' and 'delete' in request.POST:
        report_id = request.POST.get('report_id')
        report = Report.objects.get(id=report_id)
        report.delete()
        return redirect('report-view')
        
    context = {
        'reports_plus': reports_plus,
        'reports_minus': reports_minus,
        'total_plus': total_plus,
        'total_minus': total_minus,
        'form': form
    }
    return render(request, 'dashboard/report_view.html', context)

# KPI
def kpi_view(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers
    }
    return render(request, 'dashboard/kpi_view.html', context)