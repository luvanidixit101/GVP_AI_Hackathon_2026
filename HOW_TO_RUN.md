# How to Run the Application

## Step-by-Step Instructions

### Step 1: Open Terminal/Command Prompt
- **Windows**: Press `Win + R`, type `cmd` or `powershell`, press Enter
- **Mac/Linux**: Open Terminal

### Step 2: Navigate to Project Folder
```bash
cd "C:\Users\dixit001\OneDrive\Desktop\New folder"
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note**: If you get an error, try:
```bash
python -m pip install -r requirements.txt
```
or
```bash
pip3 install -r requirements.txt
```

### Step 4: Create Database Tables
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Run the Development Server
```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 6: Open in Browser
- Open your web browser (Chrome, Firefox, Edge, etc.)
- Go to: **http://127.0.0.1:8000/**
- You should see the Smart Attendance Tracker homepage!

## Quick Test

1. **Generate Sample Data** (Recommended first step)
   - Click "Generate Data" in the navigation
   - Enter `5` students
   - Click "Generate Sample Data"
   - This creates test data automatically

2. **View Students**
   - Click "Students" to see the list
   - Click "View Report" on any student

3. **Add a Student**
   - Click "Add Student"
   - Enter: Roll No: `101`, Name: `Rahul Shah`, Semester: `3`
   - Click "Add Student"

## Troubleshooting

### Problem: "python is not recognized"
**Solution**: 
- Make sure Python is installed
- Try `python3` instead of `python`
- Or use full path: `C:\Python39\python.exe manage.py runserver`

### Problem: "pip is not recognized"
**Solution**:
- Install Python from python.org (make sure to check "Add Python to PATH")
- Or use: `python -m pip install -r requirements.txt`

### Problem: "ModuleNotFoundError: No module named 'django'"
**Solution**:
- Run: `pip install django==4.2.7`
- Or: `pip install -r requirements.txt`

### Problem: "Port 8000 already in use"
**Solution**:
- Use a different port: `python manage.py runserver 8001`
- Then access: http://127.0.0.1:8001/

### Problem: "No such table" error
**Solution**:
- Run migrations: `python manage.py migrate`

## Stopping the Server

- Press `Ctrl + C` in the terminal to stop the server

## Next Steps After Running

1. ✅ Generate sample data for testing
2. ✅ Explore all features (Add Student, Mark Attendance, Enter Marks)
3. ✅ View student reports
4. ✅ Test AI features (warnings, remarks)

## Video Guide (Text Version)

```
1. Open Terminal
   ↓
2. cd to project folder
   ↓
3. pip install -r requirements.txt
   ↓
4. python manage.py makemigrations
   ↓
5. python manage.py migrate
   ↓
6. python manage.py runserver
   ↓
7. Open browser → http://127.0.0.1:8000/
   ↓
8. Done! 🎉
```

---

**Need Help?** Check `SETUP_INSTRUCTIONS.md` for more details.
