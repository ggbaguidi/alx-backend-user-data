#!/usr/bin/env python3
"""Module documentation"""
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str):
    """
    Arguments:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating all
        fields in the log line (message)
    The function should use a regex to replace occurrences of certain field
    values.
    """
    for field in fields:
        pattern = re.compile(
            r'(?<='
            + re.escape(separator)
            + field
            + '='
            + ')[^'
            + re.escape(separator)
            + ']+'
        )
        message = re.sub(pattern, redaction, message)

    return message
