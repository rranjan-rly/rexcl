"""RExCL phone statement Parser

The general format for the same is 

phone <name> (<icom>, <icom_no>, <disp_name>, <secret>, <rly_no>, <pstn_no>)

<name>: Can be any token with alnum, '-', '_'
<icom_no>: intercom number
<disp_name>: Name for displaying on the phone.
<secret>: The password for the SIP account.
<rly_no>: The 5-digit railway number. Used as the username for SIP
account.
<pstn_no>: The PSTN number assigned with the phone. Can be "-1" if not
required.   

"""

from IcomParser import IcomParser
from Parser import Parser
from RexclException import ParsingError

class PhoneParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        #Check for phone hive in Parser._ast
        try:
            Parser._ast["phone"]
        except:
            Parser._ast["phone"] = []

        self.match_token("phone")
        name = self.get_token()
        # Chek for duplicate phone names
        if name in [ val["name"] for val in Parser._ast["phone"] ]:
            raise ParsingError("Phone " +
                                      name +
                                      " already defined at " +
                                      str(self.get_phone_def_line_no(name)) +
                                      ". " + self.error_string())
        
        self.match_token(Parser._LP)
        icom = self.get_token()
        # Check if the icom exists
        if (not IcomParser.icom_exists(icom)):
            raise ParsingError("Icom " + icom +
                                 " is not defined. " +
                                 self.error_string())
        

        self.match_token(Parser._COMMA)
        icom_no = self.get_token()
        # Check if the icom_number is already defined. 
        if (icom, icom_no) in [ (val["icom"], val["icom_no"]) for val in Parser._ast["phone"] ]:
            raise ParsingError("Icom No. " + icom_no +
                                           " for Intercom " + icom +
                                           " is already defined" +
                                           ". " + self.error_string())

        self.match_token(Parser._COMMA)
        disp_name = self.get_token()

        self.match_token(Parser._COMMA)
        secret = self.get_token()

        self.match_token(Parser._COMMA)
        rly_no = self.get_token()

        # Check if Rly No. is unique
        if rly_no in [ val["rly_no"] for val in Parser._ast["phone"] ]:
            raise ParsingError("Rly Number " + rly_no +
                                      " for Phone " + name +
                                      " is already defined" +
                                      ". " + self.error_string())
        
        self.match_token(Parser._COMMA)
        pstn_no = self.get_token()
        # Check if PSTN No. is unique
        if ((pstn_no != "-1") and
            (pstn_no in [ val["pstn_no"] for val in Parser._ast["phone"] ])):
            raise ParsingError("PSTN Number " + pstn_no +
                                       " for Phone " + name +
                                       " is already defined" +
                                       ". " + self.error_string())

        self.match_token(Parser._RP)
        
        Parser._ast["phone"].append({
            "name": name,
            "icom": icom,
            "reg": IcomParser.get_reg_for_icom(icom),
            "icom_no": icom_no,
            "disp_name": disp_name,
            "secret": secret,
            "rly_no": rly_no,
            "pstn_no": pstn_no,
            "byte_no": "",
            "secy_no": "",
            "secy_type": "default",
            "line_no": line_no,
            "breg": "",
            "model": "",
            "mac": ""
        })            

    def get_phone_def_line_no(self, phone_name: str) -> str:
        # Phone_name should exist.
        lst = [ val["line_no"] for val in Parser._ast["phone"] if val["name"] == phone_name ]
        return lst[0]

    
