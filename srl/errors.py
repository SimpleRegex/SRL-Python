# -*- coding: utf-8 -*-

class SRLException(Exception):
    pass

class BuilderException(SRLException):
    pass

class ImplementationException(SRLException):
    pass

class InterpreterException(SRLException):
    pass

class SyntaxException(SRLException):
    pass

class PregException(SRLException):
    pass

class PregInternalError(PregException):
    pass

class PregBacktrackLimitError(PregException):
    pass

class PregBadUTF8Error(PregException):
    pass

class PregBadUTF8OffsetError(PregException):
    pass

class PregJITStackLimitError(PregException):
    pass

class UnknownPregError(PregException):
    pass
