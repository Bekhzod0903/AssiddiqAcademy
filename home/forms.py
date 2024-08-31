from django import forms
from .models import Teacher, Group, Student

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'start_date', 'teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'phone_number', 'payment_status', 'group_payment', 'group']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'group_payment': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }
