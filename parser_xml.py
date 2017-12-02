# Zhihao Zhang
# 1462413


import re
import os


def trimfile():
    file_name = input()
    file_name = file_name.strip()
    lines = open(file_name, 'r').readlines()
    del lines[-1]
    del lines[0]
    open('tem_file.txt', 'w').writelines(lines)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return False


def get_title_term(line):
    title_list = list()
    title_term = find_between(line,"<title>","</title>")
    title_term = title_term.lower().strip()
    title_term = title_term.replace('.','')
    title_term = title_term.replace('\\','&92')
    # TODO will add more patter here
    p=re.compile('[-,.:;\s]+')
    title_term = p.split(title_term)
    for item in title_term:
        if len(item) <= 2 :
            continue
        else:
            title_list.append(item)
    # print(title_list)
    return title_list

def get_booktitle_term(line):
    booktitle_list = list()
    booktitle_term = find_between(line,"<booktitle>","</booktitle>")

    if booktitle_term == False:
        booktitle_list = list()
        # print(booktitle_list)
    else:
        booktitle_term = booktitle_term.lower()
        booktitle_term= booktitle_term.replace('.','')
        booktitle_term = booktitle_term.split()
        for item in booktitle_term:
            if len(item) <= 2 :
                continue
            else:
                booktitle_list.append(item)
        # print(booktitle_list)

    return booktitle_list

def get_journal_term(line):
    journal_list = list()
    journal_term = find_between(line,"<journal>","</journal>")

    if journal_term == False:
        journal_list = list()
        # print(journal_list)
    else:
        journal_term = journal_term.lower()
        journal_term = journal_term.replace('.','')
        journal_term = journal_term.split()
        for item in journal_term:
            if len(item) <= 2 :
                continue
            else:
                journal_list.append(item)
        # print(journal_list)

    return journal_list

def get_author_term(line):
    author_list= list()
    # print(line)
    while (True):
        context_author = find_between(line,"<author>","</author>")
        if context_author == False:
            break
        context_author_tem = context_author
        # Todo might add more constrain in the future
        context_author_tem = re.split(';|\s|&',context_author_tem)
        for item in context_author_tem:
            item = item.lower()
            author_list.append(item)

        text_term = "<author>" + context_author + "</author>"
        line= line.replace(text_term,'')
    # print(author_list)
    return author_list


def get_date(line):
    date_list = list()
    date_term = find_between(line,"<year>","</year>")
    # print(date_term)
    return date_term

def write_recs(key,line):
    recs = open('recs.txt','a')
    key = key.strip('"')
    recs.writelines(key +':'+line)
    recs.close()
def write_year(year,key):
    years_txt = open('years.txt','a')
    key = key.strip('"')
    years_txt.writelines(year+":"+key+"\n")
    years_txt.close()


def write_term(key,title_list,journal_list,author_list):
    term_txt = open('terms.txt','a')
    key = key.strip('"')
    if (len(title_list)>0):
        for item in title_list:
            content = "t-" + item + ':'+key+'\n'
            term_txt.writelines(content)
    if(len(journal_list)>0):
        for itme in journal_list:
            content = "o-" + itme +':'+key+'\n'
            term_txt.writelines(content)
    if(len(author_list)>0):
        for item in author_list:
            content = 'a-' +item+':'+key+'\n'
            term_txt.writelines(content)

    term_txt.close()


def initialize():
    try:
        os.remove('recs.txt')
        os.remove('years.txt')
        os.remove('terms.txt')
    except OSError:
        pass

def parsing():
    f = open( 'tem_file.txt' , 'r' )
    for line in f.readlines() :
        if find_between(line,"<article key=",">"):
            key = find_between(line,"<article key=",">")
            write_recs(key,line)
            year = get_date(line)
            write_year(year,key)
            title_list = get_title_term(line)
            journal_list = get_journal_term(line)
            author_list = get_author_term(line)
            write_term(key,title_list,journal_list,author_list)
            # print(key)
        if find_between(line,"<inproceedings key=",">"):
            key = find_between(line,"<inproceedings key=",">")
            write_recs(key,line)
            year = get_date(line)
            write_year(year,key)
            title_list = get_title_term(line)
            booktitle_list = get_booktitle_term(line)
            author_list = get_author_term(line)
            write_term(key,title_list,booktitle_list,author_list)
            # print(key)

    f.close() # not indented, this happens after the loop


if __name__ == "__main__":
    trimfile()
    initialize()
    parsing()
