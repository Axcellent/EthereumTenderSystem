from pydantic import BaseModel, field_validator

from models.common import (string,
                           text,
                           UserStatus)

from typing import List

import re

class UserCreateDTO(BaseModel):
    title: string
    description: text
    cities: text
    telephones: text
    emails: text

    @field_validator("telephones", mode="before")
    def validate_telephones(cls, values: List):
        if not isinstance(values, List):
            raise ValueError("Uncorrect input format (expected array)")
        if len(values) > 5:
            raise ValueError("Too many telephones")
                
        for v in values:
            if not re.fullmatch(r"\+7 \([0-9]{3}\) [0-9]{3}-[0-9]{2}-[0-9]{2}", v) and \
                not re.fullmatch(r"8[0-9]{10}", v):
                raise ValueError(f"Uncorrect format on {v}, need +7 (xxx) xxx-xx-xx or 8xxxxxxxxxx")
        return ', '.join(values)

    @field_validator("emails", mode="before")
    def validate_emails(cls, values: List):
        if not isinstance(values, List):
            raise ValueError("Uncorrect input format (expected array)")
        if len(values) > 5:
            raise ValueError("Too many emails")
                
        for v in values:
            if not re.fullmatch(r"[a-zA-Z-0-9]+@[a-zA-Z-]+\.ru", v):
                raise ValueError(f"Uncorrect format on {v}, need your-email@some-domain.only-ru")
        return ', '.join(values)

    @field_validator("cities", mode="before")
    def validate_cities(cls, values: List):
        if not isinstance(values, List):
            raise ValueError("Uncorrect input format (expected array)")
        if len(values) > 128:
            raise ValueError("Too many cities")
                
        for v in values:
            if not re.fullmatch(r"[a-zA-Z-]+", v):
                raise ValueError(f"Uncorrect format on {v}, need Rostov-On-Don like")
        return ', '.join(values)

class UserGetFullDTO(BaseModel):
    title: string
    description: text
    cities: list[string]
    telephones: list[string]
    emails: list[string]

    @field_validator("telephones", mode="before")
    def validate_telephones(cls, values: text):
        if not isinstance(values, str):
            raise ValueError("Uncorrect input format (expected text)")

        values = values.split(', ')    
            
        for v in values:
            if not re.fullmatch(r"\+7 \([0-9]{3}\) [0-9]{3}-[0-9]{2}-[0-9]{2}", v) and \
                not re.fullmatch(r"8[0-9]{10}", v):
                raise ValueError(f"Uncorrect format on {v}, need +7 (xxx) xxx-xx-xx or 8xxxxxxxxxx")
        return values

    @field_validator("emails", mode="before")
    def validate_emails(cls, values: text):
        if not isinstance(values, str):
            raise ValueError("Uncorrect input format (expected text)")
                
        values = values.split(', ')

        for v in values:
            if not re.fullmatch(r"[a-zA-Z-]+@[a-zA-Z-]+\.ru", v):
                raise ValueError(f"Uncorrect format on {v}, need your-email@some-domain.only-ru")
        return values

    @field_validator("cities", mode="before")
    def validate_cities(cls, values: text):
        if not isinstance(values, str):
            raise ValueError("Uncorrect input format (expected text)")

        values = values.split(', ')
                
        for v in values:
            if not re.fullmatch(r"[a-zA-Z-]+", v):
                raise ValueError(f"Uncorrect format on {v}, need Rostov-On-Don like")
        return values
    
    status: UserStatus

class UserGetShortDTO(BaseModel):
    title: string
    status: UserStatus
