import os
import sys
import re
import pickle
import ipaddress
from workflow import Workflow
from workflow.background import run_in_background, is_running
from toolchain import run_script
import hashlib

idb_path = os.getenv('idb_path')

def main(wf):
    arg = wf.args[0].strip()
    log.debug(arg)

    wf.add_item(
        title="Show apps list", 
        uid="list_apps",
        valid=True,
        arg="list_apps"
    )
    
    wf.add_item(
        title="Take screenshot", 
        uid="screen_shot",
        valid=True,
        arg="screen_shot"
    )
        
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    log.debug("Hello from show_device_options")
    sys.exit(wf.run(main))
