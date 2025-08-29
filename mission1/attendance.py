unique_uniform_num = {}
uniform_num_count = 0

# dat[사용자ID][요일]
attendance_by_day = [[0] * 100 for _ in range(100)]
points = [0] * 100
grade = [0] * 100
player_names = [''] * 100

def calc_attendance_point(attendee_name, attendance_date):
    global uniform_num_count

    uniform_num = get_uniform_num(attendee_name)

    add_point = 0
    day_index = 0

    if attendance_date == "monday":
        day_index = 0
        add_point += 1
    elif attendance_date == "tuesday":
        day_index = 1
        add_point += 1
    elif attendance_date == "wednesday":
        day_index = 2
        add_point += 3
    elif attendance_date == "thursday":
        day_index = 3
        add_point += 1
    elif attendance_date == "friday":
        day_index = 4
        add_point += 1
    elif attendance_date == "saturday":
        day_index = 5
        add_point += 2
    elif attendance_date == "sunday":
        day_index = 6
        add_point += 2

    attendance_by_day[uniform_num][day_index] += 1
    points[uniform_num] += add_point


def get_uniform_num(attendee_name):
    global uniform_num_count
    if attendee_name not in unique_uniform_num:
        uniform_num_count += 1
        unique_uniform_num[attendee_name] = uniform_num_count
        player_names[uniform_num_count] = attendee_name
    uniform_num = unique_uniform_num[attendee_name]
    return uniform_num


def get_attendance_data():
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            lines_data = []
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                lines_data.append(line.strip().split())
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

    return lines_data

def print_remove_player_list():
    print("\nRemoved player")
    print("==============")
    for attendee in range(1, uniform_num_count + 1):
        if grade[attendee] not in (1, 2) and attendance_by_day[attendee][2] == 0 and attendance_by_day[attendee][5] + attendance_by_day[attendee][6] == 0:
            print(player_names[attendee])


def print_player_data(attendee):
    print(f"NAME : {player_names[attendee]}, POINT : {points[attendee]}, GRADE : ", end="")
    if grade[attendee] == 1:
        print("GOLD")
    elif grade[attendee] == 2:
        print("SILVER")
    else:
        print("NORMAL")


def calc_grade(attendee):
    if points[attendee] >= 50:
        grade[attendee] = 1
    elif points[attendee] >= 30:
        grade[attendee] = 2
    else:
        grade[attendee] = 0


def get_bonus_points(attendee):
    if attendance_by_day[attendee][2] > 9:
        points[attendee] += 10
    if attendance_by_day[attendee][5] + attendance_by_day[attendee][6] > 9:
        points[attendee] += 10


if __name__ == "__main__":
    attendance_data = get_attendance_data()

    for attendee_info in attendance_data:
        if len(attendee_info) == 2:
            calc_attendance_point(attendee_info[0], attendee_info[1])

    for attendee in range(1, uniform_num_count + 1):
        get_bonus_points(attendee)
        calc_grade(attendee)
        print_player_data(attendee)

    print_remove_player_list()