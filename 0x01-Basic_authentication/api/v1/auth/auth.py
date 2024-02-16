#!/usr/bin/env python3
"""
Auth class
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """a class to manage the API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth method"""

        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path in excluded_paths:
            return False
        else:
            for in_path in excluded_paths:
                if path.startswith(in_path):
                    return False
                elif in_path.startswith(path):
                    return False
                else:
                    if in_path[-1] == "*":
                        if path.startswith(in_path[:-1]):
                            return False
        return True

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
