
from RexclException import NotAnIpAddress, TokenNotMatched
from RexclException import ExtraCharsInLine 
from RexclException import ParsingError 

class Parser:
    _ast = {}
    _COMMA = ","
    _LP = "("
    _RP = ")"
    def __init__(self, line_no, line):
        """
        Instantiates various housekeeping variables.
        self.line: This is the original line given to the parser to parse.
        self.line_no: This is the line number passed to the parser. Used to
        provide helpful error messages.
        self.lst: A list containing all the words of the line.
        self.current_token: This is the current parsed token.
        self.length is the length of the line.
        self.curp: The curret pointer.
        """
        self.line = line
        self.line_no = line_no
        self.lst = [x for x in line] # lst is an array of chars for line
        self.current_token = ""
        self.length = len(line)
        self.curp = 0;

    def eat_white(self):
        """
        This function reads the white space from the current input cursor.
        The white space is discarded. A SPACE and a TAB character is considered
        white space by this method. 
        """
        if self.curp < len(self.lst):
            while(self.lst[self.curp] == ' ' or self.lst[self.curp] == '\t'):
                self.curp += 1;
                if self.curp == len(self.lst):
                    break
        #end while

    def match_token(self, token):
        t = [x for x in token]
        i = 0
        self.eat_white()
        str_start = self.curp;
        for c in t:
            if (c != self.lst[self.curp]):
                raise TokenNotMatched("Expecting " + token +
                                      self.error_string())
            self.curp += 1
        #end for
        self.current_token = self.line[str_start:self.curp]

    def look_ahead(self):
        try:
            self.eat_white()
            return self.lst[self.curp]
        except IndexError:
            raise ParsingError('Unexpected End of line. ' + self.error_string())
            

    def get_token(self):
        self.eat_white()
        token_start = self.curp
        try:
            while(self.lst[self.curp].isalnum() or
                  self.lst[self.curp] == '_' or
                  self.lst[self.curp] == '-'):
                #print(self.line + ":" + self.line[token_start:self.curp+1])
                self.curp += 1
        except IndexError:
            pass
            
        self.current_token = self.line[token_start:self.curp]
        #print ('Token: "' + self.current_token + '"')
        return self.current_token
    
    def get_token_till(self, ch):
        self.eat_white()
        token_start = self.curp
        while(self.lst[self.curp] != ch):
            self.curp += 1
        self.current_token = self.line[token_start:self.curp]
        return self.current_token
    
    def get_token_ipv4(self):
        self.eat_white()
        token_start = self.curp
        f = self.curp
        token_len = 0

        for times in [1, 2, 3, 4]:
            while(self.lst[self.curp].isdigit()):
                token_len += 1
                self.curp += 1

            if (token_len == 0):
                raise NotAnIpAddress("Octets of IP address should start with a digit.\n" + self.error_string())
            
            if(self.lst[self.curp] != '.'):
                if (times != 4):
                    raise NotAnIpAddress("Expecting a dot character.")

            self.current_token = self.line[f:self.curp]
            if(int(self.current_token) > 255):
                raise NotAnIPAddress("Octet of an IP address shall be less than 255.")

            self.curp += 1
            f = self.curp
            token_len = 0;
        #end for
        #adjust the self.fcurp to the point to the next char not yet recognised.
        self.curp -= 1
        self.current_token = self.line[token_start:self.curp]
        return self.current_token

    def error_string(self):
        rv = "\nLine No. " + str(self.line_no) + "\n" 
        rv += self.line + "\n"
        rv += ' ' * self.curp
        rv += "^ Error encountered here.\n"
        return rv

    def check_for_extra_chars(self, comment_chars = "#"):
        self.eat_white()
        try:
            if (self.lst[self.curp] not in list(comment_chars)):
                raise ExtraCharsInLine("Extra Characters in line. " + self.error_string())
        except IndexError:
            #encounters when the end of line is reached
            pass;
