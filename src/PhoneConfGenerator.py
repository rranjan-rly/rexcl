from IPPhoneParser import IPPhoneFactory
from Parser import Parser

class PhoneConfGenerator:
    def __init__(self):    
        ipphones = [ x for x in Parser._ast["phone"] if x["mac"] != "" ]
        self.conf = ""
        print(ipphones)
        for p in ipphones:
            self.conf += IPPhoneFactory(p["model"], p).get_conf()
        with open("ipphone.sh", 'w') as f:
            f.write(self.conf)
        
    
    
    
    
    