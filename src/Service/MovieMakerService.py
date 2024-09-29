from datetime import datetime

class MovieMakerService():

    @staticmethod
    def _is_valid_date(date_str: str) -> bool:
        """Helper method to validate the date format (YYYY-MM-DD)."""
        if not isinstance(date_str, str):
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d") # check if str can be convert to valid datetime
            return True
        except ValueError:
            return False