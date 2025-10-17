from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
import imghdr

MAX_FILE_SIZE_MB = 5  # máximo 5 MB
ALLOWED_FORMATS = ['jpeg', 'png']

@deconstructible
class ValidateImageFile:
    def __call__(self, value):
        # Verify size
        limit = MAX_FILE_SIZE_MB * 1024 * 1024
        if value.size > limit:
            raise ValidationError(f"File too large. Size should not exceed {MAX_FILE_SIZE_MB} MB.")

        # Verify real image type (header, not extension)
        file_type = imghdr.what(value)
        if file_type not in ALLOWED_FORMATS:
            raise ValidationError("Unsupported file type. Only JPG and PNG are allowed.")

        return value
