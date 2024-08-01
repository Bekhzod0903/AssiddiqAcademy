from django.urls import path
from .views import home,group_students,pay,add_student,delete_student,create_group,edit_student

urlpatterns = [
    path('', home, name='home'),
    path('group/<int:group_id>/', group_students, name='group_students'),
    path('pay/<int:student_id>/', pay, name='pay'),
    path('groups/<int:group_id>/add_student/', add_student, name='add_student'),
    path('students/<int:student_id>/delete/', delete_student, name='delete_student'),
    path('create-group/', create_group, name='create_group'),
    path('students/<int:student_id>/edit/', edit_student, name='edit_student'),

]