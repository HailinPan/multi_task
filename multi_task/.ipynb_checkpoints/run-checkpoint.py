import os
import re
import time
import glob
from typing import Optional, Tuple, Union, List
import numpy as np
import pandas as pd
from multiprocessing import Pool


def read_cmd_file(
    cmd_file: str
) -> pd.DataFrame:
    f = open(cmd_file, 'rt')
    cmds = f.readlines()
    cmds = [i.strip() for i in cmds]
    cmds = [" ".join(one_line.split()) for one_line in cmds] # remove more than one consecutive space as one
    cmd_df = pd.DataFrame({'cmd':cmds, 'index': range(1, len(cmds)+1)})
    cmd_df['index'] = ["{:0>5d}".format(i) for i in cmd_df['index']]
    return cmd_df

def prepare_log_dir(
    cmd_file: str
) -> str:
    dir_name = os.path.basename(cmd_file) + '.log'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    return dir_name


def collect_finished_indexs(
    log_dir: str
) -> List:
    finish_indexs = []
    log_files = glob.glob(f'{log_dir}/work*.log')
    for one_log_file in log_files:
        if is_finish(one_log_file):
            index = re.search(r'work(\d+)\.log$', one_log_file).group(1)
            finish_indexs.append(index)
    return finish_indexs

def is_finish(one_log_file):
    finish = False
    try:
        last_line = open(one_log_file, 'rt').readlines()[-1]
    except:
        last_line = None
    
    if last_line != None:
        last_line = last_line.strip()
    
    if last_line == 'This_work_has_completed':
        finish = True
    return finish


    
def polish_cmd_df(cmd_df, log_dir):
    cmd_df['polish_cmd'] = cmd_df['cmd'] + f" > {log_dir}/work" + cmd_df['index'] + ".log" + f" 2>{log_dir}/work" + cmd_df['index'] + ".log" + f" && echo This_work_has_completed >> {log_dir}/work" + cmd_df['index'] + ".log"
    return cmd_df

def os_sys(cmd):
    os.system(cmd)

def _run_cmds(
    cmd_file: str,
    task_num: int = 1,
):
    cmd_df = read_cmd_file(cmd_file)
    log_dir = prepare_log_dir(cmd_file)
    finished_indexs = collect_finished_indexs(log_dir)
    cmd_df = cmd_df[~np.isin(cmd_df['index'], finished_indexs)]

    cmd_df = polish_cmd_df(cmd_df, log_dir)
    cmds = [(i,) for i in cmd_df['polish_cmd']] 
    with Pool(task_num) as p:
        p.starmap(os_sys, cmds)



def run_cmds(
    cmd_file: str,
    task_num: int = 1,
    try_time: int = 10,
):
    for i in range(try_time):
        _run_cmds(cmd_file=cmd_file, task_num=task_num)
        
