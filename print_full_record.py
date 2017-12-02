from bsddb3 import db
import re

def PrintOutput(author_list, title, page, year, booktitle, journal):
    print("*******")
    if (len(author_list)>0):
        print("Author: " + ", ".join(author_list) + '\n')
    if (title):
        print("Title: " + title +'\n')
    if (page):
        print("Page: " + page + '\n')
    if (year):
        print("Year: " + year + '\n')
    if(booktitle):
        print("BookTitle: "+booktitle+ '\n')
    if(journal):
        print("Journal: "+journal+ '\n')


def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return False

def get_author_term(line):
    author_list= list()
    while (True):
        context_author = find_between(line,"<author>","</author>")
        if context_author == False:
            break
        context_author
        author_list.append(context_author)
        text_term = "<author>" + context_author + "</author>"
        line= line.replace(text_term,'')
    return author_list

def ParsePrint(line):
    if find_between(line,"<article key=",">"):
        key = find_between(line,"<article key=",">")
        key = "<article key="+key+">"

    if find_between(line,"<inproceedings key=",">"):
        key = find_between(line,"<inproceedings key=",">")
        key = "<inproceedings key="+key+">"

    line = line.replace(key,"")
    author_list = get_author_term(line)
    title = find_between(line,"<title>","</title>")
    page = find_between(line,"<pages>","</pages>")
    year = find_between(line,"<year>","</year>")
    journal = find_between(line,"<journal>","</journal>")
    booktitle = find_between(line,"<booktitle>","</booktitle>")
    PrintOutput(author_list,title, page, year, booktitle, journal)

def PrintFullRecords(KeySet):

    if len(KeySet)==0:
        print("No such entry found in the database")
        return

    DB_File = "re.idx"
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(DB_File,None, db.DB_HASH, db.DB_CREATE)
    cursor = database.cursor()
    KeySet = sorted(KeySet)
    for currentkey in KeySet:

        result = cursor.set(currentkey.encode("utf-8"))

        if (result != None):
            print("Records matching the key: " + currentkey )
            ParsePrint(result[1].decode("utf-8"))
            #print("")

            duplicate = cursor.next_dup()

            while (duplicate != None):
                ParsePrint(duplicate[1].decode("utf-8"))
                duplicate = cursor.next_dup()
        else:
            print("No such entry found in the database: " + currentkey)

    cursor.close()
    database.close()
if __name__ == "__main__":
    KeySet = set(["conf/icdim/WazanLBB08", "journals/cii/ElghazelBGHMZ15", "conf/setn/PothitosKS12", "Adit Hasan"])
    PrintFullRecords(KeySet)
