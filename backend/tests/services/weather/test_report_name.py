from backend.services.weather.report_name import to_file_name


def test_to_file_name_sanitizes_and_adds_extension():
    assert to_file_name("My Report 2024") == "My_Report_2024.wea"


def test_to_file_name_preserves_existing_extension():
    assert to_file_name("data.wea") == "data.wea"


def test_to_file_name_handles_empty_name():
    assert to_file_name("   ") == "report.wea"
