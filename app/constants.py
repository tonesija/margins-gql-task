from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class AgeGroup(str, Enum):
    CHILDREN = "children"
    YOUTH = "youth"
    YOUNG_ADULT = "young_adult"
    ADULT = "adult"
