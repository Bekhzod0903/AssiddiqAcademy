from django.shortcuts import render, get_object_or_404
from .models import Teacher, Group, Student
from django.shortcuts import redirect


def home(request):
    teachers = Teacher.objects.prefetch_related('groups').all()
    return render(request, 'home.html', {'teachers': teachers})

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Group, Student

def group_students(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Get the current date and time
    today = timezone.now().date()

    # Check if today is 30 days after the group start date
    reset_due_date = group.start_date + timezone.timedelta(days=30)

    # Reset payment status for all students when the button is pressed
    if request.method == 'POST' and 'reset_payments' in request.POST:
        students = Student.objects.filter(group=group)
        for student in students:
            student.payment_status = False
            student.group_payment = None
            student.save()

    students = group.students.all()
    return render(request, 'group_students.html', {'group': group, 'students': students, 'today': today, 'reset_due_date': reset_due_date})

from django.contrib import messages

def pay(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            student.payment_status = True
            student.group_payment = amount
            student.save()
            messages.success(request, 'To\'lov muvaffaqiyatli amalga oshirildi!')
            return redirect('group_students', group_id=student.group.id)

    return render(request, 'pay.html', {'student': student})


def add_student(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        if student_name:
            Student.objects.create(name=student_name, group=group)
            return redirect('group_students', group_id=group.id)

    return render(request, 'group_students.html', {'group': group, 'students': group.students.all()})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Student

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    group_id = student.group.id
    student.delete()
    return redirect('group_students', group_id=group_id)
