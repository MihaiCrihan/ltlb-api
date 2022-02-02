class BaseError:
    __abstract__ = True
    errors = None
    message = "Succeess"
    status = 200

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            self.__setattr__(key, value)

    def __call__(self, *args, **kwargs):
        for (key, value) in kwargs.items():
            self.__setattr__(key, value)

        if self.errors is not None:
            return {"message": self.message, "errors": self.errors}, self.status
        else:
            return self.message, self.status


class Success:
    status = 200
    data = None
    message = 'Success'

    def __call__(self, data, **kwargs):
        self.data = data

        for (key, value) in kwargs.items():
            self.__setattr__(key, value)

        if data is None:
            return self.message, self.status
        return self.data, self.status


class UnprocessableEntityError(BaseError):
    message = 'Unprocessable entity'
    status = 422


class NotFoundError(BaseError):
    errors = None
    message = "Not found"
    status = 404


class UnauthorizedError(BaseError):
    errors = None
    message = "Unauthorized"
    status = 401


class ForbiddenError(BaseError):
    errors = None
    message = "Forbidden"
    status = 403


class InternalServerError(BaseError):
    errors = None
    message = "Forbidden"
    status = 403


UnprocessableEntity = UnprocessableEntityError()
NotFound = NotFoundError()
InternalServerError = InternalServerError()
ForbiddenError = ForbiddenError()
UnauthorizedError = UnauthorizedError()