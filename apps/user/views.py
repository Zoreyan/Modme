from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import requests
from django.http import HttpResponse

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Login Page
def login_page(request):
    page = 'login'
    ip = get_client_ip(request)
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

# Operator
@login_required(login_url='login')
def operator_profile(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
        
    operator = Operator.objects.get(id=pk)

    form = OperatorForm(instance=operator)
    if request.method == 'POST':
        form = OperatorForm(request.POST, request.FILES, instance=operator)
        if form.is_valid():
            form.save()
            return redirect('operator-profile', pk=pk)
    
    if request.method == 'POST' and 'delete' in request.POST:
        operator.delete()
        return redirect('operator-list')
    
    context = {
        'operator': operator,
        'form': form,
    }
    return render(request, 'user/operator_profile.html', context)


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
def pupil_groups(request):
    if request.user.role != '2':
        return redirect('home')
    groups = Group.objects.filter(pupil=request.user.pupil)

    context = {
        'groups': groups
    }
    return render(request, 'user/pupil_groups.html', context)

@login_required(login_url='login')
def pupil_lessons(request, pk):
    if request.user.role != '2':
        return redirect('home')
    pupil = Pupil.objects.get(user=request.user)
    groups = Group.objects.filter(pupil=pupil)
    group = Group.objects.get(id=pk)

    lessons = Lesson.objects.filter(group_access__in=groups)
    context = {
        'lessons': lessons,
        'group': group
    }
    return render(request, 'user/pupil_lessons.html', context)


# Teacher
@login_required(login_url='login')
def teacher_profile(request, pk):
    if not request.user.is_superuser:
        return redirect('home')
        
    teacher = Teacher.objects.get(id=pk)
    # total_payment = teacher.group.pupil_set.count() * teacher.payment

    form = TeacherForm(instance=teacher)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher-profile', pk=pk)
    
    if request.method == 'POST' and 'delete' in request.POST:
        teacher.delete()
        return redirect('teacher-list')
    

    group = Group.objects.filter(teacher=teacher)
    # pupils = Pupil.objects.filter(group=group)

    context = {
        'teacher': teacher,
        'form': form,
        # 'total_payment': total_payment,
        # 'pupils': pupils,
    }
    return render(request, 'user/teacher_profile.html', context)

@login_required(login_url='login')
def teacher_pupils(request):
    teacher = Teacher.objects.get(user=request.user)
    group = Group.objects.filter(teacher=teacher)
    pupils = Pupil.objects.filter(group__in=group)
    context = {
        'pupils': pupils,
        'teacher': teacher,
    }
    return render(request, 'user/teacher_pupils.html', context)

@login_required(login_url='login')
def teacher_groups(request):
    if request.user.role != '3':
        return redirect('home')
    groups = Group.objects.filter(teacher=request.user.teacher)

    context = {
        'groups': groups
    }
    return render(request, 'user/teacher_groups.html', context)

@login_required(login_url='login')
def teacher_lessons(request, pk):
    if request.user.role != '3':
        return redirect('home')
    teacher = Teacher.objects.get(user=request.user)
    group = Group.objects.get(id=pk)

    lessons = Lesson.objects.filter(course__group=group).distinct()
    context = {
        'lessons': lessons,
        'group': group
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


def send_to_whatsapp(request, pk):
    transaction = Transaction.objects.get(id=pk)
    message = f"Здравствуйте! Ваш чек: {transaction.amount} СОМ, для {transaction.pupil.name}"
    

    whatsapp_api_url = "https://api.whatsapp.com/send"
    params = {
        "phone": f"{transaction.pupil.phone}",
        "text": message,
    }
    response = requests.get(whatsapp_api_url, params=params)
    
    if response.status_code == 200:
        return HttpResponse("Сообщение отправлено на WhatsApp")
    else:
        return HttpResponse("Произошла ошибка при отправке сообщения")
