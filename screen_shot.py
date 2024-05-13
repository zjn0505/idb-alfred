import os
import sys
import re
import pickle
import ipaddress
from workflow import Workflow
from workflow.background import run_in_background, is_running
from toolchain import run_script
from toolchain import call_script
import hashlib
import time


idb_path = os.getenv('idb_path')
udid = os.getenv('udid')
datetime = time.time()

def screenshot(args):

    # "~/.pyenv/versions/3.10.6/bin/idb screenshot --udid BE29599A-15DB-4826-B6B9-D52E16AEDFC3 "
    local_path = "/tmp/screenshot_{0}.jpg".format(datetime)
    run_script("{0} screenshot --udid {1} {2}".format(idb_path, udid, local_path))
    
    if call_script(['which', 'osascript']) == 0:
        shell_cmd_4 = "osascript -e 'on run args' -e 'set thisFile to item 1 of args' -e 'set the clipboard to (read thisFile as JPEG picture)' -e return -e end {0}".format(local_path)
        run_script(shell_cmd_4)
    elif call_script(['which', 'xclip']) == 0:
        run_script("xclip -selection clipboard -t image/jpg -i {0}".format(local_path))
        run_script("rm {0}".format(local_path))
    print("Screenshot captured to clipboard")

def main(wf):
    arg = wf.args[0].strip()
    log.debug(arg)

    screenshot(arg)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    log.debug("Hello from screenshot")
    sys.exit(wf.run(main))
