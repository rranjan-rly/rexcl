"""RExCL registrar Statement Parser

This module parses the registrar statement of RExCL. The format for
registrar statement is as under

registrar <name> ( <primary_ip_addr> [, <secondary_ip_addr>] )

<name> : Can be any token
<primary_ip_address>: Should be an IPv4 address.
<secondary_ip_address>: Should be an IPv4 address. This is optional. 

Note: The primary and the secondary ips must be different. 

Exceptions Raised
-----------------
It raises the following exceptions:

a. RegistrarNameExists: This is raised when the registrar name is
duplicated. 
b. RegistrarIPExists: This is raised if the same IP is assigned to
another registrar either as secondary or primary registrar. 

"""

from RexclException import ParsingError
from Parser import Parser

class RegistrarParser(Parser):
    def __init__(self, line_no, line):
        name = ""
        ipv4 = ""
        bipv4 = ""
        Parser.__init__(self, line_no, line)
        # Check if the "registrar" hive is available in the ast class var
        try:
            Parser._ast["registrar"]
        except:
            Parser._ast["registrar"] = []
            
        self.match_token("registrar")
        name = self.get_token()
        self.match_token("(")
        ipv4 = self.get_token_ipv4()
        if (self.look_ahead() == ","):
            # Looks like a secondary registrar ip is also defined.
            self.match_token(",")
            bipv4 = self.get_token_ipv4()
        self.match_token(")")
        self.check_for_extra_chars()
        
        if (ipv4 == bipv4):
            raise ParsingError("Registrar " + name + " has same secondary and primary IPs.\n" + self.error_string())

        # All ok. Register the registrar

        # Check for name clash
        if name in [ val["name"] for val in Parser._ast["registrar"] ]:
            raise ParsingError("Registrar " + name + " already exists.")
        # Check for IP clash
        # prepare a set of all IPs. 
        s1 = {val["ip"] for val in Parser._ast["registrar"] if val["ip"] != ""}
        s2 = {val["bip"] for val in Parser._ast["registrar"] if val["bip"] != ""}
        s1.update(s2)
        if ((ipv4 in s1) or (bipv4 in s1)):
            raise ParsingError("Registrar IP " +
                                    bipv4 +
                                    " already exists.\n" +
                                    self.error_string())
        # No IP clash found
        Parser._ast["registrar"].append({"name": name, "ip": ipv4, "bip": bipv4})
        
