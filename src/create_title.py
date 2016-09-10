import os
index_path = ('../Index/MyTitle')

f = open(os.path.abspath(index_path))
path = '../Index/Title/'
count = 1
temp_list = []
store_index = []

def write_out(count,prefix,lines,factor):
    output_name = path + prefix + str(count/factor)
    output_file = open(os.path.abspath(output_name),"w")
    for line in lines:
        output_file.write(line)
    rem_first = lines[0][:-1].split(" ")[0] + " " + prefix +str(count/factor) + " NotLeaf\n"
    return rem_first

with open(os.path.abspath(index_path)) as IndexFile:
    for line in IndexFile:
        if(count%500 == 0):
            store_index.append(write_out(count,"",temp_list,500))
            temp_list = []
        temp_list.append(line)
        count += 1

if(len(temp_list)!=0):
    store_index.append(write_out(count+500,"",temp_list,500))
    temp_list = []


indexno = 0
while(len(store_index) > 200):
    store_top = []
    temp_index = []
    count = 1
    for i in store_index:
        if(count%200 == 0):
            store_top.append(write_out(count,"L" + str(indexno),temp_index,200))
            temp_index = []
        temp_index.append(i)
        count += 1
    if(len(temp_index)!=0):
        store_top.append(write_out(count+200,"L" + str(indexno),temp_index,200))
        temp_index = []
    indexno+=1
    store_index = store_top

name = path + 'main'
out = open(os.path.abspath(name),"w")
for i in store_index:
    out.write(i)
    count += 1

