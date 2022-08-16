
from string import Template
from Parser import Parser
__conf_init__ = """
[dial_icom]
; ARG1 -> icom_name
; ARG2 -> icom_no
; ARG3 -> rly_no
exten => s, 1, Set(CALLERID(all) = ${CLI_ICOM})
  same => n(common), Set(REDIR=${DB(${ARG1}-redir/${ARG2})})
  same => n, GotoIf($[${ISNULL(${REDIR})}]?internal:redir)
  same => n(internal), Dial(SIP/${ARG3}, 60, tT)
  same => n, Hangup
  same => n(redir), Goto(${REDIR}, common)


[dial_rly_remote]
; ARG1 -> rly_no
; ARG2 -> sip1
; ARG3 -> sip2
exten => s, 1, Set(CALLERID(all)=${CLI_RLY})
  same => n, Set(STATUS=${SIPPEER(${ARG1},status)})
  same => n, GotoIf($[ ${STATUS} = UNREACHABLE]?try2)
  same => n, Dial(SIP/${ARG2}/${ARG1},60, tT)
  same => n, Hangup
  same => n(try2), Dial(SIP/${ARG3}/${ARG1}, 60, tT)
  same => n, Hangup

[dial_byte_remote]
; ARG1 -> rly_no
; ARG2 -> sip1
; ARG3 -> sip2
exten => s, 1, Set(STATUS=${SIPPEER(${ARG1},status)})
  same => n, GotoIf($[ ${STATUS} = UNREACHABLE]?try2)
  same => n, Dial(SIP/${ARG2}/byte-${ARG1},60, tT)
  same => n, Hangup
  same => n(try2), Dial(SIP/${ARG3}/byte-${ARG1}, 60, tT)
  same => n, Hangup

[dial_rly_local]
; ARG1 -> rly_no
; ARG2 -> secy_no
; ARG3 -> secy_type
; ARG4 -> Should i modify CLI:(yes|no)
exten => s, 1, GotoIf($[${ARG4} = no ] ? noclimod)
  same => n, Set(CALLERID(all)=${CLI_RLY})
  same => n(noclimod), Set(REDIR=${DB(rly-redir/${ARG1})})
  same => n, GotoIf($[${REDIR} != ""]?redir)
  same => n, GotoIf($[${ARG2} = ""]?nosecy)
  same => n, GotoIf($[${CALLERID(num)} = ${ARG2}]?nosecy)
  same => n, GotoIf($[${ARG3}=only-secy]?only-secy)
  same => n, Dial(SIP/${ARG2},60,tT)
  same => n(nosecy), Dial(SIP/${ARG1},60,tT)
  same => n, Hangup
  same => n(only-secy) DIal(SIP/${ARG2},60,tT)
  same => n, Hangup
  same => n(redir), Goto(rly,${REDIR})
  

[dial_byte_local]
; ARG1 -> rly_no
exten => s, 1, Set(CALLERID(all)=${CLI_BYTE})
  same => n, Set(REDIR=${DB(byte-redir/${ARG1})})
  same => n, GotoIf($[${REDIR} != ""]?redir)
  same => n, Dial(SIP/${ARG1},60,tT)
  same => n(redir), Goto(byte-icom,${REDIR})


[change-conf-pin]
;ARG1 -> conference name
;ARG2 -> rly number of admin phone of the conference 
exten => s, 1, Answer
    same => n, Playback(conf-getpin)
    same => n, Read(pin,,4)
    same => n, Set(DB(conf/${ARG1})=${pin})
    same => n, Goto(rly,playpin-${ARG2},1)
    same => n, Hangup

"""

dial_rly_remote = """
macro dial_rly_remote( rly_no, sip1, sip2) {
  if (${SIPPEER(${sip1}, status)} = UNREACHABLE) {
    if (${sip2} != "") {
      Dial(SIP/${sip2}/${rly_no}, 60, tT);
    }
  } else {
    Dial(SIP/${sip1}/${rly_no}, 60, tT);
  }
};


macro dial_rly_local(rly_no, secy_no) {
    Set(CALLERID(all) = ${CLI_RLY});
common:
    Set(REDIR=${DB(rly-redir/${rly_no})});
    if(${REDIR} = "") {
        if (${secy_no} != "") {
            if (${CALLERID(num)} = ${secy_no}) {
                Dial(SIP/${secy_no}, 60, tT);
            }
        }
        Dial(SIP/${rly_no}, 60, tT);
    }
    goto rly,${REDIR},common;
};


"""

dial_icom = """

macro dial_icom(icom, icom_no, rly_no) {
  Set(CALLERID(all)=${CLI_RLY});
check_redir:
  Set(REDIR=${DB(${icom}-redir/${icom_no})});
  if(REDIR == "") {
    Dial(SIP/${rly_no}, 60, tT);
  } else {
    goto ${redir},check_redir;
  }
};

"""

class AsteriskExtenFile:
    __ael_init = dial_icom + dial_rly_remote
    __conf_init = __conf_init__
    icom_t_old = Template('[icom-$icom]\n'
                      'exten => $icom_no, 1, Set(CALLERID(all)=${CLI_ICOM})\n'
                      '  same => n(common), Set(REDIR=${DB($icom-redir/${EXTEN})})\n'
                      '  same => n, GotoIf($[${ISNULL(${REDIR})}]?internal:redir)\n'
                      '  same => n(internal), Dial(SIP/$rly_no, 60, tT)\n'
                      '  same => n, Hangup\n'
                      '  same => n(redir), Goto(${REDIR}, common)\n\n')

    # icom
    # icom_no
    # rly_no
    __conf_dial_icom_t = Template('exten => $icom_no, 1, GoSub(dial_icom,s,1($icom,$icom_no,$rly_no))\n')
    
    # rly_no,
    # sip1
    # sip2
    __conf_dial_rly_remote_t = Template('exten => $rly_no, 1, GoSub(dial_rly_remote,s,1(t$rly_no,$sip1,$sip2)\n')

    # rly_no
    # secy_no
    __conf_dial_rly_local_t = Template('exten => $rly_no, 1, GoSub(dial_rly_local,s,1($rly_no,$secy_no,$secy_type,yes)\n'
                                       'exten => t$rly_no, 1, GoSub(dial_rly_local,s,1($rly_no,$secy_no,$secy_type,no)\n'
                                       )
    __conf_byte_local_t = Template(
        'exten => byte-$rly_no, 1, GoSub(dial_byte_local,s,1($rly_no))\n')
    __conf_byte_remote_t = Template(
        'exten => byte-$rly_no, 1, GoSub(dial_byte_remote,s,1($rly_no,$sip1, $sip2))\n')
    
    __conf_icom_context_t = Template(
        '[icom-$icom-byte]\n'
        'include => icom-$icom\n'
        'include => byte-icom\n\n'
        '[icom-$icom]\n'
        'include => rly\n'
        'include => outgoing\n'
    )
        
    __conf_byte_t = Template('exten => $byte_no, 1, Goto(rly,byte-$rly_no,1)\n') 

    icom_t = Template('exten => $icom_no, 1, GoSub(dial_icom,s,1($icom,$icom_no,$rly_no))\n')
    # AEL templates. 
    __ael_rly_remote_t = Template('  $rly_no => { &dial_rly_remote($rly_no, $sip1, $sip2) };\n')
    __ael_rly_local_t = Template('  $rly_no => { &dial_rly_local($rly_no, $secy_no) };\n') 
    __ael_icom_context_t = Template('context icom-$icom-byte {\n'
                                  '  include {\n'
                                  '    icom-$icom;\n'
                                  '    byte-icom;\n'
                                  '  };\n'
                                  '};\n\n')
    __ael_icom_t = Template('  $icom_no => { &dial_icom($icom, $icom_no, $rly_no) };\n')
        
    # conference template
    # Arguments
    # $conf_no
    # $name
    # $admin_phone_no
    __conf_conference_local_t = Template(
        'exten => $conf_no, 1, GoSub(dial_rly_local,s,1(conf-$conf_no,,yes)\n'
        'exten => t$conf_no, 1, GoSub(dial_rly_local,s,1(conf-$conf_no,,no)\n'
        'exten => conf-$conf_no,1,Answer\n'
        '    same => n, Playback(conf-getpin)\n'
        '    same => n, Read(pin,,4)\n'
        '    same => n, Noop($${pin})\n'
        '    same => n, Set(Dbpin=$${DB(conf/snt)})\n'
        '    same => n, GotoIf($$["$${Dbpin}" != ""]?continue)\n'
        '    same => n, Set(Dbpin=0000)\n'
        '    same => n(continue), Noop($${Dbpin})\n'
        '    same => n, GotoIf($$["$${Dbpin}" != "$${pin}"]?error)\n'
        '    same => n, Confbridge($name)\n'
        '    same => n, Hangup\n'
        '    same => n(error), Playback(conf-invalidpin)\n'
        '    same => n, Hangup\n'
        ''
        'exten => playpin-$admin_phone_no, 1, Answer\n'
        '    same => n, Set(PIN=$${DB(conf/snt)})\n'
        '    same => n, SayDigits($${PIN})\n'
        '    same => n, Hangup\n'
        ''
        'exten => setpin-$admin_phone_no, 1, GoSub(change-conf-pin,s,1(snt,$${EXTEN:7}))\n\n')
    
    # $conf_no
    # $sip1
    # $sip2
    __conf_conference_remote_t = Template(
        'exten => $conf_no, 1, Goto(dial_rly_remote,s,1(t$conf_no,$sip1,$sip2))\n')
                                          
    
    def __init__(self, reg_lst, phone_lst):
        self.reg_lst = reg_lst
        self.phone_lst = phone_lst
        self.do_conf()
        
    def __write_files(self, f1, f2, c, s):
        # f1 -> main file
        # f2 -> secondary file
        # c -> check variable
        # s -> str to write to file
        # print("c: " + c + ". Str: " + s)
        f1.write(s)
        if (c != ""): f2.write(s)
        
    def __open_files(self, reg, ip_p, ip_s, exten):
        fp_name = reg + '-' + ip_p + '-exten.' + exten
        fp = open(fp_name, 'w') or die ('Cannot open file: ' + fp_name)
        fs_name = ""
        fs = ""
        if (ip_s != ""):
            fs_name = reg + '-b-' + ip_s + '-exten.' + exten
            fs = open(fs_name, 'w') or die ('Cannot open file: ' + fs_name)
        return fp, fs

    def do_conf(self):
        for (reg, ip_p, ip_s) in self.reg_lst:
            fp, fs = self.__open_files(reg, ip_p, ip_s, 'conf')
            self.__write_files(fp, fs, ip_s, self.__conf_init)
            for icom in {x['icom'] for x in self.phone_lst if x['reg'] == reg }:
                self.__write_files(fp, fs, ip_s,
                                   self.__conf_icom_context_t.substitute({
                                       'icom': icom}))
                phs = [x for x in self.phone_lst if x['icom'] == icom]
                
                for ph in phs:
                    s1 = self.__conf_dial_icom_t.substitute({
                        'icom': icom,
                        'icom_no': ph['icom_no'],
                        'rly_no': ph['rly_no']})
                    self.__write_files(fp, fs, ip_s, s1)
                self.__write_files(fp, fs, ip_s, "\n\n")
                # Now generate rly context
                self.__write_files(fp, fs, ip_s, "[rly]\n")
                for ph in self.phone_lst:
                    if ph['reg'] == reg:
                        # Local rly _no
                        s1 = self.__conf_dial_rly_local_t.substitute({
                            'rly_no': ph['rly_no'],
                            'secy_type': ph['secy_type'],
                            'secy_no': ph['secy_no']})
                        if ph["byte_no"] != "":
                            s1 += self.__conf_byte_local_t.substitute({
                                'rly_no': ph["rly_no"]})
                        self.__write_files(fp, fs, ip_s, s1)
                    else:
                        # Remote rly no
                        (r, i, p) = [x for x in self.reg_lst if x[0] == ph["reg"] ][0]
                        sip1 = r
                        sip2 = ""
                        if (p != ''): sip2 = r + '-b'
                        s1 = self.__conf_dial_rly_remote_t.substitute({
                            'rly_no': ph['rly_no'],
                            'sip1': sip1,
                            'sip2': sip2 })
                        if ph["byte_no"] != "":
                            s1 += self.__conf_byte_remote_t.substitute({
                                'rly_no': ph["rly_no"],
                                'sip1': sip1,
                                'sip2': sip2 })
                        self.__write_files(fp, fs, ip_s, s1)
                    #end if
                #end for
                self.__write_files(fp, fs, ip_s, "\n\n")
            self.__do_byte(fp, fs, ip_s)
            self.__do_route(reg, fp, fs, ip_s)
            self.__do_conference(reg, fp, fs, ip_s)
            fp.close()
            if (fs != ''): fs.close()
                    
    def __do_byte(self, fp, fs, ip_s):
        self.__write_files(fp, fs, ip_s, "[byte-icom]\n")
        byte_phones = [x for x in self.phone_lst if x["byte_no"] != "" ]
        for b in byte_phones:
            s1 = self.__conf_byte_t.substitute({
                'byte_no': b["byte_no"],
                'rly_no': b["rly_no"]})
            self.__write_files(fp, fs, ip_s, s1)
        # end for
        self.__write_files(fp, fs, ip_s, "\n\n")
              

    def __do_route(self, reg, fp, fs, ip_s):
        self.__write_files(fp, fs, ip_s, "[outgoing]\n")
        routes  = [x for x in Parser._ast["route"] if x["rname"] == reg]
        for r in routes:
            s1 = "exten => _" + r['pattern'] + ', 1, Noop\n'
            for rdef in r['rdef']:
                s1 += '  same => n, Dial(SIP/sip-' + rdef["name"] + '/'
                try:
                    rdef['fname']
                    if rdef['fname'] == "prefix":
                        s1 += rdef['val'] + "${EXTEN}"
                    elif rdef['fname'] == "postfix":
                        s1 += "${EXTEN}" + rdef['val']
                    elif rdef['fname'] == "slice":
                        s1 += "${EXTEN:" + rdef['val'] + "}"
                    #end if
                except:
                    s1 += "${EXTEN}"
                finally:
                    s1 += ", 60, tT)\n"
            s1 += "  same => n, Hangup\n\n"
            self.__write_files(fp, fs, ip_s, s1)
                

    def __do_conference(self, reg, fp, fs, ip_s):
        self.__write_files (fp, fs, ip_s, "; Generating Conference dial plans\n[rly]\n")
        for c in Parser._ast["conference"]:
            if (reg == c["reg"]):
                # This conference is defined in this registrar
                self.__write_files(fp, fs, ip_s,
                                   self.__conf_conference_local_t.substitute(c))
            else:
                sip1 = "sip-" + c["reg"]
                sip2 = ""
                bip = [x for x in Parser._ast["registrar"] if x["name"] == c["reg"]][0]["bip"]
                if bip != "":
                    sip2 = sip1 + "-b"
                self.__write_files(fp, fs, ip_s,
                                   self.__conf_conference_remote_t.substitute(
                                       {'conf_no': c['conf_no'],
                                        'sip1': sip1,
                                        'sip2': sip2}))
   
                
                    
        
        