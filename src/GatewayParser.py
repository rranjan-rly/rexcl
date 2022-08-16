from Parser import Parser
from RexclException import ParsingError

class GatewayParser(Parser):
    def __init__(self, line_no, line):
        Parser.__init__(self, line_no, line)
        try:
            Parser._ast["gateway"]
        except:
            Parser._ast["gateway"] = []
        
        self.match_token("gateway")
        gw_name = self.get_token()
        if gw_name in [x["name"] for x in Parser._ast["gateway"] ]:
            raise ParsingError("Gateway name " + gw_name + " exists already. " + self.error_string()) 
        
        self.match_token(Parser._LP)
        
        gw_type = self.get_token()
        if gw_type not in ['pri', 'sip', 'fxs', 'fxo']:
            raise ParsingError('Gateway type can only be pri|sip|fxs|fxo. Found ' +
                               gw_type + " . " + self.error_string())
        
        self.match_token(Parser._COMMA)
        
        gw_ports = self.get_token()
        try:
            int(gw_ports)
        except:
            raise ParsingError(gw_ports + "is not an integer. " + self.error_string())
                
        self.match_token(Parser._COMMA)
        gw_ipv4 = self.get_token_ipv4()
        self.match_token(Parser._RP)
        self.check_for_extra_chars()
        
        Parser._ast["gateway"].append({
            'name': gw_name,
            'type': gw_type,
            'nports': gw_ports,
            'ipv4': gw_ipv4})
        