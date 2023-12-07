#그리디 알고리즘    

comp = 0 # 비교 횟수

def is_conflict(schedule, new_course): # 시간표 충돌 확인용
    for scheduled_course in schedule:
        for scheduled_time in scheduled_course.times:
            for new_time in new_course.times:
                if is_time_overlap(scheduled_time, new_time):
                    return True
    return False

def is_time_overlap(time1, time2):
    global comp
    comp += 1
    return max(time1[0], time2[0]) < min(time1[1], time2[1])        

# 결과 중복 제거용 함수
def delete_duplicate_list(total_schedule):
    # 중복을 제거한 리스트 생성
    unique_times_list = []

    # 중복을 확인하기 위한 집합(set)을 사용
    seen = set()

    for times in total_schedule:
        # times 리스트를 정렬한 문자열을 생성하여 중복 확인
        times_str = str(times)
        if times_str not in seen:
            unique_times_list.append(times)
            seen.add(times_str)
    return unique_times_list

# 학수번호-분반 id 추출 함수
def convert_id(greedy_schedules):
    schedule = []
    for table in greedy_schedules:
        timetable= []
        for time in table:
            timetable.append(time.course_id)
        schedule.append(timetable)
    return schedule


def find_schedule_greedy(desired_courses, times_dict):
    time_list = []

    for course in desired_courses:
        time_list.extend(times_dict[course])

    sorted_time_list = sorted(time_list, key=lambda x: (
        x.times[0][0] if x.times else float('inf'),
        x.times[0][1] if x.times and len(x.times[0]) > 1 else float('inf'),
        len(x.times) == 1,
        x.times[1][0] if len(x.times) > 1 else float('inf')
    ))

    schedule = []
    total_schedule = []
    is_selected = set()

    for start in sorted_time_list:
        start_course_id = start.course_id.split('-')[0]
        schedule.append(start)
        is_selected.add(start_course_id)
        for time in sorted_time_list:
            course_id = time.course_id.split('-')[0]
        
            if course_id in is_selected:
                continue
        
            if not is_conflict(schedule, time): # 시간 충돌이 없을 경우 case 시간표에 추가
                schedule.append(time)
                is_selected.add(course_id)

        if len(schedule) == len(desired_courses):
            schedule.sort(key=lambda x: (
        x.times[0][0] if x.times else float('inf'),
        x.times[0][1] if x.times and len(x.times[0]) > 1 else float('inf'),
        len(x.times) == 1,
        x.times[1][0] if len(x.times) > 1 else float('inf')
        ))
            total_schedule.append(schedule)
        
        schedule = []
        is_selected.clear()

    total_schedule = delete_duplicate_list(total_schedule)
    total_schedule = convert_id(total_schedule)

    return total_schedule
