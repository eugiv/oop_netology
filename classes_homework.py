import random


# global function to calculate average values where it needed
def avg_grade_glob(grades):
    ttl_sum = 0
    ppl_count = 0
    for key, val in grades.items():
        if isinstance(val, list):
            ttl_sum += sum(val)
            ppl_count += len(val)
        else:
            print("Wrong data structure")
    avg_gr = ttl_sum / ppl_count
    avg_gr = round(avg_gr, 2)
    return avg_gr


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
                lecturer.grades[course] += grade
            else:
                lecturer.grades[course] = grade
        else:
            return "Error"

    # def avg_grades(self):
    #     return avg_grade_glob(self.grades) # replaced with magic func below

    def __lt__(self, other):
        return avg_grade_glob(self.grades) < avg_grade_glob(other.grades)

    def __str__(self):
        return (f'Name: {self.name}\n'
                f'Surname: {self.surname}\n'
                f'Average homework grades: {avg_grade_glob(self.grades)}\n'
                f'Courses in progress: {", ".join(self.courses_in_progress)}\n'
                f'Finished courses: {", ".join(self.finished_courses)}')


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

    # def avg_grades(self):
    #     return avg_grade_glob(self.grades) # replaced with magic func below

    def __lt__(self, other):
        return avg_grade_glob(self.grades) < avg_grade_glob(other.grades)

    def __str__(self):
        return (f'Name: {self.name}\n'
                f'Surname: {self.surname}\n'
                f'Average lecturers grade: {avg_grade_glob(self.grades)}')


class Reviewer(Mentor):
    def __init__(self, name, surname, gender):
        super().__init__(name, surname, gender, courses_attached=None)

    def rate_hw_rew(self, student, course, grade):
        if(isinstance(student, Student) and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += grade
            else:
                student.grades[course] = grade
        else:
            return "Error"

    def __str__(self):
        return (f'Name: {self.name}\n'
                f'Surname: {self.surname}')


students_dict = {"name": ["Ruoy", "John", "Emma", "Elton"], "surname": ["Eman", "Smith", "Watson", "John"],
                 "gender": ["male", "male", "female", "male"]}

reviewers_dict = {"name": ["Frank", "Elvis", "Morgan"], "surname": ["Sinatra", "Presley", "Freeman"],
                  "gender": ["male", "male", "male"]}

lecturer_dict = {"name": ["Harland", "Ronald", "Marge"], "surname": ["Sanders", "McDonald", "Simpson"],
                 "gender": ["male", "non_binary", "female"]}

initial_course = ["Python", "Java", "Python", "Kotlin"]


# custom functions
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


def random_grades(begin, end, k):
    return random.choices(range(begin, end), k=k)


def assign_courses_progress(persons: dict, init_course: list):
    for obj in zip(persons.values(), init_course):
        obj[0].courses_in_progress += [obj[1]]


def assign_courses_attached(persons: dict, init_course: list):
    for obj in zip(persons.values(), init_course):
        obj[0].courses_attached += [obj[1]]


# creating class instances
students = cls_inst_maker(Student, students_dict)
reviewers = cls_inst_maker(Reviewer, reviewers_dict)
lecturers = cls_inst_maker(Lecturer, lecturer_dict)

# assigning basic course to students
assign_courses_progress(students, initial_course)

# assigning basic course to reviewers
assign_courses_attached(reviewers, initial_course)

# assigning basic course to lecturers
assign_courses_attached(lecturers, initial_course)

# manual courses adding
students["student_1"].finished_courses += ["Introduction to Docker"]
students["student_3"].finished_courses += ["Advanced Git"]
students["student_3"].courses_in_progress += ["Java"]
lecturers["lecturer_0"].courses_attached += ["Kotlin", "Java"]
lecturers["lecturer_2"].courses_attached += ["Kotlin"]
reviewers["reviewer_1"].courses_attached += ["Kotlin", "Python"]

# reviewers grade students
reviewers["reviewer_0"].rate_hw_rew(students["student_2"], "Python", random_grades(3, 10, 10))
reviewers["reviewer_1"].rate_hw_rew(students["student_1"], "Java", random_grades(3, 10, 20))
reviewers["reviewer_1"].rate_hw_rew(students["student_3"], "Java", random_grades(3, 10, 15))
reviewers["reviewer_1"].rate_hw_rew(students["student_3"], "Kotlin", random_grades(3, 10, 15))
reviewers["reviewer_2"].rate_hw_rew(students["student_0"], "Python", random_grades(3, 10, 25))

# students grade lecturers
students["student_1"].rate_lc(lecturers["lecturer_1"], "Java", random_grades(3, 10, 10))
students["student_2"].rate_lc(lecturers["lecturer_0"], "Python", random_grades(3, 10, 15))
students["student_3"].rate_lc(lecturers["lecturer_2"], "Kotlin", random_grades(3, 10, 10))
students["student_0"].rate_lc(lecturers["lecturer_2"], "Python", random_grades(3, 10, 10))


# grades comparison
def grades_compare(person1, person2):
    if person1 < person2:
        print(f"{person1.surname} has better average grades than {person2.surname}", "\n")
    else:
        print(f"{person2.surname} has better average grades than {person1.surname}", "\n")


# comparing students average grades
grades_compare(students["student_0"], students["student_1"])

# comparing students average grades
grades_compare(lecturers["lecturer_2"], lecturers["lecturer_1"])


# field test
courses_list = ["Java", "Kotlin"]


def job_avg_grade(course_name: list, persons: dict) -> float:
    persons_on_course = {}
    for key, pers in persons.items():
        for crs in course_name:
            if crs in pers.grades.keys():
                persons_on_course[key] = pers.grades[crs]
    print(persons_on_course)

    return avg_grade_glob(persons_on_course)


print("STUDENT:")
print("-----------")
print(students["student_3"], "\n")
print("LECTURER:")
print("-----------")
print(lecturers["lecturer_1"], "\n")
print("REVIEWER:")
print("-----------")
print(reviewers["reviewer_0"], "\n")

if len(courses_list) > 1:
    course_qty = "courses"
else:
    course_qty = "course"

print(f"Average students grade by {', '.join(courses_list)} {course_qty}: ",
      job_avg_grade(courses_list, students), "\n")
print(f"Average lecturers grade by {', '.join(courses_list)} {course_qty}: ",
      job_avg_grade(courses_list, lecturers), "\n")
