from enum import Enum


class Variant(str, Enum):
    FLAT = "flat"
    ELEVATED = "elevated"
    OUTLINED = "outlined"
    TEXT = "text"
    PLAIN = "plain"
