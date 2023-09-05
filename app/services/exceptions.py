class UserNotFound(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class LoginError(Exception):
    pass


class UserNotInAgeGroup(Exception):
    pass


class UserAlreadyInClass(Exception):
    pass


class UserNotInClass(Exception):
    pass


class UserAlreadyMaxEnrolled(Exception):
    pass


class SportClassCapacityReached(Exception):
    pass


class SportClassNotFound(Exception):
    pass


class EmailVerificationFailed(Exception):
    pass
