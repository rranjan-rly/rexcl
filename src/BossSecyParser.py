"""
BossSecyParser.py

boss-secy <boss_phone> ( <secy_phone> [, <boss_secy_type> ] )

  * boss-secy: keyword
  * <boss_phone>: The name of the phone of boss
  * <secy_phone>: The name of the secy phone.
  * <boss_secy_type>: The type can be default | only-secy.
  
The <boss_phone> and <secy_phone> are to be in the same intercom.
"""

from Parser import Parser
from RexclException import ParsingError

class BossSecyParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        self.boss_secy_type= "default"
        self.match_token("boss-secy")
        self.boss = self.get_token()
        
        #Check the icom for the boss.
        try:
            icom = [x["icom"] for x in Parser._ast["phone"] if x["name"] == self.boss ][0]
        except:
            raise ParsingError("The Phone " + self.boss + " is not defined. " + self.error_string())
        
        icom_phones = [ x for x in Parser._ast["phone"] if x["icom"] == icom ]
        
        self.match_token(Parser._LP)
        self.secy = self.get_token()
        # check if type is given
        try:
            phone_secy = [x for x in icom_phones if x["name"] == self.secy][0]
        except:
            raise ParsingError("The secy phone " + self.secy +
                              " does not exist in icom " + icom +
                              ". " + self.error_string())
        
        phone_boss = [x for x in icom_phones if x["name"] == self.boss][0]
        
        if self.look_ahead() == Parser._COMMA:
            #get the <boss_secy_type>
            self.match_token(Parser._COMMA)
            self.boss_secy_type = self.get_token()
            if self.boss_secy_type not in ['default', 'only-secy', 'only_secy'] :
                raise ParsingError('Unknow  type of boss secy arranegment. Can be default|only-secy. Found ' +
                                 self.boss_secy_type +
                                 '. ' + self.error_string())
        self.match_token(Parser._RP)
        self.check_for_extra_chars()
            
         #delete boss_phone from the AST
        Parser._ast["phone"].remove(phone_boss)
        #update phone_boss
        phone_boss["secy_no"] = phone_secy["rly_no"]
        phone_boss["secy_type"] = self.boss_secy_type
        Parser._ast["phone"].append(phone_boss)
