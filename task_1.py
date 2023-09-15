class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}


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
    pass


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


students_dict = {"name": ["Ruoy", "John", "Emma"], "surname": ["Eman", "Smith", "Watson"],
                 "gender": ["male", "male", "female"]}

reviewers_dict = {"name": ["Frank", "Elvis"], "surname": ["Sinatra", "Presley"], "gender": ["male", "male"]}

courses = ["Python", "Java", "Python"]


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

for stud_obj in zip(students.values(), courses):
    stud_obj[0].courses_in_progress += [stud_obj[1]]

print(students["student_0"].courses_in_progress)

reviewers = cls_inst_maker(Reviewer, reviewers_dict)


# reviewer_1 = Reviewer("Frank", "Sinatra")
# reviewer_1.courses_attached += ["Python"]
#
# cool_mentor.rate_hw(best_student, "Python", 10)
# cool_mentor.rate_hw(best_student, "Python", 10)
# cool_mentor.rate_hw(best_student, "Python", 10)
#
# rew1 = Reviewer("Luydmila", "Postovalova")
# rew1.courses_attached += ["Java"]
# rew1.courses_attached += ["Python"]
#
# print(rew1.__dict__)
