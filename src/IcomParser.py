"""RExCL icom statement parser

THe genral format of the icom statement is 

icom <name> ( <registrar_name>)

<name>: Can be any token with alnum , '-' and '_'
<registrar_name>: Name of the registrar. The same should have been
previously defined. 
 
"""

from RexclException import IcomNameExists, RegistrarNotDefined
from RexclException import ExtraCharsInLine
from Parser import Parser

class IcomParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        name = ""
        reg = ""
        # Check for "icom" hive in Parser._ast
        try:
            Parser._ast["icom"]
        except:
            Parser._ast["icom"] = []

        self.match_token("icom")
        name = self.get_token()
        self.match_token("(")
        reg = self.get_token()
        self.match_token(")")
        self.check_for_extra_chars()
        
        if name in [ val["name"] for val in Parser._ast["icom"] ]:
            raise IcomNameExists("Icom name " +
                                 name +
                                 " already exists." +
                                 self.error_string())
        
        if reg not in [ val["name"] for val in Parser._ast["registrar"] ]:
            raise RegistrarNotDefined("The registrar " +
                                      reg +
                                      " is not defined. " +
                                      self.error_string())
        
        Parser._ast["icom"].append({"name": name, "registrar": reg})

    def icom_exists(name):
        return name in [ val["name"] for val in Parser._ast["icom"] ]

    def get_reg_for_icom(icom_name: str) -> str:
        if (IcomParser.icom_exists(icom_name)):
            return [ val["registrar"] for val in Parser._ast["icom"] if (val["name"] == icom_name) ][0]
