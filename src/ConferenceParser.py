"""
Conference Statement Definition
===============================

conference <conf_name> ( <reg>, <rly_no>, <phone_name> [, <conf_type>] )

<conf_name> -> Name of the conference.
<reg> -> This conference is to be installed on this registrar named <reg>.
<rly_no> -> The rly_no that is used to access the conference named <conf_name>.
<phone_name> -> The name of the admin phone for this conference.
<conf_type> -> attended | default

Attended Conference
===================
An attended conference means that the users cannot directly become a
participant in the conference. The operator uses the admin
phone of the conference to call a subscriber and then transfers the
called subscriber in the conference. This has to be done for each and
every conference participant.

Default Conference
==================
The default conference is a conference that has a security PIN. It
has a railway number associated and any subscriber can dial this
number, enter the security PIN when asked and become part of the
conference. No operator is required. The users can change the
security PIN for the conference using the admin phone for the
conference.

Admin Function
==============
*26630* -> Play PIN
*26631* -> Set  PIN

"""

from Parser import Parser
from RexclException import ParsingError

class ConferenceParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        self.match_token("conference")
        self.conf_name = self.get_token()
        # Check conf name duplication
        if len([x for x in Parser._ast["conference"] if x["name"] == self.conf_name]) != 0:
            raise ParsingError("Conference name " + self.conf_name + " already exists. " + self.error_string())
        
        self.match_token(Parser._LP)
        self.reg = self.get_token()
        #check existence of reg
        if len([x for x in Parser._ast["registrar"] if x["name"] == self.reg]) == 0:
            raise ParsingError("Registrar " + self.reg + " does not exist. " + self.error_string())
        
        self.match_token(Parser._COMMA)
        self.conf_no = self.get_token()
        #check conf_no is an integer
        try:
            int(self.conf_no)
        except:
            raise ParsingError("Conference number should be an integer. Found " +
                               self.conf_no + ". " +self.error_string())
        
        self.match_token(Parser._COMMA)
        self.admin_phone = self.get_token()
        #check that the phone exists
        self.admin_phone_no = ''
        try:
            #print (Parser._ast["phone"])
            admin_ph = [x for x in Parser._ast["phone"] if x["name"] == self.admin_phone][0]
            self.admin_phone_no = admin_ph['rly_no']
        except:
            raise ParsingError("Phone " + self.admin_phone + " does not exist. " + self.error_string())
        
        #Check tha the admin phone is the same rgsitrar where the conference is defined.
        #TODO
        # Do we actually need to check it. Conference can be aseparate server.
        ch = self.look_ahead()
        if ch == ",":
            # A conf_type has been defined.
            self.match_token(Parser._COMMA)
            self.conf_type = self.get_token()
            if self.conf_type != "attended" and self.conf_type != "default":
                raise ParsingError("Conference type has to be attended|default. " + self.error_string())
            # end
        else:
            self.conf_type = "default"
        self.match_token(Parser._RP)
        self.check_for_extra_chars()
        
        Parser._ast["conference"].append({
            'name': self.conf_name,
            'reg': self.reg,
            'conf_no': self.conf_no,
            'admin_phone': self.admin_phone,
            'admin_phone_no': self.admin_phone_no,
            'type': self.conf_type})
        