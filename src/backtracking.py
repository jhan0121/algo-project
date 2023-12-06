#백트래킹 알고리즘(DFS)
def find_schedule_backtracking(desired_courses, times_dict, schedule=[], all_schedules=[]):
    if len(schedule) == len(desired_courses): # 사용자가 입력한 학수번호를 모두 충족할 경우,
        all_schedules.append(schedule[:]) # 최종 시간표 리스트에 추가
        return

    current_course = desired_courses[len(schedule)] # 분반 중복 없이 선택
    for time in times_dict[current_course]:
        if not is_conflict(schedule, time): # 시간 충돌이 없을 경우 case 시간표에 추가
            schedule.append(time)
            find_schedule_backtracking(desired_courses, times_dict, schedule, all_schedules)
            schedule.pop()

def is_conflict(schedule, new_course): # 시간표 충돌 확인용
    for scheduled_course in schedule:
        for scheduled_time in scheduled_course.times:
            for new_time in new_course.times:
                if is_time_overlap(scheduled_time, new_time):
                    return True
    return False

def is_time_overlap(time1, time2):
    return max(time1[0], time2[0]) < min(time1[1], time2[1])

# time 클래스로 저장된 결과를 id로 변환
def convert_id(backtracking_schedules):
    schedule = []
    for table in backtracking_schedules:
        timetable= []
        for time in table:
            timetable.append(time.course_id)
        schedule.append(timetable)
    return schedule