from datetime import datetime


def _is_valid_date(date_str: str) -> bool:
    """Helper method to validate the date format (YYYY-MM-DD).
    
    Parameters
    ----------
    date_str : str
        The date

    Returns
    -------
    bool 
        True if the date is valid."""
    if not isinstance(date_str, str):
        return False
    try:
        datetime.strptime(
            date_str, "%Y-%m-%d"
        )  # check if str can be convert to valid datetime
        return True
    except ValueError:
        return False
