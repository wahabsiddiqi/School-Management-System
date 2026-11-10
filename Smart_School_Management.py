import json
import random
import string
from datetime import datetime
from pathlib import Path


class Student:

    def __init__(self, name, age, father_name, contact, class_name):

        self.student_id = self.generate_id()
        self.name = name
        self.age = age
        self.father_name = father_name
        self.contact = contact
        self.class_name = class_name
        self.admission_date = datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def generate_id():

        return "STU" + ''.join(
            random.choices(string.digits, k=5)
        )

    def to_dict(self):

        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "father_name": self.father_name,
            "contact": self.contact,
            "class_name": self.class_name,
            "admission_date": self.admission_date
        }


class Teacher:

    def __init__(self, name, age, contact, qualification, subject, salary):

        self.teacher_id = self.generate_id()
        self.name = name
        self.age = age
        self.contact = contact
        self.qualification = qualification
        self.subject = subject
        self.salary = salary
        self.joining_date = datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def generate_id():

        return "TCH" + ''.join(
            random.choices(string.digits, k=5)
        )

    def to_dict(self):

        return {
            "teacher_id": self.teacher_id,
            "name": self.name,
            "age": self.age,
            "contact": self.contact,
            "qualification": self.qualification,
            "subject": self.subject,
            "salary": self.salary,
            "joining_date": self.joining_date
        }


class School:

    def __init__(self):

        self.database = "school_data.json"

        self.data = {
            "students": [],
            "teachers": [],
            "classes": [],
            "subjects": [],
            "attendance": [],
            "exams": [],
            "results": [],
            "fees": []
        }

        self.load_data()

    # Load Database

    def load_data(self):

        if Path(self.database).exists():

            with open(self.database, "r") as f:

                content = f.read().strip()

                if content:
                    try:
                        loaded_data = json.loads(content)

                        if isinstance(loaded_data, dict):
                            self.data.update(loaded_data)

                    except json.JSONDecodeError:
                        print("Invalid JSON file! Creating new database.")
                        self.save_data()

                else:
                    self.save_data()

        else:
            self.save_data()

    # Save Database

    def save_data(self):

        with open(self.database, "w") as f:
            json.dump(self.data, f, indent=4)

    # Helper: Generate Unique ID

    def generate_unique_id(self, prefix, collection, key):

        existing_ids = [
            item[key] for item in self.data[collection]
        ]

        while True:

            new_id = prefix + ''.join(
                random.choices(string.digits, k=5)
            )

            if new_id not in existing_ids:
                return new_id

    # Helper: Find Record By Key

    def find_record(self, collection, key, value):

        for record in self.data[collection]:

            if record[key] == value:
                return record

        return None

    # Helper: Get Students Of A Class

    def get_class_students(self, class_name):

        return [
            s for s in self.data["students"]
            if s["class_name"].lower() == class_name.lower()
        ]

    # Helper: Validate Date Input

    def get_valid_date(self, message):

        date_text = input(message).strip()

        if not date_text:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text

        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD.")
            return None

    # Helper: Calculate Grade

    @staticmethod
    def calculate_grade(percentage):

        if percentage >= 90:
            return "A+"

        elif percentage >= 80:
            return "A"

        elif percentage >= 70:
            return "B"

        elif percentage >= 60:
            return "C"

        elif percentage >= 50:
            return "D"

        else:
            return "F"

    # ==================================================
    # STUDENT MANAGEMENT
    # ==================================================

    # Student Management

    def student_management(self):

        while True:

            print("\n" + "=" * 50)
            print("          STUDENT MANAGEMENT")
            print("=" * 50)

            print("1. Add Student")
            print("2. View All Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("0. Back to Main Menu")

            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.view_students()

            elif choice == "3":
                self.search_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.delete_student()

            elif choice == "0":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice! Please try again.")

    # Add Student

    def add_student(self):

        print("\n========== ADD STUDENT ==========")

        name = input("Enter student name: ").strip()

        if not name:
            print("Name cannot be empty!")
            return

        try:
            age = int(input("Enter student age: "))

            if age <= 0:
                print("Age must be positive!")
                return

        except ValueError:
            print("Invalid age!")
            return

        father_name = input("Enter father name: ").strip()
        contact = input("Enter contact number: ").strip()
        class_name = input("Enter class name: ").strip()

        if not father_name or not contact or not class_name:
            print("All fields are required!")
            return

        student = Student(
            name,
            age,
            father_name,
            contact,
            class_name
        )

        # Check duplicate ID

        existing_ids = [
            s["student_id"] for s in self.data["students"]
        ]

        while student.student_id in existing_ids:
            student.student_id = Student.generate_id()

        self.data["students"].append(student.to_dict())

        self.save_data()

        print("\nStudent added successfully!")
        print("Student ID:", student.student_id)

    # View All Students

    def view_students(self):

        print("\n========== ALL STUDENTS ==========")

        students = self.data["students"]

        if not students:
            print("No students found!")
            return

        for student in students:

            print("-" * 40)

            for key, value in student.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

        print("-" * 40)

        print("Total Students:", len(students))

    # Search Student

    def search_student(self):

        print("\n========== SEARCH STUDENT ==========")

        student_id = input("Enter Student ID: ").strip().upper()

        for student in self.data["students"]:

            if student["student_id"] == student_id:

                print("\nStudent Found!")

                for key, value in student.items():
                    print(f"{key.replace('_', ' ').title()}: {value}")

                return

        print("Student not found!")

    # Update Student

    def update_student(self):

        print("\n========== UPDATE STUDENT ==========")

        student_id = input("Enter Student ID: ").strip().upper()

        for student in self.data["students"]:

            if student["student_id"] == student_id:

                print("\nStudent Found!")
                print("Press Enter to keep the old value.")

                name = input(
                    f"Name ({student['name']}): "
                ).strip()

                age = input(
                    f"Age ({student['age']}): "
                ).strip()

                father_name = input(
                    f"Father Name ({student['father_name']}): "
                ).strip()

                contact = input(
                    f"Contact ({student['contact']}): "
                ).strip()

                class_name = input(
                    f"Class ({student['class_name']}): "
                ).strip()

                if name:
                    student["name"] = name

                if age:

                    try:
                        new_age = int(age)

                        if new_age <= 0:
                            print("Age must be positive!")
                            return

                        student["age"] = new_age

                    except ValueError:
                        print("Invalid age!")
                        return

                if father_name:
                    student["father_name"] = father_name

                if contact:
                    student["contact"] = contact

                if class_name:
                    student["class_name"] = class_name

                self.save_data()

                print("\nStudent updated successfully!")

                return

        print("Student not found!")

    # Delete Student

    def delete_student(self):

        print("\n========== DELETE STUDENT ==========")

        student_id = input("Enter Student ID: ").strip().upper()

        for student in self.data["students"]:

            if student["student_id"] == student_id:

                print("Student Name:", student["name"])

                confirm = input(
                    "Are you sure you want to delete? (yes/no): "
                ).strip().lower()

                if confirm == "yes":

                    self.data["students"].remove(student)

                    self.save_data()

                    print("Student deleted successfully!")

                else:
                    print("Deletion cancelled!")

                return

        print("Student not found!")

    # ==================================================
    # CLASS MANAGEMENT
    # ==================================================

    # Class Management

    def class_management(self):

        while True:

            print("\n" + "=" * 50)
            print("           CLASS MANAGEMENT")
            print("=" * 50)

            print("1. Add Class")
            print("2. View All Classes")
            print("3. View Class Students")
            print("4. Update Class")
            print("5. Delete Class")
            print("0. Back to Main Menu")

            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_class()

            elif choice == "2":
                self.view_classes()

            elif choice == "3":
                self.view_class_students()

            elif choice == "4":
                self.update_class()

            elif choice == "5":
                self.delete_class()

            elif choice == "0":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice! Please try again.")

    # Add Class

    def add_class(self):

        print("\n========== ADD CLASS ==========")

        class_name = input("Enter class name: ").strip()

        if not class_name:
            print("Class name cannot be empty!")
            return

        # Check duplicate class name

        for c in self.data["classes"]:

            if c["class_name"].lower() == class_name.lower():
                print("Class already exists!")
                return

        room = input("Enter room number: ").strip()

        if not room:
            print("Room number is required!")
            return

        teacher_id = input(
            "Enter class teacher ID (Enter to skip): "
        ).strip().upper()

        if teacher_id:

            if not self.find_record("teachers", "teacher_id", teacher_id):
                print("Teacher not found! Add the teacher first.")
                return

        class_record = {
            "class_id": self.generate_unique_id("CLS", "classes", "class_id"),
            "class_name": class_name,
            "room": room,
            "class_teacher_id": teacher_id
        }

        self.data["classes"].append(class_record)

        self.save_data()

        print("\nClass added successfully!")
        print("Class ID:", class_record["class_id"])

    # View All Classes

    def view_classes(self):

        print("\n========== ALL CLASSES ==========")

        classes = self.data["classes"]

        if not classes:
            print("No classes found!")
            return

        for c in classes:

            teacher = self.find_record(
                "teachers", "teacher_id", c["class_teacher_id"]
            )

            teacher_name = teacher["name"] if teacher else "Not Assigned"

            total_students = len(self.get_class_students(c["class_name"]))

            print("-" * 40)
            print("Class ID:", c["class_id"])
            print("Class Name:", c["class_name"])
            print("Room:", c["room"])
            print("Class Teacher:", teacher_name)
            print("Total Students:", total_students)

        print("-" * 40)

        print("Total Classes:", len(classes))

    # View Class Students

    def view_class_students(self):

        print("\n========== CLASS STUDENTS ==========")

        class_name = input("Enter class name: ").strip()

        students = self.get_class_students(class_name)

        if not students:
            print("No students found in this class!")
            return

        for student in students:

            print("-" * 40)
            print("Student ID:", student["student_id"])
            print("Name:", student["name"])
            print("Father Name:", student["father_name"])
            print("Contact:", student["contact"])

        print("-" * 40)

        print("Total Students:", len(students))

    # Update Class

    def update_class(self):

        print("\n========== UPDATE CLASS ==========")

        class_id = input("Enter Class ID: ").strip().upper()

        class_record = self.find_record("classes", "class_id", class_id)

        if not class_record:
            print("Class not found!")
            return

        print("\nClass Found!")
        print("Press Enter to keep the old value.")

        room = input(
            f"Room ({class_record['room']}): "
        ).strip()

        teacher_id = input(
            f"Class Teacher ID ({class_record['class_teacher_id'] or 'None'}): "
        ).strip().upper()

        if room:
            class_record["room"] = room

        if teacher_id:

            if not self.find_record("teachers", "teacher_id", teacher_id):
                print("Teacher not found!")
                return

            class_record["class_teacher_id"] = teacher_id

        self.save_data()

        print("\nClass updated successfully!")

    # Delete Class

    def delete_class(self):

        print("\n========== DELETE CLASS ==========")

        class_id = input("Enter Class ID: ").strip().upper()

        class_record = self.find_record("classes", "class_id", class_id)

        if not class_record:
            print("Class not found!")
            return

        # Class with students cannot be deleted

        if self.get_class_students(class_record["class_name"]):
            print("This class still has students! Move them first.")
            return

        print("Class Name:", class_record["class_name"])

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            self.data["classes"].remove(class_record)

            self.save_data()

            print("Class deleted successfully!")

        else:
            print("Deletion cancelled!")

    # ==================================================
    # TEACHER MANAGEMENT
    # ==================================================

    # Teacher Management

    def teacher_management(self):

        while True:

            print("\n" + "=" * 50)
            print("          TEACHER MANAGEMENT")
            print("=" * 50)

            print("1. Add Teacher")
            print("2. View All Teachers")
            print("3. Search Teacher")
            print("4. Update Teacher")
            print("5. Delete Teacher")
            print("0. Back to Main Menu")

            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_teacher()

            elif choice == "2":
                self.view_teachers()

            elif choice == "3":
                self.search_teacher()

            elif choice == "4":
                self.update_teacher()

            elif choice == "5":
                self.delete_teacher()

            elif choice == "0":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice! Please try again.")

    # Add Teacher

    def add_teacher(self):

        print("\n========== ADD TEACHER ==========")

        name = input("Enter teacher name: ").strip()

        if not name:
            print("Name cannot be empty!")
            return

        try:
            age = int(input("Enter teacher age: "))

            if age <= 0:
                print("Age must be positive!")
                return

        except ValueError:
            print("Invalid age!")
            return

        contact = input("Enter contact number: ").strip()
        qualification = input("Enter qualification: ").strip()
        subject = input("Enter main subject: ").strip()

        if not contact or not qualification or not subject:
            print("All fields are required!")
            return

        try:
            salary = float(input("Enter salary: "))

            if salary <= 0:
                print("Salary must be positive!")
                return

        except ValueError:
            print("Invalid salary!")
            return

        teacher = Teacher(
            name,
            age,
            contact,
            qualification,
            subject,
            salary
        )

        # Check duplicate ID

        existing_ids = [
            t["teacher_id"] for t in self.data["teachers"]
        ]

        while teacher.teacher_id in existing_ids:
            teacher.teacher_id = Teacher.generate_id()

        self.data["teachers"].append(teacher.to_dict())

        self.save_data()

        print("\nTeacher added successfully!")
        print("Teacher ID:", teacher.teacher_id)

    # View All Teachers

    def view_teachers(self):

        print("\n========== ALL TEACHERS ==========")

        teachers = self.data["teachers"]

        if not teachers:
            print("No teachers found!")
            return

        for teacher in teachers:

            print("-" * 40)

            for key, value in teacher.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

        print("-" * 40)

        print("Total Teachers:", len(teachers))

    # Search Teacher

    def search_teacher(self):

        print("\n========== SEARCH TEACHER ==========")

        teacher_id = input("Enter Teacher ID: ").strip().upper()

        teacher = self.find_record("teachers", "teacher_id", teacher_id)

        if teacher:

            print("\nTeacher Found!")

            for key, value in teacher.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

            return

        print("Teacher not found!")

    # Update Teacher

    def update_teacher(self):

        print("\n========== UPDATE TEACHER ==========")

        teacher_id = input("Enter Teacher ID: ").strip().upper()

        teacher = self.find_record("teachers", "teacher_id", teacher_id)

        if not teacher:
            print("Teacher not found!")
            return

        print("\nTeacher Found!")
        print("Press Enter to keep the old value.")

        name = input(
            f"Name ({teacher['name']}): "
        ).strip()

        age = input(
            f"Age ({teacher['age']}): "
        ).strip()

        contact = input(
            f"Contact ({teacher['contact']}): "
        ).strip()

        qualification = input(
            f"Qualification ({teacher['qualification']}): "
        ).strip()

        subject = input(
            f"Subject ({teacher['subject']}): "
        ).strip()

        salary = input(
            f"Salary ({teacher['salary']}): "
        ).strip()

        if name:
            teacher["name"] = name

        if age:

            try:
                new_age = int(age)

                if new_age <= 0:
                    print("Age must be positive!")
                    return

                teacher["age"] = new_age

            except ValueError:
                print("Invalid age!")
                return

        if contact:
            teacher["contact"] = contact

        if qualification:
            teacher["qualification"] = qualification

        if subject:
            teacher["subject"] = subject

        if salary:

            try:
                new_salary = float(salary)

                if new_salary <= 0:
                    print("Salary must be positive!")
                    return

                teacher["salary"] = new_salary

            except ValueError:
                print("Invalid salary!")
                return

        self.save_data()

        print("\nTeacher updated successfully!")

    # Delete Teacher

    def delete_teacher(self):

        print("\n========== DELETE TEACHER ==========")

        teacher_id = input("Enter Teacher ID: ").strip().upper()

        teacher = self.find_record("teachers", "teacher_id", teacher_id)

        if not teacher:
            print("Teacher not found!")
            return

        # Teacher assigned to a class or subject cannot be deleted

        for c in self.data["classes"]:

            if c["class_teacher_id"] == teacher_id:
                print("This teacher is a class teacher! Reassign first.")
                return

        for s in self.data["subjects"]:

            if s["teacher_id"] == teacher_id:
                print("This teacher is assigned to a subject! Reassign first.")
                return

        print("Teacher Name:", teacher["name"])

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            self.data["teachers"].remove(teacher)

            self.save_data()

            print("Teacher deleted successfully!")

        else:
            print("Deletion cancelled!")

    # ==================================================
    # SUBJECT MANAGEMENT
    # ==================================================

    # Subject Management

    def subject_management(self):

        while True:

            print("\n" + "=" * 50)
            print("          SUBJECT MANAGEMENT")
            print("=" * 50)

            print("1. Add Subject")
            print("2. View All Subjects")
            print("3. View Class Subjects")
            print("4. Update Subject Teacher")
            print("5. Delete Subject")
            print("0. Back to Main Menu")

            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_subject()

            elif choice == "2":
                self.view_subjects()

            elif choice == "3":
                self.view_class_subjects()

            elif choice == "4":
                self.update_subject()

            elif choice == "5":
                self.delete_subject()

            elif choice == "0":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice! Please try again.")

    # Add Subject

    def add_subject(self):

        print("\n========== ADD SUBJECT ==========")

        subject_name = input("Enter subject name: ").strip()
        class_name = input("Enter class name: ").strip()
        teacher_id = input("Enter teacher ID: ").strip().upper()

        if not subject_name or not class_name or not teacher_id:
            print("All fields are required!")
            return

        # Class and teacher must exist

        class_exists = any(
            c["class_name"].lower() == class_name.lower()
            for c in self.data["classes"]
        )

        if not class_exists:
            print("Class not found! Add the class first.")
            return

        if not self.find_record("teachers", "teacher_id", teacher_id):
            print("Teacher not found! Add the teacher first.")
            return

        # Check duplicate subject in same class

        for s in self.data["subjects"]:

            if (s["subject_name"].lower() == subject_name.lower()
                    and s["class_name"].lower() == class_name.lower()):

                print("This subject already exists in this class!")
                return

        subject = {
            "subject_id": self.generate_unique_id("SUB", "subjects", "subject_id"),
            "subject_name": subject_name,
            "class_name": class_name,
            "teacher_id": teacher_id
        }

        self.data["subjects"].append(subject)

        self.save_data()

        print("\nSubject added successfully!")
        print("Subject ID:", subject["subject_id"])

    # View All Subjects

    def view_subjects(self):

        print("\n========== ALL SUBJECTS ==========")

        subjects = self.data["subjects"]

        if not subjects:
            print("No subjects found!")
            return

        for s in subjects:

            teacher = self.find_record(
                "teachers", "teacher_id", s["teacher_id"]
            )

            teacher_name = teacher["name"] if teacher else "Unknown"

            print("-" * 40)
            print("Subject ID:", s["subject_id"])
            print("Subject Name:", s["subject_name"])
            print("Class:", s["class_name"])
            print("Teacher:", teacher_name)

        print("-" * 40)

        print("Total Subjects:", len(subjects))

    # View Class Subjects

    def view_class_subjects(self):

        print("\n========== CLASS SUBJECTS ==========")

        class_name = input("Enter class name: ").strip()

        subjects = [
            s for s in self.data["subjects"]
            if s["class_name"].lower() == class_name.lower()
        ]

        if not subjects:
            print("No subjects found for this class!")
            return

        for s in subjects:

            teacher = self.find_record(
                "teachers", "teacher_id", s["teacher_id"]
            )

            teacher_name = teacher["name"] if teacher else "Unknown"

            print("-" * 40)
            print("Subject ID:", s["subject_id"])
            print("Subject Name:", s["subject_name"])
            print("Teacher:", teacher_name)

        print("-" * 40)

        print("Total Subjects:", len(subjects))

    # Update Subject Teacher

    def update_subject(self):

        print("\n========== UPDATE SUBJECT ==========")

        subject_id = input("Enter Subject ID: ").strip().upper()

        subject = self.find_record("subjects", "subject_id", subject_id)

        if not subject:
            print("Subject not found!")
            return

        print("\nSubject Found!")
        print("Press Enter to keep the old value.")

        teacher_id = input(
            f"Teacher ID ({subject['teacher_id']}): "
        ).strip().upper()

        if teacher_id:

            if not self.find_record("teachers", "teacher_id", teacher_id):
                print("Teacher not found!")
                return

            subject["teacher_id"] = teacher_id

        self.save_data()

        print("\nSubject updated successfully!")

    # Delete Subject

    def delete_subject(self):

        print("\n========== DELETE SUBJECT ==========")

        subject_id = input("Enter Subject ID: ").strip().upper()

        subject = self.find_record("subjects", "subject_id", subject_id)

        if not subject:
            print("Subject not found!")
            return

        print("Subject Name:", subject["subject_name"])

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            self.data["subjects"].remove(subject)

            self.save_data()

            print("Subject deleted successfully!")

        else:
            print("Deletion cancelled!")

    # ==================================================
    # ATTENDANCE MANAGEMENT
    # ==================================================

    # Attendance Management

    def attendance_management(self):

        while True:

            print("\n" + "=" * 50)
            print("         ATTENDANCE MANAGEMENT")
            print("=" * 50)

            print("1. Mark Class Attendance")
            print("2. View Student Attendance")
            print("3. View Class Attendance By Date")
            print("0. Back to Main Menu")

            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.mark_attendance()

            elif choice == "2":
                self.view_student_attendance()

            elif choice == "3":
                self.view_class_attendance()

            elif choice == "0":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice! Please try again.")

    # Mark Class Attendance

    def mark_attendance(self):

        print("\n========== MARK ATTENDANCE ==========")

        class_name = input("Enter class name: ").strip()

        students = self.get_class_students(class_name)

        if not students:
            print("No students found in this class!")
            return

        date = self.get_valid_date(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        )

        if not date:
            return

        # Check if attendance is already marked

        for record in self.data["attendance"]:

            if (record["date"] == date
                    and record["class_name"].lower() == class_name.lower()):

                print("Attendance already marked for this class on", date)
                return

        status_map = {
            "P": "Present",
            "A": "Absent",
            "L": "Leave"
        }

        print("\nP = Present, A = Absent, L = Leave\n")

        for student in students:

            while True:

                status = input(
                    f"{student['student_id']} - {student['name']} (P/A/L): "
                ).strip().upper()

                if status in status_map:
                    break

                print("Invalid input! Enter P, A or L.")

            self.data["attendance"].append({
                "date": date,
                "class_name": student["class_name"],
                "student_id": student["student_id"],
                "student_name": student["name"],
                "status": status_map[status]
            })

        self.save_data()

        print("\nAttendance marked successfully!")

    # View Student Attendance

    def view_student_attendance(self):

        print("\n========== STUDENT ATTENDANCE ==========")

        student_id = input("Enter Student ID: ").strip().upper()

        student = self.find_record("students", "student_id", student_id)

        if not student:
            print("Student not found!")
            return

        records = [
            a for a in self.data["attendance"]
            if a["student_id"] == student_id
        ]

        if not records:
            print("No attendance records found!")
            return

        print("\nStudent Name:", student["name"])
        print("-" * 40)

        for record in records:
            print(f"{record['date']}  -  {record['status']}")

        print("-" * 40)

        present = sum(1 for r in records if r["status"] == "Present")
        absent = sum(1 for r in records if r["status"] == "Absent")
        leave = sum(1 for r in records if r["status"] == "Leave")

        percentage = (present / len(records)) * 100

        print("Total Days:", len(records))
        print("Present:", present)
        print("Absent:", absent)
        print("Leave:", leave)
        print(f"Attendance Percentage: {percentage:.2f}%")

    # View Class Attendance By Date

    def view_class_attendance(self):

        print("\n========== CLASS ATTENDANCE ==========")

        class_name = input("Enter class name: ").strip()

        date = self.get_valid_date(
            "Enter date (YYYY-MM-DD) or press Enter for today: "
        )

        if not date:
            return

        records = [
            a for a in self.data["attendance"]
            if a["date"] == date
            and a["class_name"].lower() == class_name.lower()
        ]

        if not records:
            print("No attendance found for this class on", date)
            return

        print("\nClass:", class_name)
        print("Date:", date)
        print("-" * 40)

        for record in records:

            print(
                f"{record['student_id']} - "
                f"{record['student_name']}: {record['status']}"
            )

        print("-" * 40)

        present = sum(1 for r in records if r["status"] == "Present")
        absent = sum(1 for r in records if r["status"] == "Absent")
        leave = sum(1 for r in records if r["status"] == "Leave")

        print("Present:", present)
        print("Absent:", absent)
        print("Leave:", leave)

    # ==================================================
    # EXAMINATION MANAGEMENT
    # ==================================================

    # Examination Management

    def examination_management(self):

        while True:

            print("\n" + "=" * 50)
            print("        EXAMINATION MANAGEMENT")
            print("=" * 50)

            print("1. Add Exam")
            print("2. View All Exams")
            print("3. Delete Exam")
            print("0. Back to Main Menu")

            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_exam()

            elif choice == "2":
                self.view_exams()

            elif choice == "3":
                self.delete_exam()

            elif choice == "0":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice! Please try again.")

    # Add Exam

    def add_exam(self):

        print("\n========== ADD EXAM ==========")

        exam_name = input("Enter exam name (e.g. Midterm): ").strip()
        class_name = input("Enter class name: ").strip()
        subject_name = input("Enter subject name: ").strip()

        if not exam_name or not class_name or not subject_name:
            print("All fields are required!")
            return

        # Subject must exist in the given class

        subject_exists = any(
            s["subject_name"].lower() == subject_name.lower()
            and s["class_name"].lower() == class_name.lower()
            for s in self.data["subjects"]
        )

        if not subject_exists:
            print("This subject does not exist in this class!")
            return

        try:
            total_marks = int(input("Enter total marks: "))

            if total_marks <= 0:
                print("Total marks must be positive!")
                return

        except ValueError:
            print("Invalid total marks!")
            return

        exam_date = self.get_valid_date(
            "Enter exam date (YYYY-MM-DD) or press Enter for today: "
        )

        if not exam_date:
            return

        exam = {
            "exam_id": self.generate_unique_id("EXM", "exams", "exam_id"),
            "exam_name": exam_name,
            "class_name": class_name,
            "subject_name": subject_name,
            "total_marks": total_marks,
            "exam_date": exam_date
        }

        self.data["exams"].append(exam)

        self.save_data()

        print("\nExam added successfully!")
        print("Exam ID:", exam["exam_id"])

    # View All Exams

    def view_exams(self):

        print("\n========== ALL EXAMS ==========")

        exams = self.data["exams"]

        if not exams:
            print("No exams found!")
            return

        for exam in exams:

            print("-" * 40)

            for key, value in exam.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

        print("-" * 40)

        print("Total Exams:", len(exams))

    # Delete Exam

    def delete_exam(self):

        print("\n========== DELETE EXAM ==========")

        exam_id = input("Enter Exam ID: ").strip().upper()

        exam = self.find_record("exams", "exam_id", exam_id)

        if not exam:
            print("Exam not found!")
            return

        print("Exam:", exam["exam_name"], "-", exam["subject_name"])
        print("Note: All results of this exam will also be deleted.")

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            self.data["exams"].remove(exam)

            # Remove linked results

            self.data["results"] = [
                r for r in self.data["results"]
                if r["exam_id"] != exam_id
            ]

            self.save_data()

            print("Exam deleted successfully!")

        else:
            print("Deletion cancelled!")

    # ==================================================
    # RESULT MANAGEMENT
    # ==================================================

    # Result Management

    def result_management(self):

        while True:

            print("\n" + "=" * 50)
            print("           RESULT MANAGEMENT")
            print("=" * 50)

            print("1. Add Result")
            print("2. View Student Results")
            print("3. View Exam Results")
            print("4. Delete Result")
            print("0. Back to Main Menu")

            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_result()

            elif choice == "2":
                self.view_student_results()

            elif choice == "3":
                self.view_exam_results()

            elif choice == "4":
                self.delete_result()

            elif choice == "0":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice! Please try again.")

    # Add Result

    def add_result(self):

        print("\n========== ADD RESULT ==========")

        exam_id = input("Enter Exam ID: ").strip().upper()

        exam = self.find_record("exams", "exam_id", exam_id)

        if not exam:
            print("Exam not found!")
            return

        student_id = input("Enter Student ID: ").strip().upper()

        student = self.find_record("students", "student_id", student_id)

        if not student:
            print("Student not found!")
            return

        # Student must belong to the exam's class

        if student["class_name"].lower() != exam["class_name"].lower():
            print("This student is not in the class of this exam!")
            return

        # Check duplicate result

        for r in self.data["results"]:

            if r["exam_id"] == exam_id and r["student_id"] == student_id:
                print("Result already added for this student!")
                return

        try:
            obtained_marks = float(
                input(f"Enter obtained marks (out of {exam['total_marks']}): ")
            )

            if obtained_marks < 0 or obtained_marks > exam["total_marks"]:
                print("Marks must be between 0 and", exam["total_marks"])
                return

        except ValueError:
            print("Invalid marks!")
            return

        percentage = (obtained_marks / exam["total_marks"]) * 100

        result = {
            "result_id": self.generate_unique_id("RES", "results", "result_id"),
            "exam_id": exam_id,
            "exam_name": exam["exam_name"],
            "subject_name": exam["subject_name"],
            "student_id": student_id,
            "student_name": student["name"],
            "total_marks": exam["total_marks"],
            "obtained_marks": obtained_marks,
            "percentage": round(percentage, 2),
            "grade": self.calculate_grade(percentage)
        }

        self.data["results"].append(result)

        self.save_data()

        print("\nResult added successfully!")
        print(f"Percentage: {result['percentage']}%  Grade: {result['grade']}")

    # View Student Results

    def view_student_results(self):

        print("\n========== STUDENT RESULTS ==========")

        student_id = input("Enter Student ID: ").strip().upper()

        student = self.find_record("students", "student_id", student_id)

        if not student:
            print("Student not found!")
            return

        results = [
            r for r in self.data["results"]
            if r["student_id"] == student_id
        ]

        if not results:
            print("No results found for this student!")
            return

        print("\nStudent Name:", student["name"])
        print("-" * 40)

        total_obtained = 0
        total_marks = 0

        for r in results:

            print("Result ID:", r["result_id"])
            print("Exam:", r["exam_name"])
            print("Subject:", r["subject_name"])
            print(f"Marks: {r['obtained_marks']} / {r['total_marks']}")
            print(f"Percentage: {r['percentage']}%")
            print("Grade:", r["grade"])
            print("-" * 40)

            total_obtained += r["obtained_marks"]
            total_marks += r["total_marks"]

        overall = (total_obtained / total_marks) * 100

        print(f"Overall: {total_obtained} / {total_marks}")
        print(f"Overall Percentage: {overall:.2f}%")
        print("Overall Grade:", self.calculate_grade(overall))

    # View Exam Results

    def view_exam_results(self):

        print("\n========== EXAM RESULTS ==========")

        exam_id = input("Enter Exam ID: ").strip().upper()

        exam = self.find_record("exams", "exam_id", exam_id)

        if not exam:
            print("Exam not found!")
            return

        results = [
            r for r in self.data["results"]
            if r["exam_id"] == exam_id
        ]

        if not results:
            print("No results found for this exam!")
            return

        # Sort by obtained marks (highest first)

        results.sort(key=lambda r: r["obtained_marks"], reverse=True)

        print("\nExam:", exam["exam_name"])
        print("Subject:", exam["subject_name"])
        print("Class:", exam["class_name"])
        print("-" * 50)

        for position, r in enumerate(results, start=1):

            print(
                f"{position}. {r['student_name']} ({r['student_id']}) - "
                f"{r['obtained_marks']}/{r['total_marks']} - "
                f"{r['percentage']}% - {r['grade']}"
            )

        print("-" * 50)

        average = sum(r["obtained_marks"] for r in results) / len(results)

        print("Total Students:", len(results))
        print(f"Average Marks: {average:.2f}")
        print("Highest Marks:", results[0]["obtained_marks"])
        print("Lowest Marks:", results[-1]["obtained_marks"])

    # Delete Result

    def delete_result(self):

        print("\n========== DELETE RESULT ==========")

        result_id = input("Enter Result ID: ").strip().upper()

        result = self.find_record("results", "result_id", result_id)

        if not result:
            print("Result not found!")
            return

        print("Student:", result["student_name"])
        print("Exam:", result["exam_name"], "-", result["subject_name"])

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            self.data["results"].remove(result)

            self.save_data()

            print("Result deleted successfully!")

        else:
            print("Deletion cancelled!")

    # ==================================================
    # FEE MANAGEMENT
    # ==================================================

    # Fee Management

    def fee_management(self):

        while True:

            print("\n" + "=" * 50)
            print("             FEE MANAGEMENT")
            print("=" * 50)

            print("1. Collect Fee")
            print("2. View All Fee Records")
            print("3. View Student Fee History")
            print("4. View Pending Fees")
            print("5. Delete Fee Record")
            print("0. Back to Main Menu")

            print("-" * 50)

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.collect_fee()

            elif choice == "2":
                self.view_fees()

            elif choice == "3":
                self.view_student_fees()

            elif choice == "4":
                self.view_pending_fees()

            elif choice == "5":
                self.delete_fee()

            elif choice == "0":
                print("Returning to Main Menu...")
                break

            else:
                print("Invalid choice! Please try again.")

    # Collect Fee

    def collect_fee(self):

        print("\n========== COLLECT FEE ==========")

        student_id = input("Enter Student ID: ").strip().upper()

        student = self.find_record("students", "student_id", student_id)

        if not student:
            print("Student not found!")
            return

        month = input("Enter month (YYYY-MM): ").strip()

        try:
            datetime.strptime(month, "%Y-%m")

        except ValueError:
            print("Invalid month format! Use YYYY-MM.")
            return

        # Check duplicate payment for the same month

        for fee in self.data["fees"]:

            if fee["student_id"] == student_id and fee["month"] == month:
                print("Fee already paid for this month!")
                return

        try:
            amount = float(input("Enter fee amount: "))

            if amount <= 0:
                print("Amount must be positive!")
                return

        except ValueError:
            print("Invalid amount!")
            return

        fee = {
            "fee_id": self.generate_unique_id("FEE", "fees", "fee_id"),
            "student_id": student_id,
            "student_name": student["name"],
            "class_name": student["class_name"],
            "month": month,
            "amount": amount,
            "paid_date": datetime.now().strftime("%Y-%m-%d")
        }

        self.data["fees"].append(fee)

        self.save_data()

        print("\nFee collected successfully!")
        print("Fee ID:", fee["fee_id"])

    # View All Fee Records

    def view_fees(self):

        print("\n========== ALL FEE RECORDS ==========")

        fees = self.data["fees"]

        if not fees:
            print("No fee records found!")
            return

        for fee in fees:

            print("-" * 40)

            for key, value in fee.items():
                print(f"{key.replace('_', ' ').title()}: {value}")

        print("-" * 40)

        total = sum(fee["amount"] for fee in fees)

        print("Total Records:", len(fees))
        print("Total Collected:", total)

    # View Student Fee History

    def view_student_fees(self):

        print("\n========== STUDENT FEE HISTORY ==========")

        student_id = input("Enter Student ID: ").strip().upper()

        student = self.find_record("students", "student_id", student_id)

        if not student:
            print("Student not found!")
            return

        fees = [
            f for f in self.data["fees"]
            if f["student_id"] == student_id
        ]

        if not fees:
            print("No fee records found for this student!")
            return

        print("\nStudent Name:", student["name"])
        print("-" * 40)

        for fee in fees:

            print(
                f"{fee['month']}  -  {fee['amount']}  "
                f"(Paid on {fee['paid_date']})"
            )

        print("-" * 40)

        print("Total Paid:", sum(f["amount"] for f in fees))

    # View Pending Fees

    def view_pending_fees(self):

        print("\n========== PENDING FEES ==========")

        month = input("Enter month (YYYY-MM): ").strip()

        try:
            datetime.strptime(month, "%Y-%m")

        except ValueError:
            print("Invalid month format! Use YYYY-MM.")
            return

        paid_ids = [
            f["student_id"] for f in self.data["fees"]
            if f["month"] == month
        ]

        pending = [
            s for s in self.data["students"]
            if s["student_id"] not in paid_ids
        ]

        if not pending:
            print("No pending fees for", month)
            return

        print("\nPending students for", month)
        print("-" * 40)

        for student in pending:

            print(
                f"{student['student_id']} - {student['name']} "
                f"({student['class_name']})"
            )

        print("-" * 40)

        print("Total Pending:", len(pending))

    # Delete Fee Record

    def delete_fee(self):

        print("\n========== DELETE FEE RECORD ==========")

        fee_id = input("Enter Fee ID: ").strip().upper()

        fee = self.find_record("fees", "fee_id", fee_id)

        if not fee:
            print("Fee record not found!")
            return

        print("Student:", fee["student_name"])
        print("Month:", fee["month"])
        print("Amount:", fee["amount"])

        confirm = input(
            "Are you sure you want to delete? (yes/no): "
        ).strip().lower()

        if confirm == "yes":

            self.data["fees"].remove(fee)

            self.save_data()

            print("Fee record deleted successfully!")

        else:
            print("Deletion cancelled!")

    # ==================================================
    # SCHOOL DASHBOARD
    # ==================================================

    # School Dashboard

    def school_dashboard(self):

        print("\n" + "=" * 50)
        print("            SCHOOL DASHBOARD")
        print("=" * 50)

        today = datetime.now().strftime("%Y-%m-%d")
        current_month = datetime.now().strftime("%Y-%m")

        print("Total Students :", len(self.data["students"]))
        print("Total Teachers :", len(self.data["teachers"]))
        print("Total Classes  :", len(self.data["classes"]))
        print("Total Subjects :", len(self.data["subjects"]))
        print("Total Exams    :", len(self.data["exams"]))
        print("Total Results  :", len(self.data["results"]))

        print("-" * 50)

        # Students per class

        print("Students Per Class:")

        if not self.data["classes"]:
            print("  No classes found!")

        for c in self.data["classes"]:

            count = len(self.get_class_students(c["class_name"]))

            print(f"  {c['class_name']}: {count}")

        print("-" * 50)

        # Today's attendance

        today_records = [
            a for a in self.data["attendance"]
            if a["date"] == today
        ]

        present = sum(1 for r in today_records if r["status"] == "Present")
        absent = sum(1 for r in today_records if r["status"] == "Absent")
        leave = sum(1 for r in today_records if r["status"] == "Leave")

        print("Today's Attendance:")
        print("  Present:", present)
        print("  Absent :", absent)
        print("  Leave  :", leave)

        print("-" * 50)

        # Fee summary

        total_collected = sum(f["amount"] for f in self.data["fees"])

        month_collected = sum(
            f["amount"] for f in self.data["fees"]
            if f["month"] == current_month
        )

        paid_ids = [
            f["student_id"] for f in self.data["fees"]
            if f["month"] == current_month
        ]

        pending_count = len([
            s for s in self.data["students"]
            if s["student_id"] not in paid_ids
        ])

        print("Fee Summary:")
        print("  Total Collected     :", total_collected)
        print(f"  Collected ({current_month}) :", month_collected)
        print(f"  Pending Students    :", pending_count)

        print("=" * 50)


# Main Program

def main():

    school = School()

    while True:

        print("\n" + "=" * 50)
        print("       SCHOOL MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Student Management")
        print("2. Class Management")
        print("3. Teacher Management")
        print("4. Subject Management")
        print("5. Attendance Management")
        print("6. Examination Management")
        print("7. Result Management")
        print("8. Fee Management")
        print("9. School Dashboard")
        print("0. Exit")

        print("-" * 50)

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            school.student_management()

        elif choice == "2":
            school.class_management()

        elif choice == "3":
            school.teacher_management()

        elif choice == "4":
            school.subject_management()

        elif choice == "5":
            school.attendance_management()

        elif choice == "6":
            school.examination_management()

        elif choice == "7":
            school.result_management()

        elif choice == "8":
            school.fee_management()

        elif choice == "9":
            school.school_dashboard()

        elif choice == "0":
            print("Thank you for using School Management System. Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()