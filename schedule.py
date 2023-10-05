import os
import csv
from numpy import array, mean, std
from itertools import chain
from copy import deepcopy

blocks = ("b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9")

points = {}
with open("priority points.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        #if int(row[3]) >= 33:
        points[row[1]] = int(row[3])
#print(sorted(points, key=lambda subject: points[subject]))

teachers_classes_all = {
    "t1": {"AP English Language & Composition0", "ELA - 110", "ELA - 111", "ELA - 112"}, 
    "t2": {"ELA - 100", "ELA - 101", "ELA - 102","ELA - 90", "ELA - 91", "ELA - 92"}, 
    "t3": {"AP Macroeconomics0", "AP Microeconomics0", "Economics0", "Marketing(or)Entrepreneurship0", "Introduction to Business(or)Accounting0", "Introduction to Business(or)Accounting1"}, 
    "t4": {"Psychology0", "Psychology1", "AP Psychology0", "AP Research0", "Creative Writing0", "Creative Writing1"}, 
    "t5": {"AP World History0", "Contemporary History0", "Contemporary History1", "Contemporary History2", "Modern History(Jack)0", "Modern History(Jack)1"}, 
    "t6": {"Modern History(Michael)0", "AP Comparative Government & Politics0", "AP Seminar0", "Model UN & Current Issues0"}, 
    "t7": {"AP Biology0", "Advanced Biology0", "Biology0", "Biology1", "Biology2"}, 
    "t8": {"AP Chemistry0", "Chemistry0", "Physical Science0", "Physical Science1", "Physical Science2"}, 
    "t9": {"AP Calculus AB0", "AP Physics C0", "AP Physics0", "Pre-Calculus0", "Pre-Calculus1", "Physics0"}, 
    "t10": {"AP Pre-Calculus0", "Algebra 20", "Algebra 21", "Algebra 1&20", "Algebra 1&21", "Algebra 1&22"}, 
    "t11": {"AP Statistics0", "Statistics0", "Geometry0", "Geometry1", "Geometry2"}, 
    "t12": {"AP Computer Science A0", "Python Programming0",  "Web Design0", "Computer Science0", "Computer Science1", "Computer Science2"}, 
    "t13": {"Music (Senior Band)0", "Music-90"}, 
    "t14": {"AP Studio Art0", "High School Art0", "Art-90", "Art-91", "Art-92"}, 
    "t15": {"Team Sports0", "Sports Leadership0", "Weight Training & Fitness0", "P.E -90", "P.E -91", "P.E -92"}, 
    "t16": {"Spanish 10", "Spanish 20", "Spanish 30", "Spanish 40"}, 
    "t17": {"Japanese 10", "Japanese 20", "Japanese 30", "Japanese 40"}, 
    "t18": {"Chinese 10", "Chinese 20", "Chinese 30", "Chinese 40"}, 
    "t19": {"Thai as an Additional Language0", "Thai as an Additional Language1", "Thai as an Additional Language2", "Thai for Native Speakers0", "Thai for Native Speakers1", "Thai for Native Speakers2"}, 
}
teachers_classes = {
    "t1": {"AP English Language & Composition", "ELA - 12", "ELA - 11"}, 
    "t2": {"ELA - 10", "ELA - 9"}, 
    "t3": {"AP Macroeconomics", "AP Microeconomics", "Economics", "Marketing(or)Entrepreneurship", "Introduction to Business(or)Accounting"}, 
    "t4": {"Psychology", "AP Psychology", "AP Research", "Creative Writing"}, 
    "t5": {"AP World History", "Contemporary History", "Modern History(Jack)"}, 
    "t6": {"Modern History(Michael)", "AP Comparative Government & Politics", "AP Seminar", "Model UN & Current Issues"}, 
    "t7": {"AP Biology", "Advanced Biology", "Biology"}, 
    "t8": {"AP Chemistry", "Chemistry", "Physical Science"}, 
    "t9": {"AP Calculus AB", "AP Physics C", "AP Physics", "Pre-Calculus", "Physics"}, 
    "t10": {"AP Pre-Calculus", "Algebra 2", "Algebra 1&2"}, 
    "t11": {"AP Statistics", "Statistics", "Geometry"}, 
    "t12": {"AP Computer Science A", "Python Programming",  "Web Design", "Computer Science"}, 
    "t13": {"Music (Senior Band)", "Music-9"}, 
    "t14": {"AP Studio Art", "High School Art", "Art-9"}, 
    "t15": {"Team Sports", "Sports Leadership", "Weight Training & Fitness", "P.E -9"}, 
    "t16": {"Spanish 1", "Spanish 2", "Spanish 3", "Spanish 4"}, 
    "t17": {"Japanese 1", "Japanese 2", "Japanese 3", "Japanese 4"}, 
    "t18": {"Chinese 1", "Chinese 2", "Chinese 3", "Chinese 4"}, 
    "t19": {"Thai as an Additional Language", "Thai for Native Speakers"}, 
}

#all_subjects = sorted(chain(*teachers_classes_all.values()), key=lambda subject: points.get(subject[:-1], 0))
subject_points = {subject: points.get(subject[:-1], 1) for subject in chain(*teachers_classes_all.values())}
for subject in subject_points:
    for classes in teachers_classes.values():
        if subject[:-1] in classes:
            subject_points[subject] *= len(classes)
all_subjects = sorted(subject_points, key=lambda subject: subject_points[subject], reverse=True)

students = {}
no = 1
for file in os.listdir("priorities"):
    with open(os.path.join("priorities", file), newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            priorities = list(x for x in row[1:])
            if len(row) > 6:
                students["s" + str(no)] = set(priorities[:-4])
            else:
                students["s" + str(no)] = set(priorities)
            no += 1
#print(mean(list(len(priorities) for priorities in students.values())[:-31]))
#print(students)

def is_complete(assignment):
    return len(list(chain(*assignment.values()))) == len(all_subjects)+1

def choose_var(assignment):
    chosen = blocks[0]
    for block in assignment:
        if len(assignment[block]) < len(assignment[chosen]):
            chosen = block
    return chosen

def is_consistent(assignment):
    for classes in teachers_classes.values():
        for subjects in assignment.values():
            if len(classes.intersection(subjects)) > 1:
                return False
    for priorities in students.values():
        subjects_to_check = priorities.intersection(set(chain(*assignment.values())))
        checked_blocks = set()
        updated = True
        while updated:
            updated = False
            for block, subjects in assignment.items():
                if block in checked_blocks:
                    continue
                overlap = subjects_to_check.intersection(subjects)
                if len(overlap) > 1:
                    continue
                elif len(overlap) == 1:
                    subjects_to_check -= overlap
                    checked_blocks.add(block)
                    updated = True
        if subjects_to_check:
            return False
    return True

def backtracking_search(assignment, assignment_all):
    if is_complete(assignment):
        return assignment
    variable = choose_var(assignment)
    for value in all_subjects:
        value_ = value[:-1]
        if value not in set(chain(*assignment_all.values())) and value_ not in assignment[variable]:
            assignment[variable].add(value_)
            assignment_all[variable].add(value)
            if is_consistent(assignment):
                result = backtracking_search(assignment, assignment_all)
                if result:
                    return result
                assignment[variable].remove(value_)
                assignment_all[variable].remove(value)
                continue
            assignment[variable].remove(value_)
            assignment_all[variable].remove(value)
    return None

assignment = {block: set() for block in blocks}
assignment["b1"].add("ELA - 12")
assignment_all = deepcopy(assignment)
solution = backtracking_search(assignment, assignment_all)
if solution:
    for block, subjects in solution.items():
        print(block, ": ", subjects)
else:
    print("no optimal solution found")
