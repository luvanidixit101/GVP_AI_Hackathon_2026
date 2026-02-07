from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Student, Attendance, Marks
from .ai_helpers import (
    validate_roll_number, get_performance_remark, get_attendance_warning,
    generate_sample_student_data, generate_sample_attendance_data, generate_sample_marks_data
)
from datetime import date


def home(request):
    """Home page with dashboard"""
    total_students = Student.objects.count()
    students_with_warnings = [s for s in Student.objects.all() if s.has_attendance_warning()]
    
    context = {
        'total_students': total_students,
        'warning_count': len(students_with_warnings),
        'recent_students': Student.objects.all()[:5],
    }
    return render(request, 'tracker/home.html', context)


def student_list(request):
    """Display all students"""
    students = Student.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        students = students.filter(
            Q(roll_no__icontains=search_query) | 
            Q(name__icontains=search_query)
        )
    
    # Add attendance and marks info
    student_data = []
    for student in students:
        attendance_pct = student.get_attendance_percentage()
        avg_marks = student.get_average_marks()
        has_warning, warning_msg, warning_type = get_attendance_warning(attendance_pct)
        remark, remark_type = get_performance_remark(avg_marks)
        
        student_data.append({
            'student': student,
            'attendance_pct': attendance_pct,
            'avg_marks': avg_marks,
            'has_warning': has_warning,
            'warning_msg': warning_msg,
            'warning_type': warning_type,
            'remark': remark,
            'remark_type': remark_type,
        })
    
    context = {
        'student_data': student_data,
        'search_query': search_query,
    }
    return render(request, 'tracker/student_list.html', context)


def add_student(request):
    """Add a new student"""
    if request.method == 'POST':
        roll_no = request.POST.get('roll_no', '').strip()
        name = request.POST.get('name', '').strip()
        semester = request.POST.get('semester', '')
        
        # AI-assisted validation
        is_valid, error_msg = validate_roll_number(roll_no)
        if not is_valid:
            messages.error(request, error_msg)
            return render(request, 'tracker/add_student.html')
        
        if not name:
            messages.error(request, "Name cannot be empty")
            return render(request, 'tracker/add_student.html')
        
        try:
            semester = int(semester)
            if semester < 1 or semester > 12:
                messages.error(request, "Semester must be between 1 and 12")
                return render(request, 'tracker/add_student.html')
        except ValueError:
            messages.error(request, "Invalid semester number")
            return render(request, 'tracker/add_student.html')
        
        # Check if roll number already exists
        if Student.objects.filter(roll_no=roll_no).exists():
            messages.error(request, f"Student with Roll No {roll_no} already exists")
            return render(request, 'tracker/add_student.html')
        
        student = Student.objects.create(
            roll_no=roll_no,
            name=name,
            semester=semester
        )
        messages.success(request, f"Student {student.name} (Roll No: {student.roll_no}) added successfully!")
        return redirect('student_list')
    
    return render(request, 'tracker/add_student.html')


def mark_attendance(request):
    """Mark attendance for students"""
    if request.method == 'POST':
        roll_no = request.POST.get('roll_no', '').strip()
        attendance_date = request.POST.get('date', '')
        status = request.POST.get('status', 'Present')
        
        # Validate roll number
        is_valid, error_msg = validate_roll_number(roll_no)
        if not is_valid:
            messages.error(request, error_msg)
            return render(request, 'tracker/mark_attendance.html', {'students': Student.objects.all()})
        
        try:
            student = Student.objects.get(roll_no=roll_no)
        except Student.DoesNotExist:
            messages.error(request, f"Student with Roll No {roll_no} not found")
            return render(request, 'tracker/mark_attendance.html', {'students': Student.objects.all()})
        
        if not attendance_date:
            attendance_date = date.today()
        else:
            try:
                attendance_date = date.fromisoformat(attendance_date)
            except ValueError:
                messages.error(request, "Invalid date format")
                return render(request, 'tracker/mark_attendance.html', {'students': Student.objects.all()})
        
        # Check if attendance already marked for this date
        attendance, created = Attendance.objects.get_or_create(
            student=student,
            date=attendance_date,
            defaults={'status': status}
        )
        
        if not created:
            attendance.status = status
            attendance.save()
            messages.success(request, f"Attendance updated for {student.name} on {attendance_date}")
        else:
            messages.success(request, f"Attendance marked successfully for {student.name} on {attendance_date}")
        
        return redirect('mark_attendance')
    
    students = Student.objects.all()
    return render(request, 'tracker/mark_attendance.html', {'students': students})


def enter_marks(request):
    """Enter marks for students"""
    if request.method == 'POST':
        roll_no = request.POST.get('roll_no', '').strip()
        subject = request.POST.get('subject', 'General').strip()
        marks_str = request.POST.get('marks', '')
        
        # Validate roll number
        is_valid, error_msg = validate_roll_number(roll_no)
        if not is_valid:
            messages.error(request, error_msg)
            return render(request, 'tracker/enter_marks.html', {'students': Student.objects.all()})
        
        try:
            student = Student.objects.get(roll_no=roll_no)
        except Student.DoesNotExist:
            messages.error(request, f"Student with Roll No {roll_no} not found")
            return render(request, 'tracker/enter_marks.html', {'students': Student.objects.all()})
        
        try:
            marks = float(marks_str)
            if marks < 0 or marks > 100:
                messages.error(request, "Marks must be between 0 and 100")
                return render(request, 'tracker/enter_marks.html', {'students': Student.objects.all()})
        except ValueError:
            messages.error(request, "Invalid marks value")
            return render(request, 'tracker/enter_marks.html', {'students': Student.objects.all()})
        
        marks_obj, created = Marks.objects.update_or_create(
            student=student,
            subject=subject,
            defaults={'marks': marks}
        )
        
        if created:
            messages.success(request, f"Marks saved successfully for {student.name}!")
        else:
            messages.success(request, f"Marks updated successfully for {student.name}!")
        
        return redirect('enter_marks')
    
    students = Student.objects.all()
    return render(request, 'tracker/enter_marks.html', {'students': students})


def student_report(request, roll_no):
    """View detailed report for a student"""
    student = get_object_or_404(Student, roll_no=roll_no)
    
    attendance_pct = student.get_attendance_percentage()
    avg_marks = student.get_average_marks()
    has_warning, warning_msg, warning_type = get_attendance_warning(attendance_pct)
    remark, remark_type = get_performance_remark(avg_marks)
    
    attendance_records = student.attendance_records.all()[:20]  # Last 20 records
    marks_records = student.marks_records.all()
    
    context = {
        'student': student,
        'attendance_pct': attendance_pct,
        'avg_marks': avg_marks,
        'has_warning': has_warning,
        'warning_msg': warning_msg,
        'warning_type': warning_type,
        'remark': remark,
        'remark_type': remark_type,
        'attendance_records': attendance_records,
        'marks_records': marks_records,
    }
    return render(request, 'tracker/student_report.html', context)


def generate_sample_data(request):
    """AI-assisted function to generate sample student data"""
    if request.method == 'POST':
        count = int(request.POST.get('count', 5))
        
        students_data = generate_sample_student_data(count)
        
        created_count = 0
        for data in students_data:
            student, created = Student.objects.get_or_create(
                roll_no=data['roll_no'],
                defaults={
                    'name': data['name'],
                    'semester': data['semester']
                }
            )
            
            if created:
                created_count += 1
                # Generate sample attendance
                attendance_data = generate_sample_attendance_data(student, days_back=20)
                for att_data in attendance_data:
                    Attendance.objects.get_or_create(
                        student=student,
                        date=att_data['date'],
                        defaults={'status': att_data['status']}
                    )
                
                # Generate sample marks
                marks_data = generate_sample_marks_data(student)
                Marks.objects.get_or_create(
                    student=student,
                    subject=marks_data['subject'],
                    defaults={'marks': marks_data['marks']}
                )
        
        messages.success(request, f"Generated {created_count} sample students with attendance and marks data!")
        return redirect('student_list')
    
    return render(request, 'tracker/generate_sample_data.html')
