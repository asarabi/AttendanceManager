import os


class AttendanceSystem:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.unique_uniform_num = {}
        self.uniform_num_count = 0

        # dat[사용자ID][요일]
        self.attendance_by_day = [[0] * 100 for _ in range(100)]
        self.points = [0] * 100
        self.grade = [0] * 100
        self.player_names = [''] * 100
        print("singleton class")

    def calc_attendance_point(self, attendee_name, attendance_date):
        point_table = {'monday': 1, 'tuesday': 1, 'wednesday': 3, 'thursday': 1, 'friday': 1, 'saturday': 2, 'sunday': 2}
        uniform_num = self.get_uniform_num(attendee_name)

        add_point = 0
        day_index = 0

        for index,(weekday, point) in enumerate(point_table.items()):
            if attendance_date == weekday:
                day_index = index
                add_point += point

        self.attendance_by_day[uniform_num][day_index] += 1
        self.points[uniform_num] += add_point


    def get_uniform_num(self, attendee_name):
        if attendee_name not in self.unique_uniform_num:
            self.uniform_num_count += 1
            self.unique_uniform_num[attendee_name] = self.uniform_num_count
            self.player_names[self.uniform_num_count] = attendee_name
        uniform_num = self.unique_uniform_num[attendee_name]
        return uniform_num


    def get_attendance_data(self,file_path=None):
        try:
            lines_data = []
            if file_path is None:
                current_directory = os.getcwd()
                file_name = "attendance_weekday_500.txt"
                file_path = os.path.join(current_directory, file_name)
            print(file_path)

            with open(file_path, encoding='utf-8') as f:
                for _ in range(500):
                    line = f.readline()
                    if not line:
                        break
                    lines_data.append(line.strip().split())
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")

        return lines_data

    def print_remove_player_list(self):
        print("\nRemoved player")
        print("==============")
        for attendee in range(1, self.uniform_num_count + 1):
            if self.grade[attendee] not in (1, 2) and self.attendance_by_day[attendee][2] == 0 and self.attendance_by_day[attendee][5] + self.attendance_by_day[attendee][6] == 0:
                print(self.player_names[attendee])


    def print_player_data(self, attendee):
        print(f"NAME : {self.player_names[attendee]}, POINT : {self.points[attendee]}, GRADE : ", end="")
        if self.grade[attendee] == 1:
            print("GOLD")
        elif self.grade[attendee] == 2:
            print("SILVER")
        else:
            print("NORMAL")


    def calc_grade(self, attendee):
        if self.points[attendee] >= 50:
            self.grade[attendee] = 1
        elif self.points[attendee] >= 30:
            self.grade[attendee] = 2
        else:
            self.grade[attendee] = 0


    def get_bonus_points(self, attendee):
        if self.attendance_by_day[attendee][2] > 9:
            self.points[attendee] += 10
        if self.attendance_by_day[attendee][5] + self.attendance_by_day[attendee][6] > 9:
            self.points[attendee] += 10

    def get_uniform_num_count(self):
        return self.uniform_num_count

if __name__ == "__main__":
    attendace_system = AttendanceSystem()
    attendance_data = attendace_system.get_attendance_data()

    for attendee_info in attendance_data:
        if len(attendee_info) == 2:
            attendace_system.calc_attendance_point(attendee_info[0], attendee_info[1])
    uniform_num_count = attendace_system.get_uniform_num_count()
    for attendee in range(1, uniform_num_count + 1):
        attendace_system.get_bonus_points(attendee)
        attendace_system.calc_grade(attendee)
        attendace_system.print_player_data(attendee)

    attendace_system.print_remove_player_list()