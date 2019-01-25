import os
import re


def search_all_contig (filename):
    '''
    This function uses one while loop to look for all the header of each contig, and return the cursor position in a list
    '''
    f = open(filename,'r')
    f.seek(0)
    curr_pos = f.tell()
    start_pos = curr_pos
    found_pos = []
    flag = True
    while flag:
        content = f.readline()
        if len(content) == 0:
            flag = False
        elif content[0] == '>':
            start_pos = f.tell() - len(content)
            found_pos.append(start_pos)
            continue
    found_pos.append(f.seek(0,os.SEEK_END))
    f.close()
    return found_pos,filename

def create_new_file(know_pos:list,filename):
    '''
    This function uses the cursor position to create new fasta files with only one contig in each file. The name of new generated files is obtained based on the header of each contig.
    '''
    f = open(filename,'r')
    for i in range(len(know_pos)-1):
        f.seek(know_pos[i])
        header = f.readline()
        try:
            temp_file_name = re.search('>([\w]*)|',header).group(1)
        except AttributeError:
            temp_file_name = header[1:20]
        filename = temp_file_name + '.fasta'
        with open(filename,"w+") as f1:
            f.seek(know_pos[i])
            data = f.read(know_pos[i+1]-know_pos[i])
            f1.write(data)
    f.close()

if __name__ == '__main__':
    search_pos, filename = search_all_contig('W303_reference.fasta')
    create_new_file(search_pos, filename)

