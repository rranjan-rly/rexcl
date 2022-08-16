
import RexclException
from Parser import Parser
from PhoneParser import PhoneParser

class ByteParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        self.match_token("byte")
        self.match_token("(")
        byte_num = self.get_token()
        self.match_token(",")
        phone = self.get_token()
        self.match_token(")")
        self.check_for_extra_chars()
        
        for v in Parser._ast["phone"]:
            if v["name"] == phone:
                v["byte_no"] = byte_num
                return
            # end if
        # end for
        # I am here. This means that the phone does not exist
        raise PhoneNotDefined("Phone " + phone +
                              " not defined. " +
                              self.error_string())
