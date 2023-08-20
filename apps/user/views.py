from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Login Page
def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Такого пользователя не существует')

    context = {'page': page}
    return render(request, 'user/login.html', context)


# Logout User
def logout_user(request):
    logout(request)
    return redirect('home')


# Pupil
@login_required(login_url='login')
def pupil_profile(request, pk):
    if request.user.role == '2':
        return redirect('home')
        
    
    pupil = Pupil.objects.get(id=pk)
    get_amount_total = Transaction.objects.filter(pupil__id=pk)
    total  = 0
    for i in get_amount_total:
        total += i.amount

    form = PupilForm(instance=pupil)
    if request.method == 'POST':
        form = PupilForm(request.POST, request.FILES, instance=pupil)
        if form.is_valid():
            form.save()
            return redirect('pupil-profile', pk=pk)
    
    if request.method == 'POST' and 'delete' in request.POST:
        pupil.delete()
        return redirect('pupil-list')

    form2 = TransactionForm()
    if request.method == 'POST' and 'transaction' in request.POST:
        form2 = TransactionForm(request.POST)
        if form2.is_valid():
            form2.instance.pupil = pupil
            form2.save()
            return redirect('pupil-profile', pk=pk)

    transactions = Transaction.objects.filter(pupil=pupil).order_by('-id')

    

    context = {
        'pupil': pupil,
        'form': form,
        'form2': form2,
        'get_amount_total': total,
        'transactions': transactions,
    }
    return render(request, 'user/pupil_profile.html', context)

@login_required(login_url='login')
def pupil_lessons(request):
    if request.user.role != '2':
        return redirect('home')
    pupil = Pupil.objects.get(user=request.user)
    group = pupil.group
    lessons = Lesson.objects.filter(group_access=group)
    context = {
        'lessons': lessons
    }
    return render(request, 'user/pupil_lessons.html', context)


# Teacher
@login_required(login_url='login')
def teacher_profile(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
        
    teacher = Teacher.objects.get(id=pk)
    total_payment = teacher.group.pupil_set.count() * teacher.payment

    form = TeacherForm(instance=teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher-profile', pk=pk)
    
    if request.method == 'POST' and 'delete' in request.POST:
        teacher.delete()
        return redirect('teacher-list')
    

    group = Group.objects.get(teacher=teacher)
    pupils = Pupil.objects.filter(group=group)

    context = {
        'teacher': teacher,
        'form': form,
        'total_payment': total_payment,
        'pupils': pupils,
    }
    return render(request, 'user/teacher_profile.html', context)

@login_required(login_url='login')
def teacher_pupils(request):
    teacher = Teacher.objects.get(user=request.user)
    group = Group.objects.get(teacher=teacher)
    pupils = Pupil.objects.filter(group=group)
    context = {
        'pupils': pupils,
        'teacher': teacher,
    }
    return render(request, 'user/teacher_pupils.html', context)

@login_required(login_url='login')
def teacher_lessons(request):
    if request.user.role != '3':
        return redirect('home')
    teacher = Teacher.objects.get(user=request.user)

    lessons = teacher.group.course.lesson_set.all()
    context = {
        'lessons': lessons
    }
    return render(request, 'user/teacher_lessons.html', context)


# Profile
@login_required(login_url='login')
def profile(request, pk):
    user = User.objects.get(id=pk)
    if request.user == user and request.user.role == '3':
        teacher = Teacher.objects.get(user=user)
        total_payment = teacher.group.pupil_set.count() * teacher.payment
        teacher_total_payment = total_payment * teacher.group.pupil_set.count()
        context = {
        'user': user,
        'total_payment': total_payment,
        'teacher': teacher,
        'teacher_total_payment': teacher_total_payment
        }
        return render(request, 'user/profile.html', context)
    if request.user == user and request.user.role == '2':
        pupil = Pupil.objects.get(user=user)
        get_amount_total = Transaction.objects.filter(pupil=pupil)
        total  = 0
        for i in get_amount_total:
            total += i.amount
        context = {
        'user': user,
        'pupil': pupil,
        'get_amount_total': total
        }
        return render(request, 'user/profile.html', context)
    if request.user == user and request.user.role == '1':
        user = User.objects.get(id=pk)
        context = {
        'user': user,
        }
        return render(request, 'user/profile.html', context)
    context = {
        'user': user,
        }
    return render(request, 'user/profile.html', context)
    
@login_required(login_url='login')
def profile_access(request, pk):
    user = User.objects.get(id=pk)
    if request.user == user and request.user.role == '3':
        teacher = Teacher.objects.get(user=user)
        context = {
        'user': user,
        'teacher': teacher
        }
        return render(request, 'user/profile_access.html', context)
    if request.user == user and request.user.role == '2':
        pupil = Pupil.objects.get(user=user)
        context = {
        'user': user,
        'pupil': pupil
        }
        return render(request, 'user/profile_access.html', context)
    if request.user == user and request.user.role == '1':
        user = User.objects.get(id=pk)
        context = {
        'user': user,
        }
        return render(request, 'user/profile_access.html', context)


# Check
def check_detail(request, pk):
    transaction = Transaction.objects.get(id=pk)
    pupil = transaction.pupil
    context = {
        'transaction': transaction,
        'pupil': pupil
        }
    return render(request, 'user/check_detail.html', context)