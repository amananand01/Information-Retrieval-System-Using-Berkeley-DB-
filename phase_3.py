# AMAN ANAND
from bsddb3 import db
from parser_xml import *
from print_full_record import *
import sys
import re

'''
Arguments: String , First Index of string to be matched, Last index of string
Returns: substring between the given indices
'''
def get_string(string,first,last):
    try:
        start=string.index(first)+len(first)
        end=string.index(last,start)
        return string[start:end]
    except ValueError:
        return False

'''
Arguments: Term, Phrase Matched, Records_keys matched
Returns: set() of keys for which phrase matches the term
'''
def Matched_phrase(term,phrase,records_matched):
    result_keys=set()

    database = db.DB()
    database.open("re.idx")
    curs = database.cursor()

    for each in records_matched:
        iter = curs.set(each.encode("utf-8"))
        while(iter):
            if term=="title":
                string=get_string(str(iter[1].decode("utf-8")),"<title>","</title>")
            elif term=="author":
                string=get_author_term(str(iter[1].decode("utf-8")))
                string=" ".join(string)
            elif term=="other":
                string_journal=get_string(str(iter[1].decode("utf-8")),"<journal>","</journal>")
                string_book_title=get_string(str(iter[1].decode("utf-8")),"<booktitle>","</booktitle>")
                if string_journal and string_book_title:
                    string=string_journal+string_book_title
                elif string_journal:
                    string=string_journal
                else:
                    string=string_book_title

            if string is False: break

            if phrase.lower() in string.lower():
                result_keys=result_keys.add(each)
            break

    curs.close()
    database.close()
    return result_keys

'''
Argument: each -> parsed input one substring at a time
Returns: set() of keys matched with the input
'''
def terms(each):

    result_keys=set()

    database = db.DB()
    database.open("te.idx")
    curs = database.cursor()

    if each[0] in ["title","author","other"]:

        if each[0]=="title": find="t-"
        elif each[0]=="author": find="a-"
        else : find="o-"
        find=find+each[1].lower()

        iter = curs.set(find.encode("utf-8"))
        while(iter):
            result_keys.add(str(iter[1].decode("utf-8")))
            #iterating through duplicates
            dup = curs.next_dup()
            while(dup!=None):
                result_keys.add(str(dup[1].decode("utf-8")))
                dup = curs.next_dup()
            break

    elif each[0]=="term":
        term=["a-","o-","t-"]
        for every in term:
            find=every+each[1].lower()
            iter = curs.set(find.encode("utf-8"))
            while(iter):
                result_keys.add(str(iter[1].decode("utf-8")))
                dup = curs.next_dup()
                while(dup!=None):
                    result_keys.add(str(dup[1].decode("utf-8")))
                    dup = curs.next_dup()
                break

    curs.close()
    database.close()
    return result_keys

'''
Arguments: lower_range match , upper_range match, exact year match
Returns: set() of keys which come in the range of the input provided
'''
def years(lower_range,higher_range,year):
    result_keys=set()

    database = db.DB()
    database.open("ye.idx")
    curs = database.cursor()

    if lower_range=='' and higher_range=='':
        iter = curs.set(year.encode("utf-8"))
        while(iter):
            result_keys.add(str(iter[1].decode("utf-8")))
            #iterating through duplicates
            dup = curs.next_dup()
            while(dup!=None):
                result_keys.add(str(dup[1].decode("utf-8")))
                dup = curs.next_dup()
            break
    else:
        iter = curs.set_range(str(higher_range).encode("utf-8"))
        while(iter):
            if(int(iter[0].decode("utf-8"))>=lower_range):
                break
            # print(iter)
            result_keys.add(str(iter[1].decode("utf-8")))
            #iterating through duplicates
            dup = curs.next_dup()
            while(dup!=None):
                result_keys.add(str(dup[1].decode("utf-8")))
                dup = curs.next_dup()
            iter = curs.next()


    curs.close()
    database.close()
    return result_keys

'''
Argumetns: inp -> input from user, output-> output format

Main function of the program:
Parses all the input and prints the keys matched by calling specific functions
'''
def Main_Function(inp,output):
    # Declare variables
    check_term=[]
    term_data=set()
    year_data=set()
    check_query=False
    year_flag=False

    flag_eq=set()
    flag_less_than=set() # for less than symbol
    flag_greater_than=set() # for greater than symbol

    lower_range=float('inf')
    higher_range=float('-inf')

    # chceck if the input only has output=key/full
    if "output=key"==inp:
        output="key"
        return output
    elif "output=full"==inp:
        output="full"
        return output

    # chceck if the input has queries with output=key/full then remove it
    if inp.split()[0]=="output=key" or inp.split()[0]=="output=full":
        if inp.split()[0]=="output=key": output="key"
        else: output="full"
        inp=inp.lstrip("output=key")
        inp=inp.lstrip("output=full")
        inp=inp[1:]


    elif inp.split()[-1]=="output=key" or inp.split()[-1]=="output=full":
        if inp.split()[-1]=="output=key": output="key"
        else: output="full"
        inp=inp.rstrip("output=full")
        inp=inp.rstrip("output=key")
        inp=inp[0:-1]

    # Match a phrase Query 8
    pattern_phrase="[title: | author: | other:]+\"+[\w+\s]+\""
    match_phrase=re.compile(pattern_phrase)
    try: # will catch the wrong input from user
        if match_phrase.match(inp):
            # print("Matched phrase-> ",match_phrase.match(inp).group())
            term=inp.split(":")[0]
            for each in inp.split(":")[1][1:-1].split():
                check_term.append( [ term,each ] )

            term_data=terms(check_term[0])
            for each in check_term[1:]:
                term_data=term_data.intersection(terms(each))

            RESULT=term_data

            if len(RESULT)>0:
                RESULT=Matched_phrase(term,inp.split(":")[1][1:-1],RESULT)
            else:
                return output

            if len(RESULT)==0:
                print("\nNothing Matched")
                return output

            if output=="full":
                PrintFullRecords(RESULT)
            else:
                for each in RESULT:
                    print(each)

            return output
    except: pass

    inp=inp.split(" ")

    for each in inp:

        # Query 1,2,4
        pattern_term="[title | author | other]+:+[\w]+$"
        match_term=re.compile(pattern_term)
        if match_term.match(each):
            check_term.append( [ each.split(":")[0],each.split(":")[1] ] )
            # print("Matched term-> ",match_term.match(each).group())
            check_query=True

        # Query 3
        pattern_year_eq="year+:+[0-9]+$"
        match_year_eq=re.compile(pattern_year_eq)
        if match_year_eq.match(each):
            # print("Matched year-> ",match_year_eq.match(each).group())
            check_query=True
            year_flag=True
            flag_eq.add(each.split(":")[1])

        # Query 6
        pattern_year_range="year+[< | >]+[0-9]+$"
        match_year_range=re.compile(pattern_year_range)
        if match_year_range.match(each):
            year_flag=True
            # print("Matched year range-> ",match_year_range.match(each).group())
            check_query=True

            if ">" in each.split("year")[1]:
                flag_greater_than.add(int(each.split("year")[1][1:]))
            elif "<" in each.split("year")[1]:
                flag_less_than.add(int(each.split("year")[1][1:]))

            if len(flag_less_than)>0:
                lower_range=min(flag_less_than)
            if len(flag_greater_than)>0:
                higher_range=max(flag_greater_than)

        # Query 5
        pattern_any_term="\w+$"
        match_any_term=re.compile(pattern_any_term)
        if match_any_term.match(each):
            check_term.append( [ "term",each ] )
            # print("Matched any term-> ",match_any_term.match(each).group())
            check_query=True

    if year_flag:
        if len(flag_eq)==0 or len(flag_eq)==1:
            if len(flag_eq)==1:
                year=int(flag_eq.pop())
                if year>float(higher_range) and year<float(lower_range):
                    year_data=years('','',str(year))

            elif not lower_range=="inf" and not higher_range=="inf" :# no year eq
                year_data=years(float(lower_range),float(higher_range),'')

    if len(check_term)>0:
        term_data=terms(check_term[0])
        for each in check_term[1:]:
            term_data=term_data.intersection(terms(each))

    if len(term_data)>0 and year_flag==True:
        RESULT=term_data.intersection(year_data)
    else:
        if len(year_data)>0:
            RESULT=year_data
        else:
            RESULT=term_data

    if len(RESULT)==0:
        print("\nNothing Matched")
        return output

    if output=="full":
        PrintFullRecords(RESULT)
    else:
        for each in RESULT:
            print(each)

    return output

'''
main()
checks if the input needs to be read from a file or command line
'''
def main():

    display = '''\nSelect "y" to exit the program \n
Enter the Query or select one of the above options\n'''

    output="key"

    if sys.argv[1:]:
        with open(sys.argv[1:][0]) as file:
            for each_line in file.readlines():
                output=Main_Function(each_line[:-1],output)
    else:
        while (True):
            inp=input(display)
            if inp=='':
                continue
            if inp=="y": break
            output=Main_Function(inp,output)

    return

if __name__ == "__main__":
	main()
