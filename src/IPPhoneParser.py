"""
#IPPhoneParser.py

ipphone (<phone_name>, <make-model>, <mac_address>)

"""

from RexclException import ParsingError
from Parser import Parser
from string import Template
from YealinkIPPhone import YealinkIPPhone

phone_model_supported = [
    "YEALINK-T27G",
    "YEALINK-T23G"
    ];
class IPPhoneParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        self.match_token("ipphone")
        self.match_token(Parser._LP)
        self.ph_name = self.get_token()
        self.match_token(Parser._COMMA)
        self.ph_model = self.get_token().upper()
        self.match_token(Parser._COMMA)
        self.ph_mac = self.get_token_mac().lower()
        self.match_token(Parser._RP)
        self.check_for_extra_chars()
        
        if self.ph_model not in phone_model_supported:
            raise ParsingError("Model " + self.ph_model + " is not yet supported. " + self.error_string())
        
        for p in Parser._ast["phone"]:
            if p["name"] == self.ph_name:
                p["model"] = self.ph_model
                p["mac"] = self.ph_mac
                return
            # end if
        # end for
        # I am here. This means that the phone does not exist
        raise ParsingError("Phone " + self.ph_name +
                              " not defined. " +
                              self.error_string())
                
class IPPhoneFactory:
    def __init__(self, model, ph):
        self.conf = ""
        if model not in phone_model_supported:
            raise ParsingError("Model " + self.ph_model + " is not yet supported. This is BUG and should be reported.")
        if model == "YEALINK-T27G" or model == "YEALINK-T23G":
            self.conf = YealinkIPPhone(model, ph).get_conf()
            
    def get_conf(self):
        return self.conf

            