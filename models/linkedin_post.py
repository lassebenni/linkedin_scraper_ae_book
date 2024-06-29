from typing import Optional
from pydantic import BaseModel
import re
import unicodedata
from datetime import datetime
import uuid

import hashlib
import re
import unicodedata
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
import uuid


class LinkedinPost(BaseModel):
    id: Optional[str] = None
    created: Optional[datetime] = datetime.now()
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
        self.generate_id()

    def generate_id(self):
        # Concatenate all relevant fields except 'created' and 'id'
        fields_concat = "".join(
            [
                str(getattr(self, field))
                for field in self.__fields__.keys()
                if field not in ["created", "id"] and getattr(self, field) is not None
            ]
        )
        # Generate hash
        self.id = hashlib.sha256(fields_concat.encode()).hexdigest()