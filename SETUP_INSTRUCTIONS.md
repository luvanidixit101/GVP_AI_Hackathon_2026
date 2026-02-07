# Quick Setup Instructions

## Step-by-Step Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. (Optional) Create Admin User
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 4. Run the Server
```bash
python manage.py runserver
```

### 5. Access the Application
- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## Quick Start Testing

1. **Generate Sample Data**
   - Go to "Generate Data" in the navigation
   - Enter 5 students
   - Click "Generate Sample Data"
   - This creates students with attendance and marks

2. **View Students**
   - Click "Students" to see the list
   - Click "View Report" on any student to see details

3. **Add a New Student**
   - Click "Add Student"
   - Enter: Roll No: `101`, Name: `Rahul Shah`, Semester: `3`
   - Click "Add Student"

4. **Mark Attendance**
   - Go to "Attendance"
   - Enter Roll No: `101`
   - Select date and status
   - Click "Mark Attendance"

5. **Enter Marks**
   - Go to "Marks"
   - Enter Roll No: `101`
   - Enter marks: `72`
   - Click "Save Marks"

6. **View Report**
   - Go to "Students"
   - Click "View Report" on student 101
   - See attendance percentage, marks, and AI-generated remarks

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution**: Make sure you've installed requirements:
```bash
pip install -r requirements.txt
```

### Issue: No such table error
**Solution**: Run migrations:
```bash
python manage.py migrate
```

### Issue: Port already in use
**Solution**: Use a different port:
```bash
python manage.py runserver 8001
```

## Features to Test

✅ Student Management
✅ Attendance Tracking
✅ Marks Entry
✅ AI-Generated Warnings
✅ Performance Remarks
✅ Sample Data Generation
