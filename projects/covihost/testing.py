import ast
import covihost_csv as covihost_csv

listy = covihost_csv.read_csv('projects/covihost/testing3.csv')

"""
for each in listy:
    for things in each:
        #print("Key {key}, value of type {value}".format(key=things, value=type(each[things])))
        if things == "creators":
            print(type(each[things]))
            each[things] = ast.literal_eval(each[things])
            print(type(each[things]))
        
        if things == "upload_type":
            print(type(each[things]))
            each[things] = ast.literal_eval(each[things])
            print(type(each[things]))
"""

disposable_keywords = ['{\textless}Has Supplementary Material{\textgreater}',
        '{\textless}Closed Access{\textgreater}',
        '{\textless}Has Two Versions{\textgreater}',
        '{\textless}Scanned Paper{\textgreater}',
        ]