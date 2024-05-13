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
udid = os.getenv('udid')

def list_apps(args):

    apps = []

    # "~/.pyenv/versions/3.10.6/bin/idb list-apps --udid BE29599A-15DB-4826-B6B9-D52E16AEDFC3"
    raw_apps = run_script("{0} list-apps --udid {1}".format(idb_path, udid)).split('\n')

    # com.apple.reminders | Reminders | system | x86_64, arm64 | Unknown | Not Debuggable | pid=None
    # xyz.jienan.my-app-ios13.MyApp | MyApp | user | x86_64 | Running | Not Debuggable | pid=72214

    for app in raw_apps:
        infos = app.split("|")

        bundle_id = infos[0].strip() # xyz.jienan.my-app-ios13.MyApp
        app_name = infos[1].strip() # MyApp
        is_system_app = infos[2].strip() == "system"
        is_running = infos[4].strip() == "Running"
        is_debuggable = infos[5].strip() != "Not Debuggable"
        pid = infos[6].strip()[4:]

        app_info = {
                "bundle_id": bundle_id,
                "app_name": app_name,
                "is_system_app": is_system_app,
                "is_running": is_running,
                "is_debuggable": is_debuggable,
                "pid": pid
            }
        apps.append(app_info)


    apps.sort(key=lambda app: app["is_running"])
    apps.reverse()

    log.debug(apps)

    for app in apps:

        subtitle = app["bundle_id"]
        if app["is_system_app"]:
            subtitle = subtitle + " - system"
        if app["is_running"]:
            subtitle = subtitle + " - Running: 🟢"
        if app["is_debuggable"]:
            subtitle = subtitle + " - Debug: 🐞" # Sorry entomophobia

        match = app["app_name"] + " " + app["bundle_id"]

        item = wf.add_item(
            title=app["app_name"],
            subtitle=subtitle,
            uid=app["bundle_id"],
            copytext=app["bundle_id"],
            match=match,
            valid=True
        )

        item.setvar("bundle_id", app["bundle_id"])
        item.setvar("app_name", app["app_name"])
        if not app["is_running"]:
            mod = item.add_modifier("cmd", subtitle="Launch {0}".format(app["bundle_id"]))
            mod.setvar("func", "launch")
        else:
            mod = item.add_modifier("cmd", subtitle="Kill {0}".format(app["bundle_id"]))
            mod.setvar("func", "terminate")

        mod = item.add_modifier("alt", subtitle="Uninstall {0}".format(app["bundle_id"]))
        mod.setvar("func", "uninstall")

        if os.getenv("is_simulator"):
            mod = item.add_modifier("shift", subtitle="Show data path")
            mod.setvar("func", "data_path")


        # title = "{0} [simulator]".format(name) if is_simulator else name
        
        # item.setvar("udid", udid)
        # item.setvar("name", name)
        # item.setvar("is_simulator", is_simulator)
        # item.setvar("os_version", os_version)

def main(wf):
    arg = wf.args[0].strip()
    log.debug(arg)

    list_apps(arg)
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    log.debug("Hello from list_apps")
    sys.exit(wf.run(main))
