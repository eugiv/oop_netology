class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lc(self, lecturer, course, grade):
        if(isinstance(lecturer, Lecturer) and course in self.courses_in_progress
                and course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return "Error"

    def __str__(self):
        return (f'Name: {self.name}\n'
                f'Surname: {self.surname}\n'
                f'Courses in progress: {" ".join(self.courses_in_progress)}\n'
                f'Finished courses: {" ".join(self.finished_courses)}')


class Mentor:
    def __init__(self, name, surname, gender, courses_attached=None):
        self.name = name
        self.surname = surname
        self.gender = gender
        if courses_attached is None:
            self.courses_attached = []
        else:
            self.courses_attached = courses_attached


class Lecturer(Mentor):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender, courses_attached=None)
        self.grades = {}

    def __str__(self):
        return (f'Name: {self.name}\n'
                f'Surname: {self.surname}')


class Reviewer(Mentor):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender, courses_attached=None)

    def rate_hw_rew(self, student, course, grade):
        if(isinstance(student, Student) and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return "Error"

    def __str__(self):
        return (f'Name: {self.name}\n'
                f'Surname: {self.surname}')

students_dict = {"name": ["Ruoy", "John", "Emma"], "surname": ["Eman", "Smith", "Watson"],
                 "gender": ["male", "male", "female"]}

reviewers_dict = {"name": ["Frank", "Elvis"], "surname": ["Sinatra", "Presley"], "gender": ["male", "male"]}

lecturer_dict = {"name": ["Harland", "Ronald"], "surname": ["Sanders", "McDonald"], "gender": ["male", "non_binary"]}

initial_course = ["Python", "Java", "Python"]


def cls_inst_maker(cls, data):
    Person = {}
    for key in range(len(data["name"])):
        name = data["name"][key]
        surname = data["surname"][key]
        gender = data["gender"][key]

        person_var = f'{str(cls.__name__).lower()}_{key}'

        person = cls(name, surname, gender)
        Person[person_var] = person
    return Person


students = cls_inst_maker(Student, students_dict)
reviewers = cls_inst_maker(Reviewer, reviewers_dict)
lecturers = cls_inst_maker(Lecturer, lecturer_dict)

# assigning courses to students
for stud_obj in zip(students.values(), initial_course):
    stud_obj[0].courses_in_progress += [stud_obj[1]]

# assigning courses to reviewers
for rew_obj in zip(reviewers.values(), initial_course):
    rew_obj[0].courses_attached += [rew_obj[1]]

# assigning courses to lecturers
for lec_obj in zip(lecturers.values(), initial_course):
    lec_obj[0].courses_attached += [lec_obj[1]]

# adding course to a lecturer manually
lecturers["lecturer_0"].courses_attached += ["Kotlin"]

# reviewers grade students
reviewers["reviewer_0"].rate_hw_rew(students["student_2"], "Python", 10)
reviewers["reviewer_1"].rate_hw_rew(students["student_1"], "Java", 8)

# students grade lecturers
students["student_1"].rate_lc(lecturers["lecturer_1"], "Java", 10)
students["student_2"].rate_lc(lecturers["lecturer_0"], "Python", 9)

print(students["student_1"])
