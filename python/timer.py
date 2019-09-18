#!/usr/bin/env python

import sys
import time
import subprocess
import json
from filelock import Timeout, FileLock


# calls main_playbook to get routers configuration file
def get_feed(admin_configs):
    arg = "ansible-playbook -i " + admin_configs["ansible_hosts_file_path"] + " " + admin_configs["main_playbook_path"]
    subprocess.call(arg, shell=True)


def main():
    with open(sys.argv[1]) as json_file:
        # creation (if not exists) of file result.txt.lock in shared /tmp
        # directory in order to implement lock-unlock technique to results.json
        with open('/tmp/result.json.lock', 'w'):
            pass
        admin_configs = json.load(json_file)
        print("--> Timer Started")
        try:
            while True:
                # we need this lock to elimininate concurrent access to results.json
                # from other processes (auto mitigation mechanism) at the same time
                lock = FileLock("/tmp/result.json.lock")
                with lock.acquire(timeout=-1, poll_intervall=0.05):
                    # If timeout <= 0, there is no timeout and this
                    # method will block until the lock could be acquired
                    get_feed(admin_configs)
                time.sleep(10)
        except KeyboardInterrupt:
            print("--> Timer Stopped")
        except:
            print("--> An error occured !!!")


if __name__ == '__main__':
    main()
