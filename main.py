from typing import Dict, Union
from datetime import datetime as dt


class OpeningHoursFormatter:
    """
    Инициализация обьекта OpeningHoursFormatter

    :param data_json: словарь с данными о часах работы
    """
    def __init__(self, data_json) -> None:
        self.data_json = data_json

    def format_opening_hours(self) -> str:
        """
        Форматирования часов работы для каждого дня

        :return: Строка с отфарматировными часами работы
        """
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        formatted_hours = []

        for day in days_of_week:
            if day.lower() in self.data_json:
                hours = self.data_json[day.lower()]
                if not hours:
                    formatted_hours.append(f"{day}: Closed")
                else:
                    formatted_hours.append(f"{day}: {self.format_day_hours(hours)}")

        return "\n".join(formatted_hours)

    def format_day_hours(self, hours: Dict) -> str:
        """
        Форматирование длаты для конкретного дня
        :param hours: Словарь с часами рабоы
        :return: Строка с отфаматировными часами работы
        """
        formatted_day_hours = []
        current_open = None

        for hour in hours:
            if hour["type"] == "open":
                current_open = self.format_time(hour["value"])
            elif hour["type"] == "close" and current_open is not None:
                formatted_day_hours.append(f"{current_open} - {self.format_time(hour['value'])}")
                current_open = None

        if current_open is not None:
            formatted_day_hours.append(f"{current_open} - 1 AM")

        return ", ".join(formatted_day_hours)

    def format_time(self, unix_time: Union[int, float]) -> str:
        """
        Форматирование из UNix формата, в строку
        :param unix_time: Время в Unix формате
        :return: Строка с отфармотировым временем
        """
        time = dt.utcfromtimestamp(unix_time).strftime('%I:%M %p')
        if ':00' in time:
            time = time.replace(':00', '')
        return time.lstrip('0')


json_data = {
            "monday": [],
            "tuesday": [
                {"type": "open", "value": 36000},
                {"type": "close", "value": 64800}
            ],
            "wednesday": [],
            "thursday": [
                {"type": "open", "value": 37800},
                {"type": "close", "value": 64800}
            ],
            "friday": [
                {"type": "open", "value": 36000}
            ],
            "saturday": [
                {"type": "open", "value": 36000}
            ],
            "sunday": [
                {"type": "open", "value": 43200},
                {"type": "close", "value": 75600}
            ]
        }

formatter = OpeningHoursFormatter(json_data)
result = formatter.format_opening_hours()
print(result)
