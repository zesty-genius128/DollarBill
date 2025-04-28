from datetime import datetime

def parse_date(date_input):
    # Accept ISO strings or datetime.date
    if isinstance(date_input, str):
        return datetime.fromisoformat(date_input)
    return datetime.combine(date_input, datetime.min.time())