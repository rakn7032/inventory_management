import re

class CommonValidators:
    """
    A utility class for common validation methods such as email and password validation.
    """
    def email_validator(self, email):
        """
        Validates the format of an email address using a regular expression pattern.
        """
        try:
            pattern = r'^[\w\.-]+(\+[\w\.-]+)?@[\w\.-]+\.\w+$'
            if re.match(pattern, email):
                return True
            else:
                return False
        except Exception as e:
            print(f"Error in email_validator: {str(e)}")
            return False

    def password_validator(self, password):
        """
        Validates the strength of a password based on length, uppercase, special characters, and digits.
        """
        try:
            if len(password) < 8:
                return False
            if not any(char.isupper() for char in password):
                return False
            if not re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?`~]', password):
                return False
            if not any(char.isdigit() for char in password):
                return False
            return True
        except Exception as e:
            print(f"Error in password_validator: {str(e)}")
            return False