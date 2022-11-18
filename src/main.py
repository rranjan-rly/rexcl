
from RexclException import RexclException
from RexclParser import RexclParser

import sys

if __name__ == "__main__":
    filename = sys.argv[1]
    p = RexclParser()
    line_no = 1
    with open(filename, "r") as f:
        for line in f:
            try:
                p.parse_stmt(line_no, line.strip())
            except RexclException as err:
                print(err.get_msg())
            line_no += 1
        
    p.gen_registrar_conf()
    
  #  p.print_ast()
