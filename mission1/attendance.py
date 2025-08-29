unique_uniform_num = {}
uniform_num_count = 0

# dat[사용자ID][요일]
data_by_day = [[0] * 100 for _ in range(100)]
points = [0] * 100
grade = [0] * 100
player_names = [''] * 100
wed = [0] * 100
weekend = [0] * 100

def calc_attendance_point(attendee_name, attendance_date):
    global uniform_num_count

    if attendee_name not in unique_uniform_num:
        uniform_num_count += 1
        unique_uniform_num[attendee_name] = uniform_num_count
        player_names[uniform_num_count] = attendee_name

    uniform_num = unique_uniform_num[attendee_name]

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
        wed[uniform_num] += 1
    elif attendance_date == "thursday":
        day_index = 3
        add_point += 1
    elif attendance_date == "friday":
        day_index = 4
        add_point += 1
    elif attendance_date == "saturday":
        day_index = 5
        add_point += 2
        weekend[uniform_num] += 1
    elif attendance_date == "sunday":
        day_index = 6
        add_point += 2
        weekend[uniform_num] += 1

    data_by_day[uniform_num][day_index] += 1
    points[uniform_num] += add_point

def get_eliminate_list():
    try:
        with open("attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                attendee_info = line.strip().split()
                if len(attendee_info) == 2:
                    calc_attendance_point(attendee_info[0], attendee_info[1])

        for i in range(1, uniform_num_count + 1):
            if data_by_day[i][2] > 9:
                points[i] += 10
            if data_by_day[i][5] + data_by_day[i][6] > 9:
                points[i] += 10

            if points[i] >= 50:
                grade[i] = 1
            elif points[i] >= 30:
                grade[i] = 2
            else:
                grade[i] = 0

            print(f"NAME : {player_names[i]}, POINT : {points[i]}, GRADE : ", end="")
            if grade[i] == 1:
                print("GOLD")
            elif grade[i] == 2:
                print("SILVER")
            else:
                print("NORMAL")

        print("\nRemoved player")
        print("==============")
        for i in range(1, uniform_num_count + 1):
            if grade[i] not in (1, 2) and wed[i] == 0 and weekend[i] == 0:
                print(player_names[i])

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    get_eliminate_list()