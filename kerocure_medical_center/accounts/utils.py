import random
import string
from .models import Staff


def generate_username(validated_data):
    """
    Generate a unique username for the staff member.
    """
    first_name = validated_data.get("first_name", "")
    last_name = validated_data.get("last_name", "")
    base_username = f"{first_name.lower()}_{last_name.lower()}"
    return base_username


def generate_password(validated_data):
    """
    Generates a secure password containing a mix of uppercase, lowercase, digits, and special characters.
    """
    
    base_word = validated_data.get("first_name", "").lower()
    special_char = random.choice(string.punctuation)
    digits = "".join(random.choices(string.digits, k=2))
    password = f"{base_word}{digits}{special_char}"

    return password
