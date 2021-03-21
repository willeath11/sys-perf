import platform,socket,re,uuid,json,psutil,logging, subprocess, os, cpuinfo
from datetime import datetime
from dmidecode import DMIDecode
from dmidecode import DMIParse


# On Linux run as `sudo -E python3 get_platform_info.py`

# https://github.com/zaibon/py-dmidecode/blob/master/dmidecode.py


def getSystemInfo():
	try:
		info={}
		d=datetime.now()   
		info['report_time_iso']=d.isoformat()
		info['report_time_text']=d.strftime("%A, %d. %B %Y %I:%M%p")
		info['platform']=platform.system()
		info['platform_release']=platform.release()
		info['platform_version']=platform.version()
		info['architecture']=platform.machine()
		info['hostname']=socket.gethostname()
		info['ip-address']=socket.gethostbyname(socket.gethostname())

		# CPU INFO
		info['processor']=cpuinfo.get_cpu_info()['brand_raw']
		info['cpu_cores']=psutil.cpu_count(logical=False)
		info['cpu_threads']=psutil.cpu_count(logical=True)
		cpufreq = psutil.cpu_freq()
		info['cpu_max_speed']=cpufreq.max
		info['cpu_min_speed']=cpufreq.min
		info['cpu_current_speed']=cpufreq.current
		info['cpu_cpu_use_percent']=psutil.cpu_percent()
		# Memory
		svmem = psutil.virtual_memory()
		swap = psutil.swap_memory()
		info['ram_total']=svmem.total
		info['ram_available']=svmem.available
		info['ram_used']=svmem.used
		info['swap_total']=swap.total
		info['swap_free']=swap.free
		info['swap_used']=swap.used
		# SW Versions
		info['sw_python_version']=cpuinfo.get_cpu_info()['python_version']
		#info['go_version']=subprocess.run(['go', 'version'], stdout=subprocess.PIPE).stdout.decode('utf-8')
		goversion=subprocess.check_output('go version', shell=True, text=True)
		goversion=goversion.split(' ', 1)[1]
		goversion=goversion.split(' ', 1)[1]
		goversion=goversion.strip().replace('\n', '')
		info['sw_go_version']=goversion


		if info['platform']== "Darwin":
			dmi = DMIDecode()

			# dmidecode -t system
			info['system_manufacturer']=dmi.get("System")[0].get("Manufacturer")
			info['system_product']=dmi.get("System")[0].get("Product Name")

			# dmidecode -t memory
			info['memory_type']=dmi.get("Memory Device")[0].get("Type")
			info['memory_speed']=dmi.get("Memory Device")[0].get("Speed")
			info['memory_manufacturer']=dmi.get("Memory Device")[0].get("Manufacturer")
			info['memory_part']=dmi.get("Memory Device")[0].get("Part Number")

			info['cache_l1_socket']=dmi.get("Cache")[0].get("Socket Designation")
			info['cache_l1_mode']=dmi.get("Cache")[0].get("Operational Mode")
			info['cache_l1_associativity']=dmi.get("Cache")[0].get("Associativity")
			info['cache_l1_type']=dmi.get("Cache")[0].get("System Type")

			info['cache_l2_socket']=dmi.get("Cache")[1].get("Socket Designation")
			info['cache_l2_mode']=dmi.get("Cache")[1].get("Operational Mode")
			info['cache_l2_associativity']=dmi.get("Cache")[1].get("Associativity")
			info['cache_l2_type']=dmi.get("Cache")[1].get("System Type")

			info['cache_l3_socket']=dmi.get("Cache")[1].get("Socket Designation")
			info['cache_l3_mode']=dmi.get("Cache")[1].get("Operational Mode")
			info['cache_l3_associativity']=dmi.get("Cache")[1].get("Associativity")
			info['cache_l3_type']=dmi.get("Cache")[1].get("System Type")


			# dmidecode -t baseboard
			info['baseboard_product']=dmi.get("Baseboard")[0].get("Product Name")
			info['baseboard_version']=dmi.get("Baseboard")[0].get("Version")


			print("if Darwin")
			# fill in gpu, cache info, other ?
			cache_l1_size=subprocess.check_output('sysctl hw.l1dcachesize', shell=True, text=True)
			cache_l1_size=cache_l1_size.split(' ', 1)[1].strip().replace('\n', '')
			info['cache_l1_size']=cache_l1_size
			cache_l2_size=subprocess.check_output('sysctl hw.l2cachesize', shell=True, text=True)
			cache_l2_size=cache_l2_size.split(' ', 1)[1].strip().replace('\n', '')
			info['cache_l2_size']=cache_l2_size
			cache_l3_size=subprocess.check_output('sysctl hw.l3cachesize', shell=True, text=True)
			cache_l3_size=cache_l3_size.split(' ', 1)[1].strip().replace('\n', '')
			info['cache_l3_size']=cache_l3_size
		elif info['architecture']=="aarch64":
			network_interface=subprocess.check_output('lshw -c network | grep -m1 product', shell=True, text=True)
			network_interface=network_interface.split(':', 1)[1].split(' ', 1)[1].strip().replace('\n', '')
			info['network_interface']=network_interface
			network_capacity=subprocess.check_output('lshw -c network | grep -m1 capacity', shell=True, text=True)
			network_capacity=network_capacity.split(':', 1)[1].split(' ', 1)[1].strip().replace('\n', '')
			info['network_capacity']=network_capacity
			system_product=subprocess.check_output('lshw -c display | grep product', shell=True, text=True)
			system_product=system_product.split(' ', 1)[1].strip().replace('\n', '')
			info['system_product']=system_product


                        
		elif info['platform']== "Linux":
			dmi = DMIDecode()

			# dmidecode -t system
			info['system_manufacturer']=dmi.get("System")[0].get("Manufacturer")
			info['system_product']=dmi.get("System")[0].get("Product Name")

			# dmidecode -t memory
			info['memory_type']=dmi.get("Memory Device")[0].get("Type")
			info['memory_speed']=dmi.get("Memory Device")[0].get("Speed")
			info['memory_manufacturer']=dmi.get("Memory Device")[0].get("Manufacturer")
			info['memory_part']=dmi.get("Memory Device")[0].get("Part Number")

			info['cache_l1_socket']=dmi.get("Cache")[0].get("Socket Designation")
			info['cache_l1_mode']=dmi.get("Cache")[0].get("Operational Mode")
			info['cache_l1_associativity']=dmi.get("Cache")[0].get("Associativity")
			info['cache_l1_type']=dmi.get("Cache")[0].get("System Type")

			info['cache_l2_socket']=dmi.get("Cache")[1].get("Socket Designation")
			info['cache_l2_mode']=dmi.get("Cache")[1].get("Operational Mode")
			info['cache_l2_associativity']=dmi.get("Cache")[1].get("Associativity")
			info['cache_l2_type']=dmi.get("Cache")[1].get("System Type")

			info['cache_l3_socket']=dmi.get("Cache")[1].get("Socket Designation")
			info['cache_l3_mode']=dmi.get("Cache")[1].get("Operational Mode")
			info['cache_l3_associativity']=dmi.get("Cache")[1].get("Associativity")
			info['cache_l3_type']=dmi.get("Cache")[1].get("System Type")


			# dmidecode -t baseboard
			info['baseboard_product']=dmi.get("Baseboard")[0].get("Product Name")
			info['baseboard_version']=dmi.get("Baseboard")[0].get("Version")
			print("if Linux")
			# Check if running as root .... provide a warning if not
			root_user = (os.getuid() == 0 and True or False)
			if not root_user:
				print("####")
				print("####  NOT RUNNING AS ROOT")
				print("####")
			# fill in gpu, cache info, other ?
			gpu=subprocess.check_output('lshw -c display | grep product', shell=True, text=True)
			gpu=gpu.split(' ', 1)[1]
			gpu=gpu.strip().replace('\n', '')
			info['gpu']=gpu
			network_interface=subprocess.check_output('lshw -c network | grep -m1 product', shell=True, text=True)
			network_interface=network_interface.split(':', 1)[1].split(' ', 1)[1].strip().replace('\n', '')
			info['network_interface']=network_interface
			network_capacity=subprocess.check_output('lshw -c network | grep -m1 capacity', shell=True, text=True)
			network_capacity=network_capacity.split(':', 1)[1].split(' ', 1)[1].strip().replace('\n', '')
			info['network_capacity']=network_capacity

			info['cache_l1_size']=dmi.get("Cache")[0].get("Installed Size")
			info['cache_l2_size']=dmi.get("Cache")[1].get("Installed Size")
			info['cache_l3_size']=dmi.get("Cache")[2].get("Installed Size")

		else:
			print("not linux or darwin")

		return info

	except Exception as e:
		logging.exception(e)



#print(json.dumps(getSystemInfo(), indent=4, sort_keys=True))
with open('platform_info.json', 'w') as outfile:
    json.dump(getSystemInfo(), outfile,indent=4, sort_keys=True,)
