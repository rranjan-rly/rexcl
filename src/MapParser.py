"""
map ( <short_code> , <phone_name> )
  
    * short_code -> The short code that is to be mapped.
    * phone_name -> The name of the phone that will be called
                    when the short_code is dialled. 

"""

from Parser import Parser
from RexclException import ParsingError

class MapParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        self.match_token("map")
        self.match_token(Parser._LP)
        self.short_code = self.get_token()
        self.match_token(Parser._COMMA)
        self.phone = self.get_token()
        self.match_token(Parser._RP)
        self.check_for_extra_chars()
        
        # Check if the phone exists.
        if len ([ x for x in Parser._ast['phone'] if x['name'] == self.phone ]) == 0:
            raise ParsingError("Phone " + self.phone + " does not exists. " + self.error_string())
        
        Parser._ast["map"].append({
            "short_code": self.short_code,
            "phone": self.phone
        })
        
        
        
    
