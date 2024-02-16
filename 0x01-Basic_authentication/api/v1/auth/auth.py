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
        return False

    def authorization_header(self, request=None) -> str:
        """authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """current user"""
        return None
