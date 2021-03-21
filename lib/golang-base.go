package main

import (
	//"bytes"
	"fmt"
	//"net"
	"github.com/shirou/gopsutil/cpu"
	"github.com/shirou/gopsutil/disk"
	"github.com/shirou/gopsutil/host"
	"github.com/shirou/gopsutil/mem"

	//"github.com/shirou/gopsutil/net"
	//"io/ioutil"
	"log"
	"runtime"
	//"strconv"
	"os"
	"time"
)


func main() {
	statsServer()
}
func dealwithErr(err error) {
	if err != nil {
		fmt.Println(err)
		os.Exit(-1)
	}
}

func statsServer() {
	log.Printf("Staring statsServer..")


	fmt.Println("runtime.GOOS:", runtime.GOOS)

	// cpu - get CPU number of cores and speed
	cpuStat, err := cpu.Info()
	dealwithErr(err)

	fmt.Println("cpuStat[0].Family:", cpuStat[0].Family)
	fmt.Println("cpuStat[0].VendorID", cpuStat[0].VendorID)
	fmt.Println("cpuStat[0].Cores:", cpuStat[0].Cores)
	fmt.Println("cpuStat[0].ModelName:", cpuStat[0].ModelName)
	fmt.Println("cpuStat[0].Mhz:", cpuStat[0].Mhz)
	pid := os.Getpid()
	fmt.Println("statsServer PID:", pid)
	fmt.Println("----------------------------")
	fmt.Println("----------------------------")
	for {
		fmt.Println("Timestamp:", time.Now())

		//cpu
		percentage, err := cpu.Percent(100000000, true)
		dealwithErr(err)
		total := 0.0
		for _, number := range percentage {
			total = total + number
		}
		cpuavgpercent := total / float64(len(percentage))
		fmt.Println(" cpuavgpercent:", cpuavgpercent)

		// memory
		vmStat, err := mem.VirtualMemory()
		dealwithErr(err)

		fmt.Println("vmStat.Total:", vmStat.Total)
		fmt.Println("vmStat.Free:", vmStat.Free)
		fmt.Println("vmStat.UsedPercent:", vmStat.UsedPercent)

		// disk - start from "/" mount point for Linux
		// might have to change for Windows!!
		// don't have a Window to test this out, if detect OS == windows
		// then use "\" instead of "/"

		diskStat, err := disk.Usage("/")
		dealwithErr(err)

		fmt.Println("diskStat.Total:", diskStat.Total)
		//                 Diskused:     diskStat.Used,
		//                  Diskfree:     diskStat.Free,
		//                Diskusedp:    diskStat.UsedPercent,

		// host or machine kernel, uptime, platform Info
		hostStat, err := host.Info()
		dealwithErr(err)

		fmt.Println("hostStat.Procs:", hostStat.Procs)


	

		//fmt.Println("processes[pid].Ppid:", processes[pid].Ppid)
		//fmt.Println("processes[pid].CPUPercent():", processes[pid].CPUPercent()[0])

		fmt.Println("----------------------------")
		time.Sleep(time.Millisecond * 10000) // 10 second pause
	}

}
