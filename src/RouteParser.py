"""
Route Statement Definition
==========================

route <rname> ( <reg_or_gw>, <pattern>, <route_def> [| <route_def] )
route_def ::= (sip|pri):<reg_or_gw>[:<tranformation_function>]
transformation_function ::= prefix ( <str> )
  | postfix ( <str> )
  | slice ( <offset> [:length] )
  | preslice ( <str>, <offset>[:<length>] )

<rname> -> Name of the route being installed.
<reg_or_gw> -> Name of the registrar or the gateway where this route will be installed.
<pattern> -> The pattern that will be matched with the extension.
    X Match any number from 0-9.
    Z Match any number from 1-9.
    N Match any number from 2-9.
    [2-5] Matches a single digit that is 2 or 3 or 4 or 5.
    23X Matches any three digit number from 230 to 239.
    0X. Matches any number of digits starting with a 0. The dot (.) matches any string of chars.
<str> -> Any string that will be attached with the extension number before dialing.
    prefix(str): This puts the str before the dialed number and then routes the call.
    suffix(str) This puts the str after the dialed number and then routes the call.
    slice(offset[:length]) This function removes length number of digits from the dialed number
            starting from the offset. If the dialed number is 923456 then slice(1) gives 23456,
            slice(1:3) gives 234.
    preslice(str,offset[:length]) This function is a mix of slice and prefix.
    
Example
========

route r1(reg1, 0X., sip:g1)

In the statement above, we define a route r1 that is installed in the server reg1. It says
that whenever the pattern 0X. is seen by the exchange, it must be forwarded to the
server g1 using SIP trunk. The pattern 0X. meets any number that starts with 0 like
03044, 0381 etc.

What if the server g1 is down? We want to have a
second route to the server g2. It is defined as under

route r2(reg1, 0X., sip:g1|sip:g2)

The above statement says that if it is not possible to route the call to g1 then route it
to g2 using SIP.


"""

from Parser import Parser
from RexclException import ParsingError

class RouteParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        self.route = {}
        self.match_token("route")
        self.rname = self.get_token()
        # Check if rname exists
        if len([x for x in Parser._ast["route"] if x["rname"] == self.rname]) > 0:
            raise ParsingError("Route Name " + rname + " already exists. " + self.error_string())
        
        self.match_token(Parser._LP)
        self.reg_gw = self.get_token()
        # Check that the reg_gw exists
        # Check for reg first
        self.check_reg_gw_exist(self.reg_gw)
        self.route['rname'] = self.reg_gw
        self.match_token(Parser._COMMA)
        self.pattern = self.get_token_till(Parser._COMMA)
        self.route['pattern'] = self.pattern
        self.route['rdef'] = []
        self.match_token(Parser._COMMA)
        self.route['rdef'] += self.do_route_def()
        self.match_token(Parser._RP)
        self.check_for_extra_chars()
        Parser._ast["route"].append(self.route)
        
        
    def do_route_def(self):
        rv = []
        rd = {}
        tech = self.get_token()
        if tech != "pri" and tech != "sip":
            raise ParsingError("Unknown Technology: " + tech + ". " + self.error_string())            
        rd['tech'] = tech
        #rd['rname'] = self.rname
        #rd['pattern'] = self.pattern
        self.match_token(':')
        reg_gw = self.get_token()
        # check that the reg r gw exists.
        self.check_reg_gw_exist(reg_gw)
        rd['name'] = reg_gw
        ch = self.look_ahead()
        # if ch == '|':
            # Next route def starts
            #print("** Got Here **")
            #self.match_token('|')
            #rv.append(self.do_route_def())
        if ch == ':':
            self.match_token(':')
            fun = self.get_token()
            if fun == "prefix" or fun == "postfix":
                self.match_token(Parser._LP)
                pstr = self.get_token()
                self.match_token(Parser._RP)
                rd['fname'] = fun
                rd['val'] = pstr
            elif fun == "slice":
                self.match_token(Parser._LP)
                offset = self.get_token()
                if (self.look_ahead() == ':'):
                    self.match_token(':')
                    length = self.get_token()
                    offset += ":" + length
                self.match_token(Parser._RP)
                rd['fname'] = fun
                rd['val'] = offset
            elif fun == "preslice":
                pass
            else:
                raise ParsingError("Unknown route function " + fun + ". " + self.error_string())
        ch = self.look_ahead()
        if ch == '|':
            self.match_token('|')
            rv += self.do_route_def()

        rv.append(rd)
        return rv

    def check_reg_gw_exist(self, reg_gw):
        if (len(
            [x for x in Parser._ast["registrar"] if x["name"] == reg_gw]
            ) == 0) and (len([x for x in Parser._ast["gateway"] if x["name"] == reg_gw]) == 0):
            raise ParsingError("Registrar of Gateway " + reg_gw + " does not exists. " + self.error_string())

