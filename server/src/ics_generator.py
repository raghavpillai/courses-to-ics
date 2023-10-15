from datetime import datetime, timedelta
from src.class_obj import Class
from ics import Event, Calendar
from pytz import timezone

class IcsGenerator:

    @classmethod
    def day_to_num(cls, day_str: str) -> int:
        """
        Converts a string day of the week to an integer
        :param str: Day of the week as a string
        :return int: Day of the week as an integer
        """
        day_dict: dict[str, int] = {
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2,
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6
        }
        return day_dict.get(day_str, -1)

    @classmethod
    def get_ics_str(cls, classes_data: list[Class]) -> tuple[str, str]:
        cal: Calendar = Calendar()
        cst = timezone('US/Central')
        errors: str = ""

        for class_obj in classes_data:
            start_date: datetime = datetime.strptime(class_obj.date_range[0], "%m/%d/%Y")
            end_date: datetime = datetime.strptime(class_obj.date_range[1], "%m/%d/%Y")

            if "N/A" in class_obj.times:
                errors += f"[INFO] No times available for {class_obj.class_num}.{class_obj.section_num}\n"
                continue
            
            if class_obj.class_status == "Dropped":
                errors += f"[INFO] Class was dropped, not showing {class_obj.class_num}.{class_obj.section_num}\n"
                continue

            if "To be Announced" in class_obj.times:
                errors += f"[INFO] Class was to be announced, not showing {class_obj.class_num}.{class_obj.section_num}\n"
                continue

            start_time = datetime.strptime(class_obj.times.split(" to ")[0], "%I:%M%p").time()
            end_time = datetime.strptime(class_obj.times.split(" to ")[1], "%I:%M%p").time()
            current_date: datetime = start_date

            while current_date <= end_date:
                if current_date.weekday() in [cls.day_to_num(day) for day in class_obj.days]:
                    event = Event()
                    event.name = f"{class_obj.class_num}.{class_obj.section_num}"
                    event.begin = cst.localize(datetime.combine(current_date, start_time))
                    event.end = cst.localize(datetime.combine(current_date, end_time))
                    event.description = f"[{class_obj.course_num}] {class_obj.class_num}.{class_obj.section_num} - {class_obj.class_title}"
                    event.location = class_obj.room
                    cal.events.add(event)
                current_date += timedelta(days=1)
        
        return errors, str(cal)
