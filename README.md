# Information-Retrieval-System-Using-the-Berkeley-DB-library-for-operating-on-files-and-indices

Implementation in python and used a bit of Bash commands

# Motivation

I did it as an assignment in University

# Group break down
phase3.py and Script (which has a few bash commands) -> Aman Anand (myself)
parser_xml.py -> Zhihao Zhang
print_full_record.py -> Adit Hasan

# Running the program
From command line
1) python3 parser_xml.py
  Creates 3 files terms.txt, years.txt, recs.txt
2) bash Script
  Creates 3 indices te.idx, ye.idx, re.idx
3) python3 phase3.py
  Command line interface for user to run queries and retrieve data corresponding to the queries
  
# Grammer for the queries
alphanumeric    ::= [0-9a-zA-Z_]
numeric		::= [0-9]
year            ::= numeric
yearPrefix      ::= 'year' ':' | 'year' '>' | 'year' '<'
yearQuery       ::= yearPrefix year
termPrefix      ::= ('title' | 'author' | 'other') ':'
term            ::= alphanumeric
termQuery       ::= termPrefix? term 
phrase		::= term (whitespace term)*
phraseQuery	::= termPrefix? '"' phrase '"'
expression      ::= yearQuery | termQuery | phraseQuery
query           ::= expression (whitespace expression)*
