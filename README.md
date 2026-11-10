# 🏫 School Management System

A terminal-based **School Management System** built with pure Python (OOP + JSON storage). It manages students, teachers, classes, subjects, attendance, exams, results and fees, and shows a summary dashboard. No external libraries needed.

## ✨ Features

| Module | What it does |
|---|---|
| **Student Management** | Add, view, search, update and delete students with auto-generated IDs |
| **Class Management** | Create classes, assign class teachers, view class students, update and delete |
| **Teacher Management** | Full CRUD for teachers (qualification, subject, salary) |
| **Subject Management** | Assign subjects to classes and teachers with validation |
| **Attendance** | Mark class attendance (Present / Absent / Leave), per-student percentage, date-wise class report |
| **Examination** | Create exams linked to a class and subject |
| **Results** | Enter marks, auto percentage and grade (A+ to F), exam ranking with average / highest / lowest |
| **Fees** | Monthly fee collection, student fee history, pending fee list |
| **Dashboard** | Totals, students per class, today's attendance and fee summary |

## 🛠️ Tech Stack

- **Python 3.8+**
- Standard library only: `json`, `random`, `string`, `datetime`, `pathlib`

## 🚀 How to Run

```bash
# 1. Clone the repository
git clone https://github.com/wahabsiddiqi/School-Management-System.git
cd School-Management-System

# 2. Run the program
python school_management.py
```

`school_data.json` is created automatically on the first run.

## 📋 Main Menu

```
==================================================
       SCHOOL MANAGEMENT SYSTEM
==================================================
1. Student Management
2. Class Management
3. Teacher Management
4. Subject Management
5. Attendance Management
6. Examination Management
7. Result Management
8. Fee Management
9. School Dashboard
0. Exit
```

> **Tip:** Add a class and a teacher first, then subjects, exams and results, because many records depend on them.

## 🧠 How It Works

- All data lives in one dictionary (`self.data`) with 8 lists: `students`, `teachers`, `classes`, `subjects`, `attendance`, `exams`, `results`, `fees`.
- On start, `load_data()` reads `school_data.json` (and handles a missing, empty or corrupt file safely).
- After every change, `save_data()` writes the data back to the file.
- Records are linked by IDs, like foreign keys in a database.

| Record | ID Prefix | Example |
|---|---|---|
| Student | `STU` | `STU48213` |
| Teacher | `TCH` | `TCH10492` |
| Class | `CLS` | `CLS77120` |
| Subject | `SUB` | `SUB30581` |
| Exam | `EXM` | `EXM52047` |
| Result | `RES` | `RES19004` |
| Fee | `FEE` | `FEE66210` |

## ✅ Validation Highlights

- No empty fields, negative ages or invalid numbers
- Duplicate IDs, classes, subjects, results and fee payments are blocked
- Marks must be between 0 and the exam's total marks
- A student can only get a result for an exam of their own class
- A class with students, or a teacher assigned to a class or subject, cannot be deleted
- Dates are validated as `YYYY-MM-DD` and fee months as `YYYY-MM`

## ⚠️ Known Limitations

- JSON file storage is not suitable for large data or multiple users
- Deleting a student does not remove their attendance, results and fee records
- Class existence is not checked when adding or updating a student
- No login system

## 🔮 Future Improvements

- [ ] Streamlit web UI
- [ ] SQLite / PostgreSQL database
- [ ] Cascade delete for linked records
- [ ] Login and user roles
- [ ] Export reports to PDF / Excel

## 👨‍💻 Author

**Wahab** – BS Computer Science student, Data Science enthusiast
GitHub: [@wahabsiddiqi](https://github.com/wahabsiddiqi)

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
