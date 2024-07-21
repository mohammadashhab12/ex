# pycommon/exceptions.py

class UserAlreadyExistsException(Exception):
    def __init__(self, username: str):
        self.username = username

class UserNotFoundException(Exception):
    def __init__(self, username: str):
        self.username = username

class MaxAdminUsersReachedException(Exception):
    pass
