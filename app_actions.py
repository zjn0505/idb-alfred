import os
from toolchain import run_script

app_name = os.getenv('app_name')
bundle_id = os.getenv('bundle_id')
idb_path = os.getenv('idb_path')
udid = os.getenv('udid')
func = os.getenv('func')

try:
    if func == "launch":
        run_script("{0} launch -f --udid {1} {2}".format(idb_path, udid, bundle_id))
    elif func == "terminate":
        run_script("{0} terminate --udid {1} {2}".format(idb_path, udid, bundle_id))
    elif func == "uninstall":
        run_script("{0} uninstall --udid {1} {2}".format(idb_path, udid, bundle_id))
    elif func == "data_path":
        result = run_script("xcrun simctl get_app_container {0} {1} data".format(udid, bundle_id))
        print(result)
except:
	print("Force stop " + app_name + " failed")