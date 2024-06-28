from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Extra


class TextContent(BaseModel):
    text: Optional[str] = None

    class Config:
        extra = "ignore"


class SummaryContent(BaseModel):
    text_direction: Optional[str] = None
    text: Optional[str] = None

    class Config:
        extra = "ignore"


class EntityEmbeddedObject(BaseModel):
    title: Optional[TextContent] = None

    class Config:
        extra = "ignore"


class LinkedInPost(BaseModel):
    title: Optional[TextContent] = None
    primary_subtitle: Optional[TextContent] = None
    summary: Optional[SummaryContent] = None
    actor_navigation_url: Optional[HttpUrl] = None
    entity_embedded_object: Optional[EntityEmbeddedObject] = None
    navigation_url: Optional[HttpUrl] = None
    template: Optional[str] = None

    class Config:
        extra = "ignore"


class LinkedInResponse(BaseModel):
    included: List[LinkedInPost] = []

    class Config:
        extra = "ignore"

    def __getattribute__(self, item):
        if item == "included":
            # Filter the included list to only return items with a 'template' attribute
            filtered_included = [
                post
                for post in super().__getattribute__(item)
                if post.template is not None
            ]
            return filtered_included
        else:
            # For any other attribute, return it as usual
            return super().__getattribute__(item)
