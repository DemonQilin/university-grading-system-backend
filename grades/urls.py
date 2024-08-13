from django.urls import path

from grades.views import course, inscription, subject

app_name = 'grades'

urlpatterns = [
    path('courses/', course.CourseListView.as_view(), name='course_list'),
    path('courses/<int:course_id>/',
         subject.assign_course_grade, name='assign_grade'),
    path('inscriptions/', inscription.create_inscription,
         name='inscription_creation'),
    path('students/<str:username>/current-subjects/',
         subject.list_current_student_subjects, name='current_student_subjects'),
    path('students/<str:username>/summary/',
         subject.get_student_summary, name='student_summary'),
    path('professors/<str:username>/subjects/',
         subject.get_professor_subjects, name='professor_subjects'),
    path('professors/<str:username>/subjects/<uuid:subject_id>/students/',
         subject.get_students_by_subject, name='students_by_subject'),
]
