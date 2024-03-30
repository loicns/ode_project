from datetime import datetime

def split_text(text, delimiter=','):
    # Function to split text based on a delimiter
    return text.split(delimiter)

def combine_fields(field1, field2):
    # Function to combine two fields
    return f"{field1} {field2}"

def capitalize_first_letter(text):
    # Capitalizes the first letter of each word in a string
    return text.title()

def convert_to_lowercase(text):
    # Converts text to lowercase
    return text.lower()

def format_date(date_string, format="%Y-%m-%d"):
    # Formats a date string in the specified format
    date = datetime.strptime(date_string, format)
    return date.strftime(format)
