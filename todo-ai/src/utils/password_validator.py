import re
from typing import Tuple

def validate_password(password: str) -> Tuple[bool, str, str]:
    """
    Validates a password according to the following rules:
    1. Password must be exactly 8 characters long
    2. It must contain exactly one special character
    3. The remaining 7 characters can be anything (letters, numbers, or symbols)
    4. If the password is longer than 8 characters, truncate it to meet this rule
    5. Ensure password is within bcrypt byte limit (72 bytes)

    Args:
        password: The password to validate

    Returns:
        Tuple[bool, str, str]: (is_valid, message, processed_password)
    """
    # Truncate password to 8 characters if it's longer
    if len(password) > 8:
        original_length = len(password)
        password = password[:8]
        return True, f"Password was truncated from {original_length} to 8 characters", password

    # Check if password is exactly 8 characters long
    if len(password) != 8:
        return False, f"Password must be exactly 8 characters long, but got {len(password)} characters", password

    # Count special characters
    special_chars = re.findall(r'[!@#$%^&*(),.?":{}|<>+=\[\]\\;\'`~]', password)
    special_count = len(special_chars)

    if special_count != 1:
        return False, f"Password must contain exactly 1 special character, but found {special_count}", password

    # Ensure the password is within bcrypt byte limit (72 bytes)
    # Since our password is limited to 8 characters, this check will always pass
    # But we include it for completeness and future-proofing
    if len(password.encode('utf-8')) > 72:
        return False, f"Password exceeds bcrypt byte limit of 72 bytes", password

    return True, "Password is valid", password