from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Student(models.Model):
    roll_no = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['roll_no']

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

    def get_attendance_percentage(self):
        """Calculate attendance percentage for the student"""
        total_lectures = self.attendance_records.count()
        if total_lectures == 0:
            return 0.0
        present_count = self.attendance_records.filter(status='Present').count()
        return round((present_count / total_lectures) * 100, 2)

    def get_average_marks(self):
        """Calculate average marks for the student"""
        marks_records = self.marks_records.all()
        if not marks_records.exists():
            return 0.0
        total_marks = sum([record.marks for record in marks_records])
        return round(total_marks / marks_records.count(), 2)

    def get_performance_remark(self):
        """AI-generated performance remark based on marks"""
        avg_marks = self.get_average_marks()
        if avg_marks >= 75:
            return "Good"
        elif avg_marks >= 50:
            return "Average"
        else:
            return "Needs Improvement"

    def has_attendance_warning(self):
        """Check if student has attendance shortage warning"""
        return self.get_attendance_percentage() < 75


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Present')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.student.roll_no} - {self.date} - {self.status}"


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks_records')
    subject = models.CharField(max_length=100, default='General')
    marks = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'subject']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.roll_no} - {self.subject} - {self.marks}"
