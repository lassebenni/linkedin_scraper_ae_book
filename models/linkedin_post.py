from typing import Optional
from pydantic import BaseModel
import re
import unicodedata


class LinkedinPost(BaseModel):
    author: Optional[str] = None
    bio: Optional[str] = None
    author_url: Optional[str] = None
    text: Optional[str] = None
    post_url: Optional[str] = None

    def __init__(self, **data):
        # Function to strip weird characters
        def clean_text(value):
            if isinstance(value, str):
                # Normalize Unicode characters
                value = unicodedata.normalize("NFKD", value)
                # Replace double quotes
                value = value.replace('"', "")
                # Remove non-ASCII characters
                value = re.sub(r"[^\x00-\x7F]+", "", value)
            return value

        # Apply the cleaning function to author, bio, and text
        for field in ["author", "bio", "text"]:
            if field in data:
                data[field] = clean_text(data[field])

        super().__init__(**data)
