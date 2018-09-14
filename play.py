# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 18:28:04 2018

@author: lilhope,zhangguijie,zhanghongli
"""

import psutil
import argparse
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import time
import sys
import os

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pid',type=int,help="listening pid",default=11648)
    parser.add_argument('--view',type=str,help="view style,cmd,img or file",default='img')
    parser.add_argument('--time',type=int,help="monitor time,seconds",default=100)
    return parser.parse_args()

def get_info(pid):
    """given target pid,get the cpu and memory information
       args:
           pid:the pid of process
       return:
           num_cpus: total number of cpus
           cpu_usage: total cpu usage
           mem_usage: total memory usage
           mem_free: total free memory
           target_cpu_usage: the cpu usage of target pid
           target_mem_usage: the memory usage of target pid
           total_mem: total memory
    """
    num_cpus = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent()
    mem_info = psutil.virtual_memory()
    mem_usage = mem_info.percent
    mem_free = float(mem_info.free) / 1024 / 1024 / 1024
    total_mem = float(mem_info.total) / 1024 / 1024 / 1024
    target = psutil.Process(pid)
    target_cpu_usage = target.cpu_percent()
    target_mem_usage = round(target.memory_percent(),2)
    datum = {"num_cpus":num_cpus,
             "cpu_usage":cpu_usage,
             "mem_usage":mem_usage,
             "mem_free":mem_free,
             "target_cpu_usage":target_cpu_usage,
             "target_mem_usage":target_mem_usage,
             'total_mem':total_mem}
    return datum

def main():
    args = arg_parse()
    if args.view =="cmd":
        pass
    if args.view == "img":
        cpu_usage,target_cpu_usage,mem_free,mem_usage,target_mem_usage,count = [],[],[],[],[],[]
        plt.figure(figsize=(16, 12), dpi=80)
        plt.ion()
        for j in range(args.time):
            datum = get_info(args.pid)
            cpu_usage.append(datum['cpu_usage'])
            target_cpu_usage.append(datum['target_cpu_usage'])
            mem_usage.append(datum['mem_usage'])
            target_mem_usage.append(datum['target_mem_usage'])
            count.append(j)
            
            num_cpus = datum['num_cpus']
            total_mem = datum['total_mem']
            plt.cla()
            #fig,ax = plt.subplots(nrows=2,ncols=1)
            plt.subplot(2,1,1)
            avg_cpu_usage = np.mean(np.array(cpu_usage))
            avg_target_cpu_usage = np.mean(np.array(target_cpu_usage))
            cpu_title = "num of cpus:{} avg_cpu_usage:{:.2f} avg_target_cpu_usage:{:.2f}".format(num_cpus,avg_cpu_usage,avg_target_cpu_usage)
            plt.title(cpu_title,fontsize=16)
            plt.grid(True)
            plt.xlabel("Time")
            #
            #plt.xticks(count)
            
            plt.ylabel("cpu usage")
            #print(len(count))
            plt.ylim(-10,100)
            plt.yticks(np.linspace(0,110,10,endpoint=True))
            plt.plot(count,cpu_usage,"b--", linewidth=2.0, label="cpu_usage")
            plt.plot(count,target_cpu_usage,"r-", linewidth=2.0, label="target_cpu_usage")

            plt.subplot(2,1,2)
            avg_mem_usage = np.mean(np.array(mem_usage))
            avg_target_mem_usage = np.mean(np.array(target_mem_usage))
            mem_title = "total of memory {:2f} GB,avg mem usage{:.2f},avg target mem usage:{:.2f}".format(total_mem,avg_mem_usage,avg_target_mem_usage) 
            plt.title(mem_title,fontsize=16)
            plt.xlabel("Time")
            plt.ylabel("memory usage")
            plt.ylim(-10,100)
            plt.yticks(np.linspace(0,110,10,endpoint=True))
            plt.plot(count,mem_usage,"b--", linewidth=2.0, label="cpu_usage")
            plt.plot(count,target_mem_usage, "r-", linewidth=2.0, label="target_cpu_usage")
            plt.show()
            plt.pause(1)
        plt.ioff()
        plt.show()
    elif args.view=="cmd":
        cpu_usage,target_cpu_usage,mem_free,mem_usage,target_mem_usage = [],[],[],[],[]
        for _ in range(args.time):
            datum = get_info(args.pid)
            cpu_usage.append(datum["cpu_usage"])
            target_cpu_usage.append(datum["target_cpu_usage"])
            mem_usage.append(datum["mem_usage"])
            target_mem_usage.append(datum["target_mem_usage"])
            avg_cpu_usage = round(np.mean(np.array(cpu_usage)),2)
            avg_target_cpu_usage = round(np.mean(np.array(target_cpu_usage)),2)
            avg_mem_usage = round(np.mean(np.array(mem_usage)),2)
            avg_target_mem_usage = round(np.mean(np.array(target_mem_usage)),2)
            out_str = "cpu_usage:"+"====>>"+str(datum["cpu_usage"]) + "    " + \
                      "target_cpu_usage"+"====>>" + str(datum["target_cpu_usage"]) +"    " \
                      "avg_target_cpu_usage" + "====>>" + str(avg_target_cpu_usage) + "    " + \
                      "target_mem_usage" + "++++>>" + str(datum["target_mem_usage"]) + "    " + \
                      "avg_tar_mem_usage" + "++++>>" + str(avg_target_mem_usage)
            print("\r",out_str,end="",flush=True)
            #print("cpu_usage:"+bar(datum["cpu_usage"])+str(datum["cpu_usage"]))
            sys.stdout.flush()
            time.sleep(1)
    elif args.view=="file":
        out_file = './sys_monitor.log'
        with open(out_file,"w") as f:
            f.writelines("Hello,welcom to use the huaq process monitor!"+'\n')
            for j in range(args.time):
                datum = get_info(args.pid)
                
                cpu_usage,target_cpu_usage,mem_free,mem_usage,target_mem_usage = [],[],[],[],[]
                cpu_usage.append(datum["cpu_usage"])
                target_cpu_usage.append(datum["target_cpu_usage"])
                mem_usage.append(datum["mem_usage"])
                target_mem_usage.append(datum["target_mem_usage"])
                avg_cpu_usage = round(np.mean(np.array(cpu_usage)),2)
                avg_target_cpu_usage = round(np.mean(np.array(target_cpu_usage)),2)
                avg_mem_usage = round(np.mean(np.array(mem_usage)),2)
                avg_target_mem_usage = round(np.mean(np.array(target_mem_usage)),2)
                f.writelines("+++++++++++++++++++++++++++++++++\n")
                f.writelines("Time:" + time.asctime(time.localtime(time.time())) + '\n')
                f.writelines("cpu_usage:"+"====>>"+str(datum["cpu_usage"]) + "\n" + \
                      "target_cpu_usage"+"====>>" + str(datum["target_cpu_usage"]) +"\n" \
                      "avg_target_cpu_usage" + "====>>" + str(avg_target_cpu_usage) + "\n" + \
                      "target_mem_usage" + "++++>>" + str(datum["target_mem_usage"]) + "\n" + \
                      "avg_tar_mem_usage" + "++++>>" + str(avg_target_mem_usage) + "\n")
                if datum["cpu_usage"] > 80.0:
                    f.writelines("warning:the cpu usage override 80%")
                if datum["mem_usage"] > 80.0:
                    f.writelines("warning:the cpu usage override 80%")
                f.writelines('\n')
            
if __name__ =="__main__":
    main()
