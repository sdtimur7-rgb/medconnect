class MedConnectException(Exception):
    pass


class OneCAPIException(MedConnectException):
    pass


class SMSException(MedConnectException):
    pass


class ChatwootException(MedConnectException):
    pass


class AIManagerException(MedConnectException):
    pass


class BillingException(MedConnectException):
    pass
