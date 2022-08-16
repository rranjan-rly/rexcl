
import json

from RexclException import UnknownRexclStatement
from Parser import Parser
from RegistrarParser import RegistrarParser
from IcomParser import IcomParser
from PhoneParser import PhoneParser
from AsteriskSIPFile import AsteriskSIPFile
from AsteriskExtenFile import AsteriskExtenFile
from ByteParser import ByteParser
from GatewayParser import GatewayParser
from BossSecyParser import BossSecyParser
from RouteParser import RouteParser
from ConferenceParser import ConferenceParser

class RexclParser:
    def __init__(self):
        Parser._ast["registrar"] = []
        Parser._ast["phone"] = []
        Parser._ast["gateway"] = []
        Parser._ast["route"] = []
        Parser._ast["conference"] = []
        Parser._ast["general"] = {}
        Parser._ast["general"]["rly-std-code"] = ''
        Parser._ast["general"]["pstn-std-code"] = ''
        Parser._ast["general"]["ntp-server"] = ''
        
        
    
    def parse_stmt(self, line_no, line):
        #remove the \n at the end of the line
        ln = line.strip(" \n")
        if ((len(ln) != 0) and (ln[0] != '#')):
            keyword = ln.split()[0]
            if (keyword == "registrar"):
                RegistrarParser(line_no, ln)
            elif (keyword == "icom"):
                IcomParser(line_no, ln)
            elif (keyword == "phone"):
                PhoneParser(line_no, ln)
            elif (keyword == "byte"):
                ByteParser(line_no, line)
            elif (keyword == "gateway"):
                GatewayParser(line_no, line)
            elif (keyword == "boss-secy"):
                BossSecyParser(line_no, line)
            elif (keyword == "route"):
                RouteParser(line_no, line)
            elif keyword == "conference":
                ConferenceParser(line_no, line)
            elif keyword == "rly-std-code" or keyword == "pstn-std-code" or keyword == "ntp-server":
                self.do_general(line_no, line)
            else:
                raise UnknownRexclStatement(f"Line No. {line_no}: Unknown statement: {line}")

    def do_general(self, line_no, line):
        p = Parser(line_no, line)
        val = ''
        stmt = p.get_token()
        p.match_token(Parser._LP)
        if stmt == "rly-std-code" or stmt == "pstn-std-code":
            val = p.get_token()
        elif stmt == "ntp-server":
            val = p.get_token_ipv4()
        else:
            raise ParsingError("BUG: " + p.error_string())
        p.match_token(Parser._RP)
        Parser._ast["general"][stmt] = val
        
    def print_ast(self):
        print(json.dumps(Parser._ast, indent=2))

    def gen_registrar_conf(self):
        # Make the registrar list
        reg_lst = []
        for v in Parser._ast["registrar"]:
            reg_lst.append((v["name"], v["ip"], v["bip"]))

        # Get a list of all the phones in the regsistrar reg
        #print(Parser._ast)
        AsteriskSIPFile(reg_lst, Parser._ast["phone"])
        AsteriskExtenFile(reg_lst, Parser._ast["phone"])
        
