from __future__ import print_function
import sys, os, logging, traceback
from plato.core.runner import ModelRunner


if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        config_location = sys.argv[1]        
        if not os.path.isabs(config_location):
            config_location = os.path.abspath(config_location)
        
        exit_code = 0
        try:
            ModelRunner(config_location, sys.stdout).run()
        except Exception as e:                      
            logging.error(traceback.format_exc())
            exit_code = -1
    else:
        print('ERROR: expected single argument for config directory', 
              file=sys.stderr)
        exit_code = -1
    
    sys.exit(exit_code)