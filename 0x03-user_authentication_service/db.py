#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Params:
            email: str
            hashed_password: str
        Returns:
            User: an object User
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Params:
            arbitrary keyword arguments
        Returns:
            returns the first row found in the users
        """
        all_users = self._session.query(User)

        for key, value in kwargs.items():
            if key not in User.__dict__:
                raise InvalidRequestError
            for user in all_users:
                if getattr(user, key) == value:
                    return user

        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Params:
            user_id integer
            arbitrary keyword arguments
        Returns:
            None
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound as e:
            raise ValueError from e

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)
        self.__session.commit()
