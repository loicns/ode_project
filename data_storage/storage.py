from django.core.files.storage import get_storage_class
import uuid  # Import for generating unique IDs

class StorageEngine:
    def __init__(self):
        self.storage = get_storage_class()  # Retrieve configured storage backend

    def upload_data(self, data, filename):
        """Uploads data to the configured storage backend (assuming PostgreSQL)."""
        unique_filename = generate_unique_filename(filename)
        self.storage.save(unique_filename, data)
        return unique_filename

    def download_data(self, filename):
        """Downloads data from the configured storage backend (assuming PostgreSQL)."""
        data = self.storage.open(filename).read()
        return data

    def delete_data(self, filename):
        """Deletes data from the configured storage backend (assuming PostgreSQL)."""
        self.storage.delete(filename)


def get_downloaded_data(filename):
    """Downloads and returns data as appropriate for the content type.

    - If the content type indicates text data (e.g., UTF-8), decodes the data.
    - Otherwise, returns the raw binary data.

    Args:
        filename: The filename of the data to download

    Returns:
        The downloaded data:
            - Decoded string (if text data)
            - Raw bytes (if binary data)
    """

    storage_engine = StorageEngine()  # Create an instance
    data = storage_engine.download_data(filename)

    # Retrieve the content type associated with the file
    content_type = storage_engine.storage.get_available_attributes(filename).get('content_type')

    if content_type and content_type.startswith('text/'):
        # Assuming text data with UTF-8 encoding
        return data.decode('utf-8')
    else:
        # Returning raw bytes for binary data
        return data

def generate_unique_filename(filename):
    """Generates a unique filename based on the original filename."""
    extension = filename.split('.')[-1]  # Extract file extension
    unique_id = uuid.uuid4().hex  # Generate a unique ID
    unique_filename = f"{unique_id}.{extension}"
    return unique_filename
