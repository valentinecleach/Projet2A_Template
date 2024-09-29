from datetime import datetime

def _is_valid_date(self, date_str: str) -> bool:
    """
    Helper method to validate the date format (YYYY-MM-DD).

    Parameters:
    -----------
    date_str : str
        The date string to be validated.

    Returns:
    --------
    bool : True if the date is valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False