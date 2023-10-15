from dataclasses import dataclass

@dataclass
class PartialClass:
    section_num: str
    course_num: str
    date_range: list[str]
    times: str
    days: list[str]
    room: str

@dataclass
class Class:
    class_num: str
    section_num: str
    course_num: str
    class_title: str
    date_range: list[str]
    times: str
    days: list[str]
    room: str
    class_status: str