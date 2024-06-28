from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field


class TextContent(BaseModel):
    text: Optional[str] = Field(None, alias="text")

    class Config:
        extra = "ignore"


class SummaryContent(BaseModel):
    text_direction: Optional[str] = Field(None, alias="textDirection")
    text: Optional[str] = Field(None, alias="text")

    class Config:
        extra = "ignore"


class EntityEmbeddedObject(BaseModel):
    title: Optional[TextContent] = Field(None, alias="title")

    class Config:
        extra = "ignore"


class IncludedElement(BaseModel):
    title: Optional[TextContent] = Field(None, alias="title")
    primary_subtitle: Optional[TextContent] = Field(None, alias="primarySubtitle")
    summary: Optional[SummaryContent] = Field(None, alias="summary")
    actor_navigation_url: Optional[HttpUrl] = Field(None, alias="actorNavigationUrl")
    entity_embedded_object: Optional[EntityEmbeddedObject] = Field(
        None, alias="entityEmbeddedObject"
    )
    navigation_url: Optional[HttpUrl] = Field(None, alias="navigationUrl")
    template: Optional[str] = None  # Hypothetical attribute for demonstration

    class Config:
        extra = "ignore"


class LinkedInResponse(BaseModel):
    included: List[IncludedElement]

    def __init__(__pydantic_self__, **data):
        super().__init__(**data)
        # Filter out LinkedInPost instances without a template value
        __pydantic_self__.included = [
            post for post in __pydantic_self__.included if post.template is not None
        ]

    class Config:
        extra = "ignore"
