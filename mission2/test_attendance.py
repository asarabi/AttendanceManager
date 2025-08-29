import os

import pytest

from attendance import AttendanceSystem, GoldSilverGrade
@pytest.fixture
def txt_file_right_path(request):
    current_directory = os.getcwd()
    file_name = "attendance_weekday_500.txt"
    return  os.path.join(current_directory, 'mission2', file_name)

@pytest.fixture
def txt_file_wrong_path(request):
    current_directory = os.getcwd()
    file_name = "attendance_weekday_500.txt"
    return  os.path.join(current_directory, file_name)


def test_get_attendance_data_with_right_path(txt_file_right_path):
    attendace_system = AttendanceSystem()
    attendance_data = attendace_system.get_attendance_data(txt_file_right_path)
    assert attendance_data != []

def test_get_attendance_data_with_wrong_path(txt_file_wrong_path, capsys):
    attendace_system = AttendanceSystem()
    attendance_data = attendace_system.get_attendance_data(txt_file_wrong_path)
    captured = capsys.readouterr()
    assert "파일을 찾을 수 없습니다" in captured.out

def test_get_attendance_data_with_none(capsys):
    attendace_system = AttendanceSystem()
    attendance_data = attendace_system.get_attendance_data()
    captured = capsys.readouterr()
    assert "파일을 찾을 수 없습니다" in captured.out

def test_calc_attendance_point_with_right_path(txt_file_right_path,capsys):
    attendace_system = AttendanceSystem()
    attendance_data= [['Umar', 'monday'], ['Daisy', 'tuesday'],
                      ['Alice', 'wednesday'], ['Xena', 'thursday'],
                      ['Ian', 'friday'], ['Hannah', 'saturday'],
                      ['Hannah', 'sunday']]


    for attendee_info in attendance_data:
        if len(attendee_info) == 2:
            attendace_system.calc_attendance_point(attendee_info[0], attendee_info[1])

    for attendee in range(1, attendace_system.get_uniform_num_count() + 1):
        attendace_system.get_bonus_points(attendee)
        attendace_system.calc_grade(attendee)
        attendace_system.print_player_data(attendee)

    captured = capsys.readouterr()

    assert "NAME : Umar, POINT : 1, GRADE : NORMAL" in captured.out
    assert "NAME : Daisy, POINT : 1, GRADE : NORMAL" in captured.out
    assert "NAME : Alice, POINT : 3, GRADE : NORMAL" in captured.out
    assert "NAME : Xena, POINT : 1, GRADE : NORMAL" in captured.out
    assert "NAME : Ian, POINT : 1, GRADE : NORMAL" in captured.out
    assert "NAME : Hannah, POINT : 4, GRADE : NORMAL" in captured.out
    assert "NAME : Hannah, POINT : 4, GRADE : NORMAL" in captured.out

    attendace_system.print_remove_player_list()

def test_calc_grade():
    attendace_system = AttendanceSystem()

    attendace_system.set_points([0, 50, 30, 20])
    attendace_system.calc_grade(1)
    attendace_system.calc_grade(2)
    attendace_system.calc_grade(3)

    result = attendace_system.make_grade.get_grade()
    assert result[1] == 1
    assert result[2] == 2
    assert result[3] == 0

def test_print_player_data(capsys):
    attendace_system = AttendanceSystem()
    #1 : Gold, #2 : Silver #ohter num: noraml
    attendace_system.make_grade.set_grade([0,1,2])
    attendace_system.print_player_data(0)
    attendace_system.print_player_data(1)
    attendace_system.print_player_data(2)
    captured = capsys.readouterr()
    assert "NAME : , POINT : 0, GRADE : NORMAL" in captured.out
    assert "NAME : , POINT : 0, GRADE : NORMAL" in captured.out
    assert "NAME : , POINT : 0, GRADE : SILVER" in captured.out


def test_get_bonus_points(capsys):
    attendace_system = AttendanceSystem()
    #1 : Gold, #2 : Silver #ohter num: noraml
    test_attendance_by_day = [[0] * 100 for _ in range(100)]
    test_attendance_by_day[1][2] = 10
    test_attendance_by_day[2][5] = 5
    test_attendance_by_day[2][6] = 5
    test_attendance_by_day[3][6] = 5

    attendace_system.set_attendance_by_day(test_attendance_by_day)
    attendace_system.get_bonus_points(1)
    attendace_system.get_bonus_points(2)
    attendace_system.get_bonus_points(3)
    test_points = attendace_system.get_points()

    assert test_points[1] == 10
    assert test_points[2] == 10
    assert test_points[3] == 0


