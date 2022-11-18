
from string import Template
from Parser import Parser

class AsteriskSIPFile:
    _gateway_t = Template('[sip-$gw]\n'
                         'context=rly\nqualify=yes\n'
                         'type=friend\ndisallow=all\n'
                         'allow=alaw\nallow=ulaw\nallow=gsm\n'
                         'host=$ip\n\n')
                         
    phone_t = Template('[$rly_no]\ntype=friend\nsecret=$secret\n'
                       'context=icom-$icom\nqualify=yes\nhost=dynamic\n'
                       'callcounter=yes\nnotifyhold=yes\nnotifyringing=yes\n'
                       'allowsubscribe=yes\ndtmfmode=rfc2833\n'
                       'cc_agent_policy=generic\ncc_monitor_policy=generic\n'
                       'sendrpid=pai\ntrustrpid=yes\nbusylevel=1\n'
                       'disallow=all\nallow=alaw\nallow=ulaw\nallow=gsm\n'
                       'callerid="$disp_name"<>\n'
                       'setvar=CLI_ICOM="$disp_name"<$icom_no>\n'
                       'setvar=CLI_RLY="$disp_name"<$rly_no>\n'
                       'setvar=CLI_BYTE="$disp_name"<$byte_no>\n'
                       'setvar=CLI_PSTN="$disp_name"<$pstn_no>\n\n')

    byte_phone_t = Template('[$rly_no]\ntype=friend\nsecret=$secret\n'
                       'context=icom-$icom-byte\nqualify=yes\nhost=dynamic\n'
                       'callcounter=yes\nnotifyhold=yes\nnotifyringing=yes\n'
                       'allowsubscribe=yes\ndtmfmode=rfc2833\n'
                       'cc_agent_policy=generic\ncc-monitor_policy=generic\n'
                       'sendrpid=pai\ntrustrpid=yes\nbusylevel=1\n'
                       'disallow=all\nallow=alaw\nallow=ulaw\nallow=gsm\n'
                       'callerid="$disp_name"<>\n'
                       'setvar=CLI_ICOM="$disp_name"<$icom_no>\n'
                       'setvar=CLI_RLY="$disp_name"<$rly_no>\n'
                       'setvar=CLI_BYTE="$disp_name"<$byte_no>\n'
                       'setvar=CLI_PSTN="$disp_name"<$pstn_no>\n\n')

    siptrunk_t = Template('[sip-$reg_name]\n'
                           'context=rly\nqualify=yes\n'
                           'type=friend\ndisallow=all\n'
                           'allow=alaw\nallow=ulaw\nallow=gsm\n'
                           'host=$reg_ip\n\n')


    def __init__(self, reg_lst, phone_lst):
        reg_gw_lst = [x for x in reg_lst]
        reg_gw_lst += [(x["name"], x["ipv4"], "") for x in Parser._ast["gateway"] ]
        for (r, i, b) in reg_gw_lst:
            rname = r
            #print ("Generation sip.conf for " + rname)
            f1 = open(r+'-'+i+'-sip.conf', 'w') or die ('Cannot open file.')
            if (b != ""): f2 = open(r+'-b-'+b+'-sip.conf', 'w') or die ('Cannot open file.')
            # do the gw sip trunks here
            #for gw in Parser._ast["gateway"]:
            #    s1 = self._gateway_t.substitute({'gw': gw["name"], 'ip': gw['ipv4']})
            #    f1.write(s1)
            #    if b!= "": f2.write(s1)
                
            # do the primary first
            for (reg, rip, rbip) in reg_gw_lst:
                if (reg == rname): continue
                s1 = AsteriskSIPFile.siptrunk_t.substitute({'reg_name': reg, 'reg_ip': rip})
                f1.write(s1)
                if b!= "": f2.write(s1)
                if (rbip != ""):
                    s1 = AsteriskSIPFile.siptrunk_t.substitute({'reg_name': reg + "-b", 'reg_ip': rbip})
                    f1.write(s1)
                    if b != "": f2.write(s1)
                    
            for x in [ v for v in phone_lst if v["reg"] == rname ]:
                if (x["byte_no"] == ""):
                    s1 = AsteriskSIPFile.phone_t.substitute(x)
                else:
                    s1 = AsteriskSIPFile.byte_phone_t.substitute(x)
                f1.write(s1)
                if b!= "": f2.write(s1)
                
        f1.close()
        if b!= "": f2.close()
        #print("+++++++++++++")
