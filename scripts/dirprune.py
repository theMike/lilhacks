
import os

def globdirs(startdir):
    return [os.path.join(startdir,dir) for dir in os.listdir(startdir)
                if os.path.isdir(os.path.join(startdir,dir))]

def globsubdirs(startdir):
    return [dir for dir in os.listdir(startdir)
                if os.path.isdir(os.path.join(startdir,dir))]

def try_ints(s):
    try:
        return int(s)
    except:
        return s

def natsort_key(s):
    import re
    return map(try_int, re.findall(r'(\d+|\D+)',s))

def natcmp(a,b):
    return cmp(natsort_key(a),natsort_key(b))

def natcasecmd(a,b):
    return natcmp(a.lower(),b.lower())

def natsort(seq,cmp=natcmp,reverse=False):
    if reverse:
        seq.sort(cmp, reverse=True)
    else:
        seq.sort(cmp)

def natsorted(seq,cmd=natcmp, reverse=False):
    import copy
    temp = copy.copy(seq)
    natsort(temp, cmp, reverse)
    return temp

def to_delete(sorted_dir_list, list_length):
    return [d for d, val in enumerate(sorted_dir_list) if len(sorted_dir_list) > list_length]

def main():
    rootdir = r"E:\develop\work\testdir"
    #get product leve dirs
    product_dirs=globdirs(rootdir)
    #get build level dirs
    for bdir in product_dirs:
        build_dirs=globsubdirs(bdir)
        newsorted = natsorted(build_dirs)

        print( newsorted)
        to_delete_list=[]
        to_delete_list = to_delete(newsorted, 4)
        print( to_delete_list)

    pass

if __name__ == '__main__':
    main()
