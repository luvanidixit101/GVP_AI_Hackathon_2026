from django.contrib import admin
from .models import Student, Attendance, Marks


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['roll_no', 'name', 'semester', 'created_at']
    search_fields = ['roll_no', 'name']
    list_filter = ['semester']


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'status', 'created_at']
    list_filter = ['status', 'date']
    search_fields = ['student__roll_no', 'student__name']


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks', 'created_at']
    search_fields = ['student__roll_no', 'student__name', 'subject']
    list_filter = ['subject']
