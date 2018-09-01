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

def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pid',type=int,help="listening pid",default=11648)
    parser.add_argument('--view',type=str,help="view style,cmd,img or file",default='img')
    parser.add_argument('--time',type=int,help="monitor time,seconds",default=100)
    return parser.parse_args()

def get_info(pid):
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
def bar(num):
    #return "=="*(int(num/10) + 1) + ">>"
    return "========"+">>"

def plot_dynamic_img(cpu_usage,target_cpu_usage,mem_free,target_mem_usage,count,num_cpus,total_mems):
    
    plt.pause(1)
def flush_cmd(datum):
    pass


def flush_file(datum):
    pass
def main():
    args = arg_parse()
    if args.view =="cmd":
        pass
    if args.view == "img":
        cpu_usage = [50. for i in range(20)]
        target_cpu_usage = [50. for i in range(20)]
        mem_free = [6.0 for i in range(20)]
        mem_usage = [50. for i in range(20)]
        target_mem_usage = [4.0 for i in range(20)]
        count = [0 for i in range(20)]
        plt.figure(figsize=(16, 12), dpi=80)
        plt.ion()
        for j in range(args.time):
            datum = get_info(args.pid)
            
            cpu_usage.pop(0)
            target_cpu_usage.pop(0)
            mem_usage.pop(0)
            target_mem_usage.pop(0)
            count.pop(0)
            
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
            plt.title("num of cpus {}".format(num_cpus))
            plt.grid(True)
            plt.xlabel("Time")
            #
            #plt.xticks(count)
            plt.ylabel("cpu usage")
            #print(len(count))
            print(target_cpu_usage)
            plt.ylim(-10,100)
            plt.yticks(np.linspace(0,110,10,endpoint=True))
            plt.plot(count,cpu_usage,"b--", linewidth=2.0, label="cpu_usage")
            plt.plot(count,target_cpu_usage,"g-", linewidth=2.0, label="target_cpu_usage")

            plt.subplot(2,1,2)
            plt.title("total of memory {} GB".format(total_mem))
            plt.xlabel("Time")
            plt.xticks(count)
            plt.ylabel("memory usage")
            plt.ylim(-10,100)
            plt.yticks(np.linspace(0,110,10,endpoint=True))
            #plt.yticks(np.linspace(0,100,9,endpoint=True))
            #print(mem_usage)
            plt.plot(count,mem_usage,"b--", linewidth=2.0, label="cpu_usage")
            plt.plot(count,target_mem_usage, "r-", linewidth=2.0, label="target_cpu_usage")
            plt.show()
            plt.pause(1)
        plt.ioff()
        plt.show()
    elif args.view=="cmd":
        cpu_usage,target_cpu_usage,mem_free,mem_usage,target_mem_usage = [],[],[],[],[]
        while(True):
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
                      "avg_target_cpu_usage" + "====>>" + str(avg_cpu_usage) + "    " + \
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
                      "avg_target_cpu_usage" + "====>>" + str(avg_cpu_usage) + "\n" + \
                      "target_mem_usage" + "++++>>" + str(datum["target_mem_usage"]) + "\n" + \
                      "avg_tar_mem_usage" + "++++>>" + str(avg_target_mem_usage) + "\n")
                if datum["cpu_usage"] > 80.0:
                    f.writelines("warning:the cpu usage override 80%")
                if datum["mem_usage"] > 80.0:
                    f.writelines("warning:the cpu usage override 80%")
                f.writelines('\n')
            
if __name__ =="__main__":
    main()
