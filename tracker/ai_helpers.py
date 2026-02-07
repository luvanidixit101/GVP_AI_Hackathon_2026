"""
AI-Assisted Helper Functions
This module contains AI-generated validation logic, remarks, and data generation
"""

import random
import string
from datetime import date, timedelta


def validate_roll_number(roll_no):
    """
    AI-generated validation logic for roll number
    Validates: non-empty, alphanumeric, reasonable length
    """
    if not roll_no or not roll_no.strip():
        return False, "Roll number cannot be empty"
    
    roll_no = roll_no.strip()
    
    if len(roll_no) < 2 or len(roll_no) > 20:
        return False, "Roll number must be between 2 and 20 characters"
    
    if not roll_no.replace('-', '').replace('_', '').isalnum():
        return False, "Roll number should contain only letters, numbers, hyphens, or underscores"
    
    return True, "Valid roll number"


def get_performance_remark(marks):
    """
    AI-generated performance remark based on marks
    """
    if marks >= 75:
        return "Good", "success"
    elif marks >= 50:
        return "Average", "warning"
    else:
        return "Needs Improvement", "danger"


def get_attendance_warning(percentage):
    """
    AI-generated attendance shortage warning
    """
    if percentage < 75:
        return True, f"⚠ Attendance Shortage: {percentage}% (Below 75%)", "danger"
    elif percentage < 85:
        return True, f"⚠ Low Attendance: {percentage}% (Below 85%)", "warning"
    else:
        return False, f"✓ Good Attendance: {percentage}%", "success"


def generate_sample_student_data(count=5):
    """
    AI-generated function to auto-generate sample student data
    """
    first_names = [
        "Rahul", "Priya", "Amit", "Sneha", "Vikram", "Anjali", 
        "Rohan", "Kavya", "Arjun", "Divya", "Siddharth", "Meera",
        "Karan", "Pooja", "Aditya", "Shreya", "Neeraj", "Radha"
    ]
    
    last_names = [
        "Shah", "Patel", "Kumar", "Singh", "Sharma", "Verma",
        "Gupta", "Reddy", "Rao", "Nair", "Mehta", "Joshi",
        "Desai", "Malhotra", "Agarwal", "Iyer", "Menon", "Pillai"
    ]
    
    students_data = []
    
    for i in range(count):
        roll_no = f"STU{100 + i:03d}"
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        semester = random.randint(1, 8)
        
        students_data.append({
            'roll_no': roll_no,
            'name': name,
            'semester': semester
        })
    
    return students_data


def generate_sample_attendance_data(student, days_back=30):
    """
    Generate sample attendance records for a student
    """
    attendance_data = []
    today = date.today()
    
    for i in range(days_back):
        record_date = today - timedelta(days=i)
        # Skip weekends (optional - you can remove this)
        if record_date.weekday() < 5:  # Monday to Friday
            status = random.choice(['Present', 'Present', 'Present', 'Absent'])  # 75% present
            attendance_data.append({
                'date': record_date,
                'status': status
            })
    
    return attendance_data


def generate_sample_marks_data(student):
    """
    Generate sample marks data for a student
    """
    # Generate marks between 40-95 with some variation
    marks = round(random.uniform(40, 95), 2)
    return {
        'subject': 'General',
        'marks': marks
    }
