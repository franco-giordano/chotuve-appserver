import logging

class ChotuveError(Exception):

    def __init__(self):
        Exception.__init__(self)


    def logger(self):
        return logging.getLogger(self.__class__.__name__)

    def to_dict(self):
        self.logger().error(self.message)
        return {"message":self.message}

# ---------------------------------------------------


class BadRequestError(ChotuveError):
    status_code = 400

    def __init__(self):
        super().__init__()

class NotFoundError(ChotuveError):
    status_code = 404

    def __init__(self):
        super().__init__()

class BadGatewayError(ChotuveError):
    status_code = 502

    def __init__(self):
        super().__init__()

class NotImplementedError(ChotuveError):
    status_code = 501

    def __init__(self):
        super().__init__()



# ---------------------------------------------------


class ReactionBadRequestError(BadRequestError):
    
    def __init__(self, message):
        self.message = message
        super().__init__()


class UserNotFoundError(NotFoundError):

    def __init__(self, message):
        self.message = message
        super().__init__()

class VideoNotFoundError(NotFoundError):

    def __init__(self, message):
        self.message = message
        super().__init__()

class FailedToContactAuthSvError(BadGatewayError):
    def __init__(self, message):
        self.message = message
        super().__init__()


class FailedToContactMediaSvError(BadGatewayError):
    def __init__(self, message):
        self.message = message
        super().__init__()