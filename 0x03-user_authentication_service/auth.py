#!/usr/bin/env python3
"""Auth Module
"""
import uuid
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User


def _generate_uuid() -> str:
    """genrate uuid
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Hash password
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Params:
            email: str
            password: str
        Returns:
            User object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = self._db.add_user(
                email=email,
                hashed_password=_hash_password(password)
            )
            return user

        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """email string argument and returns the session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Find user by session ID
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: str) -> None:
        """Destroy session
        """
        return self._db.update_user(user_id=user_id, session_id=None)
