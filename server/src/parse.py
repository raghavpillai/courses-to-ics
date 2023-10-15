from bs4 import BeautifulSoup
from src.class_obj import Class, PartialClass

class Parser:

    @classmethod
    def parse_class_row(cls, class_row: BeautifulSoup) -> PartialClass:
        course_details_row: BeautifulSoup = class_row.find('a', class_='ps-link')
        course_details_full: str
        if course_details_row:
            course_details_full = course_details_row.text.strip()
        else:
            course_details_full = "N/A"
        section_num: str = course_details_full.split(" ")[0]
        course_num: str = course_details_full.split("- ")[1]
        
        # Dates
        date_range_row: BeautifulSoup = class_row.find('span', id=lambda x: x and x.startswith('DERIVED_SSR_FL_SSR_ST_END_DT'))
        date_range: list[str]
        if date_range_row:
            date_range = date_range_row.text.strip().split(" - ")
        else:
            date_range = ["N/A"]

        # Days
        days_row: BeautifulSoup = class_row.find('span', id=lambda x: x and x.startswith('DERIVED_SSR_FL_SSR_DAYS1'))
        days: list[str]
        if days_row:
            days_text: str = days_row.text.replace("Days:", "").strip()
            days = ["TBA"] if "schedule: to" in days_text.lower() else days_text.split(" ")
        else:
            days = ["N/A"]

        # Times
        times_row: BeautifulSoup = class_row.find('span', id=lambda x: x and x.startswith('DERIVED_SSR_FL_SSR_DAYSTIMES'))
        times: str = times_row.text.replace("Times:", "").strip() if times_row else "N/A"
        
        # Room
        room_row: BeautifulSoup = class_row.find('span', id=lambda x: x and x.startswith('DERIVED_SSR_FL_SSR_DRV_ROOM1'))
        room: str = room_row.text.strip() if room_row else "N/A"

        return PartialClass(
            section_num=section_num,
            course_num=course_num,
            date_range=date_range,
            times=times,
            days=days,
            room=room
        )


    @classmethod
    def parse_class_group(cls, class_group: BeautifulSoup) -> list[Class]:
        classes: list[Class] = []
        title: BeautifulSoup = class_group.find('a', id=lambda x: x and x.startswith('DERIVED_SSR_FL_SSR_SCRTAB_DTLS'))
        things: list[str] = title.text.split("   ")
        class_num: str = things[0]
        class_title: str = things[1]

        class_status_row: BeautifulSoup = class_group.find('span', class_='ps_box-value', id=lambda x: x and x.startswith('DERIVED_SSR_FL_SSR_DRV_STAT'))
        class_status: str = class_status_row.text.strip()

        class_detail_rows: list[BeautifulSoup] = class_group.find_all('tr', class_='ps_grid-row psc_rowact')
        for class_row in class_detail_rows:
            class_details: PartialClass = cls.parse_class_row(class_row)
            full_class: Class = Class(
                class_num=class_num,
                section_num=class_details.section_num,
                course_num=class_details.course_num,
                class_title=class_title,
                date_range=class_details.date_range,
                times=class_details.times,
                days=class_details.days,
                room=class_details.room,
                class_status=class_status
            )
            classes.append(full_class)
            print(f"Class num: {class_num}, Section: {class_details.section_num}, Course: {class_details.course_num}, Status: {class_status}, Dates: {class_details.date_range}, Times: {class_details.times}, Days: {class_details.days}, Room: {class_details.room}")
        return classes
        

    @classmethod
    def get_classes(cls, html: str) -> list[Class]:
        """
        Gets classes from requested HTML and parses it
        :param str: HTML to parse
        :return list[Class]: List of classes
        """
        souped_up: BeautifulSoup = BeautifulSoup(html, 'lxml')
        classes: list[Class] = []

        class_groups: list[BeautifulSoup] = souped_up.find_all('div', class_='ps_box-group psc_collapsible psc_margin-none psc_padding-none psc_margin-topnone')
        for class_group in class_groups:
            for new_class in cls.parse_class_group(class_group):
                classes.append(new_class)
        
        return classes
        