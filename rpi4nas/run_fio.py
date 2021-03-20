import os
import time
import subprocess
import argparse

parser= argparse.ArgumentParser(description="Benchmark wrapper for FIO across OS types")
parser.add_argument("--OSX", help="specifys running on OSX, default is Ubuntu", action="store_true")
parser.add_argument("--WIN", help="specifys running on windows, default is Ubuntu", action="store_true")

args = parser.parse_args()

if args.OSX:
  print("Running on OSX")
  fio_ioengine="posixaio"
elif args.WIN:
  fio_ioengine="windowsaio"
else:	
  fio_ioengine="libaio"
 
#fio_size="1G" # size in fio
fio_size="100M"
fio_runtime="5" # runtime in fio for time_based tests
#fio_directory="/mnt/sda1/tmp"
fio_directory="./tmp"



# ok do each type in outer loop 
for run in ('write', 'randwrite', 'read', 'randread'):
  # Preconditioning (does this work ?)
  print("doing Preconditioning for", run)
  precondition_command= "sudo fio --minimal -name=precondition-fio --bs=128k "+" --ioengine="+fio_ioengine+" --iodepth=16 --size="+fio_size+" --direct=1 --rw=write --directory "+fio_directory+" --numjobs=1 --time_based --runtime=5 --group_reporting"
  precondition_output = subprocess.check_output(precondition_command, shell=True)
  print(precondition_output)

  for blocksize in ('512', '4k', '512k', '10m'):
     for numjobs in (1, 32, 64):
        for iodepth in (1, 32, 128):
           command = "sudo fio --minimal --terse-version=2 -name=temp-fio --bs="+str(blocksize)+" --ioengine="+fio_ioengine+" --iodepth="+str(iodepth)+" --size="+fio_size+" --direct=1 --rw="+str(run)+" --directory "+fio_directory+" --numjobs="+str(numjobs)+" --time_based --runtime="+fio_runtime+" --group_reporting --output-format=json+"
           print (command)
 