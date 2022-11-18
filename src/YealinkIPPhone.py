from Parser import Parser
from string import Template

class YealinkIPPhone:
    _template1 = Template('MAC=$mac.cfg\n'
                          '(\n'
                          'cat << $mac\n'
                          '#!version:1.0.0.1\n'
                          '#Conf for $name, Icom: $icom\n'
                          '#Phone Model: $model\n'
                          'account.1.enable = 1\n'
                          'account.1.label = $disp_name:$icom_no:$rly_no:$byte_no\n'
                          'account.1.display_name = $disp_name\n' 
                          'account.1.auth_name = $rly_no\n' 
                          'account.1.user_name = $rly_no\n' 
                          'account.1.password = $secret\n' 
                          'account.1.cid_source = 2\n'
                          'account.1.sip_server.1.address = $regip\n'
                          'local_time.time_zone = +5:30\n'
                          'local_time.net_server1 = $ntp_server\n'
                          '$mac\n'
                          ') > $$MAC\n'
                          '\n'
                          )
    
    
    def __init__(self, model, ph):
        regip = [ x for x in Parser._ast["registrar"] if ph["reg"] == x["name"]][0]["ip"]
        mac = ph["mac"]
        ph["mac"] = mac.lower()
        ph["regip"] = regip
        ph["ntp_server"] = Parser._ast["general"]["ntp-server"]
        self.conf = self._template1.substitute(ph)
        
    def get_conf(self):
        return self.conf
    
