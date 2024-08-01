from django.shortcuts import render, get_object_or_404
from .models import Teacher, Group, Student
from django.shortcuts import redirect


# views.py
from django.shortcuts import render
from .models import Teacher

def home(request):
    teachers = Teacher.objects.prefetch_related('groups').all()
    return render(request, 'home.html', {'teachers': teachers})


from django.utils import timezone

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


from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Student


def add_student(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student_surname = request.POST.get('student_surname')
        student_phone_number = request.POST.get('student_phone_number')

        if student_name and student_surname and student_phone_number:
            Student.objects.create(
                name=student_name,
                surname=student_surname,
                phone_number=student_phone_number,
                group=group
            )
            return redirect('group_students', group_id=group.id)

    return render(request, 'group_students.html', {'group': group, 'students': group.students.all()})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Student

def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    group_id = student.group.id
    student.delete()
    return redirect('group_students', group_id=group_id)


# views.py
from django.shortcuts import render, redirect
from .models import Group, Teacher

def create_group(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        teacher_id = request.POST.get('teacher_id')
        if group_name and teacher_id:
            teacher = get_object_or_404(Teacher, id=teacher_id)
            Group.objects.create(name=group_name, teacher=teacher)
            return redirect('home')  # Redirect to home or the group list

    teachers = Teacher.objects.all()  # Get all teachers for the form
    return render(request, 'create_group.html', {'teachers': teachers})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Group, Student


def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == 'POST':
        student.name = request.POST.get('student_name')
        student.surname = request.POST.get('student_surname')
        student.phone_number = request.POST.get('student_phone_number')
        student.save()
        return redirect('group_students', group_id=student.group.id)

    return render(request, 'edit_student.html', {'student': student})
