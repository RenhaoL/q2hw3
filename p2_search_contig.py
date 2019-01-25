import os
import re
from collections import defaultdict


def search_a_contig (filename, search_list:list):
    '''
    This function looks for the starting and ending postion of each contig in the given list. And those information will be used in a different function to create individual files as results.
    '''
    f = open(filename,'r')
    f.seek(0)
    curr_pos = f.tell()
    start_pos = curr_pos
    result_dict = defaultdict(int) # I store the header as key, and the starting postion of the header as value.
    found_pos = []

    searchable = [] # list contains header with no special characters.
    for i in search_list:
        searchable.append(re.search('\>?([\w]*)|',i).group(1))

    flag = True
    while flag:
        content = f.readline()
        if len(content) == 0:
            flag = False
        elif content[0] == '>':
            start_pos = f.tell() - len(content)
            found_pos.append(start_pos)
            protential_header = re.search('>([\w]*)|',content).group(1)
            if protential_header in searchable:
                result_dict[protential_header] = start_pos
            continue

    found_pos.append(f.seek(0,os.SEEK_END))
    f.close()
    return found_pos, result_dict, filename

def create_new_file(know_pos:list, give_dict:dict, filename):
    '''
    This function creates new individual files for each contig that entered for search.
    The name of new generated files is obtained based on the header of each contig.
    '''
    f = open(filename,'r')

    for k in give_dict.keys():
        starting_pos = give_dict[k]
        ending_pos = know_pos[know_pos.index(starting_pos)+1]
        file_name = k + '.fasta'
        with open(file_name,"w+") as f1:
            f.seek(starting_pos)
            data = f.read(ending_pos-starting_pos)
            f1.write(data)
    f.close()

if __name__ == '__main__':
    # enter the file name and the list contains all the contig headers as parameter and call function "search_a_contig"
    search_pos, result_dict, filename = search_a_contig('W303_reference.fasta',['>scf7180000000085 | quiver'])
    create_new_file(search_pos, result_dict, filename)
