#!/usr/bin/env python3

"""

simple server usage monitoring, writing json to stdout.

usage: nohup python monitor_usage.py 3 > log.json &

@TODO
* Verify across x86/ubuntu, darwin, amd/ubuntu
* change to write to file vs print to screen, get file name as argument
* remove interval as argument
* maybe rewrite to use helper functions to reduce cut and paste fun
* expand to cover more monitoring stats
  * https://www.geeksforgeeks.org/psutil-module-in-python/   
* include timestamp

"""




import sys
import psutil
import json
import time
import subprocess

try:
    interval = int(sys.argv[1])
except IndexError:
    interval = 1

disk_bytes_read_last = disk_bytes_write_last = 0
net_bytes_read_last = net_bytes_write_last = 0
iowait_last = 0
ctx_switches_last =0
interrupts_last=0
soft_interrupts_last=0
syscalls_last=0


while True:
    disk = psutil.disk_io_counters()
    disk_bytes_read, disk_bytes_write = disk.read_bytes, disk.write_bytes
    net = psutil.net_io_counters()
    net_bytes_read, net_bytes_write = net.bytes_recv, net.bytes_sent
    iowait = psutil.cpu_times().iowait
    disks = [d.mountpoint for d in psutil.disk_partitions()]
    disks_usage = [psutil.disk_usage(d) for d in disks]
    disks_used = sum(d.used for d in disks_usage)
    disks_total = sum(d.total for d in disks_usage)
    cpu_stats=psutil.cpu_stats()
    ctx_switches =cpu_stats.ctx_switches
    interrupts=cpu_stats.interrupts
    soft_interrupts=cpu_stats.soft_interrupts
    syscalls=cpu_stats.syscalls
    
    usage = json.dumps({
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'cache_percent': round(psutil.virtual_memory().cached / psutil.virtual_memory().total * 100, 1),
        'slab_percent': round(psutil.virtual_memory().slab / psutil.virtual_memory().total * 100, 1),
        'swap_percent': psutil.swap_memory().percent,
        'disk_percent': round((disks_used / disks_total * 100), 2),
        'iowait_percent': round((iowait - iowait_last) / psutil.cpu_count() * 100, 1),
        'net_read_mb_s': '{:,}'.format(int((net_bytes_read - net_bytes_read_last) / 1024 / 1024)),
        'net_write_mb_s': '{:,}'.format(int((net_bytes_write - net_bytes_write_last) / 1024 / 1024)),
        'disk_read_mb_s': '{:,}'.format(int((disk_bytes_read - disk_bytes_read_last) / 1024 / 1024)),
        'disk_write_mb_s': '{:,}'.format(int((disk_bytes_write - disk_bytes_write_last) / 1024 / 1024)),
        'lsof': '{:,}'.format(int(subprocess.check_output('lsof -e /run/user/124/gvfs / | wc -l', shell=True).decode())),
        'net_fds': '{:,}'.format(len(psutil.net_connections())),
        'pids': '{:,}'.format(len(psutil.pids())),
        'ctx_switches' :'{:,}'.format(int((ctx_switches - ctx_switches_last))), 
        'interrupts': '{:,}'.format(int((interrupts - interrupts_last))),
        'soft_interrupts': '{:,}'.format(int((soft_interrupts - soft_interrupts_last))),
        'syscalls': '{:,}'.format(int((syscalls - syscalls_last))),
    })
    print(usage, flush=True)
    time.sleep(interval)
    net_bytes_read_last, net_bytes_write_last = net_bytes_read, net_bytes_write
    disk_bytes_read_last, disk_bytes_write_last = disk_bytes_read, disk_bytes_write
    iowait_last = iowait
    ctx_switches_last =ctx_switches
    interrupts_last=interrupts
    soft_interrupts_last=soft_interrupts
    syscalls_last=syscalls
