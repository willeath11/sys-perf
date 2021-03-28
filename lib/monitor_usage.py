#!/usr/bin/env python3

"""

simple server usage monitoring, writing json to stdout.

usage: nohup python monitor_usage.py 3 > log.json &

@TODO
* Rewrite into new file, add if/else darwin, vs linux and remove 
    * remove interval as argument
    * maybe rewrite to use helper functions to reduce cut and paste fun
    * change to write to file vs print to screen, get file name as argument
* remove syscalls, seems not used in linux
* I would like to have ability to get signals from other process with event text
    * would insert into json timeseries, in pandas use to mark test sync point
* Would like to get signal to terminate when external done
* expand to cover more monitoring stats, insert notes in rewritten monitoring on what they are and why monitor
  * https://www.geeksforgeeks.org/psutil-module-in-python/   
  * http://lira.no-ip.org:8080/doc/python-psutil-doc/html/#
* include timestamp, easy to interpret in pandas


"""




import sys
import psutil
import json
import time
import subprocess
import platform
from datetime import datetime

# Define in seconds period of reporting
interval = 1

disk_bytes_read_last = disk_bytes_write_last = 0
net_bytes_read_last = net_bytes_write_last = 0
iowait_last = 0
ctx_switches_last =0
interrupts_last=0
soft_interrupts_last=0
syscalls_last=0
i=0


while True:
    disk = psutil.disk_io_counters()
    disk_bytes_read, disk_bytes_write = disk.read_bytes, disk.write_bytes
    net = psutil.net_io_counters()
    net_bytes_read, net_bytes_write = net.bytes_recv, net.bytes_sent
    disks = [d.mountpoint for d in psutil.disk_partitions()]
    disks_usage = [psutil.disk_usage(d) for d in disks]
    disks_used = sum(d.used for d in disks_usage)
    disks_total = sum(d.total for d in disks_usage)
    cpu_stats=psutil.cpu_stats()


    info={}
    d=datetime.now()  
    info['report_time_iso']=d.isoformat()
    info['cpu_percent']= psutil.cpu_percent()
    info['memory_percent']= psutil.virtual_memory().percent
    info['swap_percent']= psutil.swap_memory().percent
    info['disk_percent']= round((disks_used / disks_total * 100), 2)
    info['net_read_mb_s']= '{:,}'.format(int((net_bytes_read - net_bytes_read_last) / 1024 / 1024))
    info['net_write_mb_s']= '{:,}'.format(int((net_bytes_write - net_bytes_write_last) / 1024 / 1024))
    info['disk_read_mb_s']= '{:,}'.format(int((disk_bytes_read - disk_bytes_read_last) / 1024 / 1024))
    info['disk_write_mb_s']= '{:,}'.format(int((disk_bytes_write - disk_bytes_write_last) / 1024 / 1024))
    info['net_read']= '{:,}'.format(int((net_bytes_read - net_bytes_read_last)))
    info['net_write']= '{:,}'.format(int((net_bytes_write - net_bytes_write_last)))
    info['disk_read']= '{:,}'.format(int((disk_bytes_read - disk_bytes_read_last)))
    info['disk_write']= '{:,}'.format(int((disk_bytes_write - disk_bytes_write_last)))

    info['pids']= '{:,}'.format(len(psutil.pids()))



    if platform.system()== "Darwin":
        print("Darwin")

    elif platform.system()== "Linux":
        ctx_switches =cpu_stats.ctx_switches
        interrupts=cpu_stats.interrupts
        soft_interrupts=cpu_stats.soft_interrupts
        syscalls=cpu_stats.syscalls
        iowait = psutil.cpu_times().iowait
        print("Linux")
        info['cache_percent'] = round(psutil.virtual_memory().cached / psutil.virtual_memory().total * 100, 1)
        info['slab_percent'] = round(psutil.virtual_memory().slab / psutil.virtual_memory().total * 100, 1)
        info['iowait_percent'] = round((iowait - iowait_last) / psutil.cpu_count() * 100, 1)
        info['net_fds'] = '{:,}'.format(len(psutil.net_connections()))
        info['ctx_switches'] = '{:,}'.format(int((ctx_switches - ctx_switches_last)))
        info['interrupts']= '{:,}'.format(int((interrupts - interrupts_last)))
        info['soft_interrupts']= '{:,}'.format(int((soft_interrupts - soft_interrupts_last)))
        info['syscalls']= '{:,}'.format(int((syscalls - syscalls_last)))
        if i==100:
            info['lsof'] = '{:,}'.format(int(subprocess.check_output('lsof -e /run/user/124/gvfs / | wc -l', shell=True).decode()))
            i=0
        else:
            i=1+1
        iowait_last = iowait
        ctx_switches_last =ctx_switches
        interrupts_last=interrupts
        soft_interrupts_last=soft_interrupts
        syscalls_last=syscalls
    else:
        print("Other")

    with open('monitor_info.json', 'a') as outfile:
        json.dump(info, outfile,indent=4, sort_keys=True,)
 
    print(info)
    time.sleep(interval)
    net_bytes_read_last, net_bytes_write_last = net_bytes_read, net_bytes_write
    disk_bytes_read_last, disk_bytes_write_last = disk_bytes_read, disk_bytes_write



