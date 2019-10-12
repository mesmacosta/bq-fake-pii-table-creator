import uuid


class UUIDHelper:

    @staticmethod
    def generate_uuid(length=4):
        random = str(uuid.uuid4())  # Convert UUID format to a Python string
        random = random.replace('-', '')  # Remove the '-' character
        return random[0:length]  # Return the random string
