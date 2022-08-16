"""Exceptions that RExCL can raise.

This module defines all types of Exceptions that can be raised by
RExCL. 

"""

class RexclException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def get_msg(self):
        rv = "** Error **\n"
        rv += "=" * 70 + "\n"
        rv += self.msg + "\n"
        rv += "=" * 70 + "\n"
        return rv

class TokenNotMatched(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class NotAnIpAddress(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class RegistrarNameExists(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class RegistrarIPExists(RexclException):
        def __init__(self, msg):
            RexclException.__init__(self, msg)

class RegistrarSameIP(RexclException):
        def __init__(self, msg):
            RexclException.__init__(self, msg)
            
class UnknownRexclStatement(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class IcomNameExists(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class RegistrarNotDefined(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class PhoneAlreadyDefined(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class IcomNotDefined(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class IcomNumberAlreadyDefined(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class RlyNumberAlreadyDefined(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class PstnNumberAlreadyDefined(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class ExtraCharsInLine(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class PhoneNotDefined(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)

class ParsingError(RexclException):
    def __init__(self, msg):
        RexclException.__init__(self, msg)