import openpyxl
from itertools import product
import greedy

class Time:
    def __init__(self, course_id, times):
        self.course_id = course_id
        self.times = times

    def __repr__(self):
        return f"Time({self.course_id}, {self.times})"

class Lecture:
    def __init__(self, course_id, name, instructor, time, classroom):
        self.course_id = course_id
        self.name = name
        self.instructor = instructor
        self.time = time
        self.classroom = classroom

    def __repr__(self):
        return f"Lecture({self.course_id}, {self.name}, {self.instructor}, {self.time}, {self.classroom})"

def get_desired_courses():
    desired_courses = []
    print("원하는 학수강좌번호를 입력하세요. 완료되면 '끝'이라고 입력하세요.")

    while True:
        course_name = input("학수강좌번호: ").strip()
        if course_name.lower() == '끝':
            break
        desired_courses.append(course_name)

    return desired_courses

def convert_time_to_decimal(time_str):
    hours, minutes = map(int, time_str.split(':'))
    decimal_time = float(f"0.{hours}{minutes:02d}")
    return decimal_time

def process_lecture_schedule(file_path):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    lectures_dict = {}
    times_dict = {}
    day_to_num = {'월': 0, '화': 1, '수': 2, '목': 3, '금': 4, '토': 5, '일': 6}

    for row in sheet.iter_rows(min_row=2, values_only=True):
        full_course_id = row[4]
        course_id = full_course_id.split('-')[0]
        name = row[5]
        instructor = row[6]
        time_str = row[8]
        classroom = row[9]

        times = []
        if time_str:
            for part in time_str.split(','):
                day_of_week = day_to_num[part[0]]
                start_time, end_time = part.split('/')[1].split('-')
                times.append([day_of_week + convert_time_to_decimal(start_time), day_of_week + convert_time_to_decimal(end_time)])

        lecture = Lecture(full_course_id, name, instructor, time_str, classroom)
        time = Time(full_course_id, times)

        if course_id not in lectures_dict:
            lectures_dict[course_id] = []
        if course_id not in times_dict:
            times_dict[course_id] = []

        lectures_dict[course_id].append(lecture)
        times_dict[course_id].append(time)

    return lectures_dict, times_dict

def is_time_overlap(time1, time2):
    return max(time1[0], time2[0]) < min(time1[1], time2[1])

def are_times_overlapping(times):
    for i in range(len(times)):
        for j in range(i+1, len(times)):
            if is_time_overlap(times[i], times[j]):
                return True
    return False

def find_schedule(desired_courses, times_dict):
    possible_combinations = product(*(times_dict[course] for course in desired_courses))

    feasible_schedules = []
    for combination in possible_combinations:
        times = [time for lecture_times in combination for time in lecture_times.times]

        if not are_times_overlapping(times):
            feasible_schedules.append([lecture.course_id for lecture in combination])

    return feasible_schedules

def print_schedule_details(schedule, lectures_dict):
    for full_course_id in schedule:
        course_id = full_course_id.split('-')[0]

        for lecture in lectures_dict[course_id]:
            if lecture.course_id == full_course_id:
                print(f"Lecture ID: {lecture.course_id}, Name: {lecture.name}, Instructor: {lecture.instructor}, Time: {lecture.time}, Classroom: {lecture.classroom}")
                break 

file_path = "data.xlsx"
lectures_dict, times_dict = process_lecture_schedule(file_path)
desired_courses = get_desired_courses()
feasible_schedules = find_schedule(desired_courses, times_dict)

if not feasible_schedules:
    print("가능한 시간표가 없습니다.")
else:
    for schedule in feasible_schedules:
        print("--------------------------------")
        print('')
        print_schedule_details(schedule, lectures_dict)
        print('')
        print("--------------------------------")

#그리디 알고리즘
feasible_schedules = greedy.find_schedule_greedy(desired_courses, times_dict)

if not feasible_schedules:
    print("가능한 시간표가 없습니다.")
else:
    for schedule in feasible_schedules:
        print("--------------------------------")
        print('')
        print_schedule_details(schedule, lectures_dict)
        print('')
        print("--------------------------------")
