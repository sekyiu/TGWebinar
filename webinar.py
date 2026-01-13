class Webinar:
    def __init__(self, date, time, topic):
        self.date = date
        self.time = time
        self.topic = topic

    @property
    def title(self):
        return f"Brazil Group | Antonio | Tutors Brazil | {self.date} - {self.topic}"

    @property
    def datetime_text(self):
        return f"📅 Webinar - {self.date} às {self.time}"
    

WEBINARS = [
    Webinar("23/01/2026", "14h", "Scratch"),
    Webinar("27/01/2026", "10h", "Scratch"),
    Webinar("30/01/2026", "16h", "Scratch"),
    Webinar("03/02/2026", "14h", "Scratch"),
    Webinar("06/02/2026", "10h", "Scratch"),
]
