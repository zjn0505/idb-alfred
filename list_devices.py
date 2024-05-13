import os
import sys
import re
import pickle
import ipaddress
from workflow import Workflow
from workflow.background import run_in_background, is_running
from toolchain import run_script
import hashlib

GITHUB_SLUG = 'zjn0505/idb-alfred'

idb_path = os.getenv('idb_path')


def list_devices(args):

    try:
        booted = run_script(idb_path + " list-targets | grep Booted").split('\n')
    except:
        booted = []

    # iPhone 14 Pro | BE29599A-15DB-4826-B6B9-D52E16AEDFC3 | Booted | simulator | iOS 16.0 | x86_64 | /tmp/idb/BE29599A-15DB-4826-B6B9-D52E16AEDFC3_companion.sock
    # iPod touch (7th generation) | 880B841D-B7A8-4051-B9C9-F0DBD29A6AA9 | Booted | simulator | iOS 16.0 | x86_64 | No Companion Connected
    for device in booted:
        infos = device.split("|")

        name = infos[0].strip() # iPod touch (7th generation)
        udid = infos[1].strip() # 880B841D-B7A8-4051-B9C9-AAABD29A6AA9
        is_simulator = infos[3].strip() == "simulator"
        os_version = infos[4].strip()

        log.debug("List devices {0}".format(device))

        title = "{0} [simulator]".format(name) if is_simulator else name
        item = wf.add_item(
            title=title, 
            subtitle="{0} - {1}".format(os_version, udid),
            uid=udid,
            copytext=udid,
            valid=True
        )
        item.setvar("udid", udid)
        item.setvar("name", name)
        item.setvar("is_simulator", is_simulator)
        item.setvar("os_version", os_version)


def main(wf):
    if not idb_path:
        wf.warn_empty(title="idb not found",
                      subtitle="Please config 'idb_path' in workflow settings")
    else:
        list_devices(wf.args)
    wf.send_feedback()

if __name__ == '__main__':
    # update_settings = {'github_slug': GITHUB_SLUG, 'version': VERSION}
    wf = Workflow(update_settings=None,
                  help_url="https://github.com/zjn0505/idb-alfred")
    log = wf.logger
    log.debug("Hello from idb")

    arg = wf.args[0] if wf.args else ''

    if arg == "clear cache":
        wf.clear_cache()
    elif arg == "open cache":
        wf.open_cachedir()
    elif arg == "clear data":
        wf.clear_data()
    elif arg == "open data":
        wf.open_datadir()
    elif wf.update_available:
        wf.add_item(u'New version available',
                    u'Action this item to install the update',
                    autocomplete=u'workflow:update')

    sys.exit(wf.run(main))
