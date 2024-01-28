from typing import List
from pydantic import BaseModel, Field


class RecapOutput(BaseModel):
    title: str = Field(
        description="A concise one-line summary that captures the main topic of the document."
    )
    subtitle: str = Field(
        description="Additional information below the title, providing specifying subtopics."
    )
    summary: str = Field(
        description="A brief overview encapsulating the main content of the document."
    )
    keywords: List[str] = Field(
        description="List of frequently used important WORDs or terms in the document.",
    )

    def to_dict(self):
        return {
            "title": self.title,
            "subtitle": self.subtitle,
            "summary": self.summary,
            "keywords": self.keywords,
        }
