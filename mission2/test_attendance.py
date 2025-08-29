import os

import pytest

from attendance import AttendanceSystem
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