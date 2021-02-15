import argparse
from ChineseMapDrawer import Chinese_Map_Drawer
def parse_arguments():
    '''
    cmd line argparse for chinesemapdrawer
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('colortype',help='input a sting of intended colortypr, can be YlGn, YlGn_r, mono')
    args = parser.parse_args()
    return args

def run_prog():
    "run the cmd line prog"
    args = parse_arguments()
    Chinese_Map_Drawer(args.colortype)