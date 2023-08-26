from django.shortcuts import render, redirect
from apps.user.models import *
from apps.user.forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from openpyxl import Workbook
import random
import string

def main(request):
    courses = Course.objects.all()
    form = SupportForm()
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Ваш контакт был успешно отправлен. Наш оператор позвонит вам в ближайшее время!')


    context = {
        'courses': courses,
        'form': form
    }
    return render(request, 'landing/index.html', context)

# Home
@login_required(login_url='login')
def home(request):

    return render(request, 'dashboard/home.html')

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
                'title': f'{group.title} - {group.room.title}',
                'startTime': group.start_time.strftime("%H:%M:%S"),
                'daysOfWeek': [day.day_number],
                'url': f'/group-detail/{group.id}',
                'color': group.color
            }
            events.append(event)

    return JsonResponse(events, safe=False)

# Operator
@login_required(login_url='login')
def operator_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    # List
    operators = Operator.objects.all().order_by('-id')

    # Add Teacher
    form = OperatorForm()
    if request.method == 'POST':
        form = OperatorForm(request.POST, request.FILES)
        if form.is_valid():
            username = ''.join(random.choices(string.ascii_letters, k=4))
            password = ''.join(random.choices(string.ascii_letters, k=8))
            user = User.objects.create_user(username=username, password=password, role=4, name=request.POST.get('name'))
            form.instance.user = user
            form.instance.password = password
            form.save()

    # Search Teacher
    search_q = request.GET.get('operator_q', '')
    if search_q:
        operators = Operator.objects.filter(name__icontains=search_q)
    else:
        operators = Operator.objects.all().order_by('-id')
    
    context = {
        'operators': operators,
        'form': form,
    }
    return render(request, 'dashboard/operator_list.html', context)


# Teacher
@login_required(login_url='login')
def teacher_list(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    # List
    teachers = Teacher.objects.all().order_by('-id')

    # Add Teacher
    form = TeacherForm()
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            username = ''.join(random.choices(string.ascii_letters, k=4))
            password = ''.join(random.choices(string.ascii_letters, k=8))
            user = User.objects.create_user(username=username, password=password, role=3, name=request.POST.get('name'))
            form.instance.user = user
            form.instance.password = password
            form.save()

    # Search Teacher
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
    
    # List
    pupils = Pupil.objects.all().order_by('-id')

    # Add Pupil
    form = PupilForm()
    if request.method == 'POST':
        form = PupilForm(request.POST, request.FILES)
        if form.is_valid():
            username = ''.join(random.choices(string.ascii_letters, k=4))
            password = ''.join(random.choices(string.ascii_letters, k=8))
            user = User.objects.create_user(username=username, password=password, role=2, name=request.POST.get('name'))
            form.instance.user = user
            form.instance.password = password
            form.save()

    # Search Pupil
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
    
    # List
    course = Course.objects.get(id=pk)
    lessons = Lesson.objects.filter(course=course).order_by('-id')

    # Delete Lesson
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
    
    # Get Lesson
    lesson = Lesson.objects.get(id=pk)
    if request.user.role == '3':
        group_id = request.GET.get('group_id')
        group = Group.objects.get(id=group_id)
    else:
        group = None

    # Access to lesson
    if request.user.role == '2' and not lesson.access:
        return redirect('home')
    # List questions
    questions = Question.objects.filter(lesson=lesson)

    # Pupil Attendance
    pupils = None
    try:
        attendances = Attendance.objects.get(lesson=lesson)
    except:
        attendances = None


    # Allowing access to lesson and pupil attendance
    if request.user.role == '3':
        pupils = Pupil.objects.filter(group__teacher = request.user.teacher)
        if request.method == 'POST':
            # Add Pupils to attendance
            if 'pupil_attendance' in request.POST:
                pupil_attendance = request.POST.getlist('pupil_attendance')
                pupil_filtered = Pupil.objects.filter(id__in=pupil_attendance)
                print(pupil_filtered)
                attendance = Attendance.objects.create(lesson=lesson)
                attendance.pupils.add(*pupil_filtered)
                attendance.save()
                return redirect('lesson-detail', pk=pk)

            # Access to lesson
            if 'access' in request.POST:
                if lesson.access:
                    lesson.access = False
                    lesson.group_access.clear()
                else:
                    lesson.access = True
                    lesson.group_access.add(group)
                lesson.save()

    
    # Delete Lesson
    if request.method == 'POST' and 'delete' in request.POST:
        lesson.delete()
        return redirect('lesson-list')

    
    # Creating Question and Answers
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
    
    # Loading Answers
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

        # Create Test Result
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

    # Check access to Task
    test_result_access = TestResult.objects.filter(pupil=request.user.pupil, lesson=lesson).exists() if request.user.role == '2' else 0
    context = {
        'lesson': lesson,
        'questions': questions,
        'formset': answer_form_set,
        'test_result_access': test_result_access,
        'pupils': pupils,
        'attendances': attendances,
        'group': group
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

def room_detail(request, pk):
    groups = Group.objects.filter(room__id=pk)
    context = {
        'groups': groups
    }
    return render(request, 'dashboard/room_detail.html', context)

# Courses
def course_list(request):
    if not request.user.is_superuser:
        return redirect('home')

    form = CourseForm()
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
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
    pupils = Pupil.objects.filter(group__course=course).distinct()
    teachers = Teacher.objects.filter(group__course=course).distinct()
    if request.method == 'POST' and 'delete' in request.POST:
        course = Course.objects.get(id=pk)
        course.delete()
        return redirect('course-list')
    context = {
        'groups': groups,
        'course': course,
        'pupils': pupils,
        'teachers': teachers,
    }
    return render(request, 'dashboard/course_detail.html', context)

def course_update(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(instance=course)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course-detail', pk=pk)
    context = {
        'course': course,
        'form': form
    }
    return render(request, 'dashboard/course_update.html', context)

# Reports
def report_view(request):
    if request.user.role=='2' or request.user.role=='3':
        return redirect('home')
    
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    if date_from and date_to:
        reports_plus = Report.objects.filter(created__gte=date_from,
                              created__lte=date_to, type='plus').order_by('-id')
        reports_minus = Report.objects.filter(created__gte=date_from,
                              created__lte=date_to, type='minus').order_by('-id')
    else:
        reports_plus = Report.objects.filter(type='plus').order_by('-id')
        reports_minus = Report.objects.filter(type='minus').order_by('-id')

    total_plus = sum([item.price for item in reports_plus])
    total_minus = sum([item.price for item in reports_minus])

    if request.user.role == '4':
        form = ReportForm()
        if request.method == 'POST':
            form = ReportForm(request.POST)
            if form.is_valid():
                form.instance.operator = request.user.operator
                form.save()
                return redirect('report-view')
    else:
        form = None
    
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

def export_report_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report_data.xlsx"'

    wb = Workbook()
    ws = wb.active

    # Добавляем заголовки столбцов
    columns = ['ID', 'Администратор', 'Описание', 'Цена', 'Тип', 'Дата создания']
    ws.append(columns)

    # Добавляем данные
    queryset = Report.objects.all()
    for row in queryset:
        data_row = [row.id, row.operator.name, row.title, row.price, row.get_type_display(), f'{row.created.date()}']
        ws.append(data_row)

    wb.save(response)
    return response

# KPI
def kpi_view(request):
    teachers = Teacher.objects.all()
    context = {
        'teachers': teachers
    }
    return render(request, 'dashboard/kpi_view.html', context)

# Support
def support_list(request):
    supports = Support.objects.all().order_by('-id')
    if request.method == 'POST':
        support_id = request.POST.get('support_id')
        support = Support.objects.get(id=support_id)
        support.is_called = True
        support.save()
        return redirect('support-list')
    context = {
        'supports': supports
    }
    return render(request, 'dashboard/support_list.html', context)