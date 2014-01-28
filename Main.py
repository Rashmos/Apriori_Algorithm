'''
Created on Nov 16, 2012

@author: rashmi
'''
import sys
import csv
import itertools
from sets import Set
import pickle
temp = {}

from collections import OrderedDict

rule = {}
database = []
conf_database = []
Candidates = []
candidate = OrderedDict()
large_itemset = OrderedDict()
L1 = OrderedDict()
intermediate_Large_Itemset = OrderedDict()
Pass = 1
min_supp = float(sys.argv[2]) # getting minimum support from Command Line
min_conf = float(sys.argv[3]) # getting minimum confidence from Command Line

# reading command line arguments and creating main database containing all transactions
def make_database():
    f_name = sys.argv[1]
    cr = csv.reader(open(f_name,"rb"))
    i = 0
    for row in cr:
        str0 = ' '.join(row)
        database.append(str0) 
        i = i + 1
    confidenceDatabase()

def confidenceDatabase():
    for d in database:
        in_between = d.split(" ")
        conf_database.append(tuple(in_between))
        
        
def generateRules(Item):
    one = 0.0
    two = 0.0
    both = 0.0
    rules = []
    global rule
    if " " in Item:
        rules = Item.split(" ")
        if len(rules) == 2:
            for d in conf_database:
                if rules[0] in d:
                    one = one + 1
                if rules[1] in d:
                    two = two + 1
                if rules[0] in d and rules[1] in d:
                    both = both + 1
            temp1 = float(both/one)
            temp2 = float(both/two)
            if temp1 >= min_conf:
                text = rules[0]+" -> "+rules[1]
                rule[text] = temp1
            if temp2 >= min_conf:
                text = str(rules[1]) +" -> "+ str(rules[0])
                rule[text] = temp2
        else:
            
            for d in conf_database:
                intermediate = Item.split(" ")
                #intermediate = ['pen','ink','diary','soap']
                subsets = set(itertools.combinations(intermediate,2))
                for s in subsets:
                    Str = []
                    for item in s:
                        Str.append(item)
                    single  = list(set(intermediate).difference(set(Str)))
                    count = 0.0
                    sing_count = 0.0
                    new_count = 0.0
                    if set(single).issubset(set(d)):
                        new_count = new_count + 1
                    if set(Str).issubset(set(d)):
                        count = count + 1.0
                    if set(Str).issubset(set(d)) and set(single).issubset(set(d)):
                        sing_count = sing_count + 1.0
                    for x in single:
                        text = s, "->", x
                        if not text in temp:
                            temp[text] = list()
                            temp[text].append(sing_count)
                            temp[text].append(count)
                        new_text = x," -> ",s
                        if not new_text in temp:
                            temp[new_text] = list()
                            temp[new_text].append(sing_count)
                            temp[new_text].append(new_count)
                        else:
                            temp[text][0] = temp[text][0] + sing_count
                            temp[text][1] = temp[text][1] + count
                            temp[new_text][0] = temp[new_text][0] + sing_count
                            temp[new_text][1] = temp[new_text][1] + new_count
            for answers in temp:
                conf_num = temp[answers][0]
                conf_den = temp[answers][1]
                if conf_den == 0.0:
                    conf = 0.0
                else:
                    conf = float(conf_num/conf_den)
                    if conf >= min_conf:
                        rule[answers] = conf
        
# Finding the large item sets -> with min_supp
        
def LargeItemsets(candidates):
    for item in candidates:
        num = float(candidates[item])
        den = len(database)
        if float(num/den) >= min_supp:
            intermediate_Large_Itemset[item] = float(num/den)
            large_itemset[item] = float(num/den)
            
            
    
  #  print "Large - Itemset-",large_itemset,"\n Intermediate Large - Itemset =", intermediate_Large_Itemset
     
        
# Creating Candidate Item sets        
    
def clacCandidateItemsets(iteration_no):
    print "Generating "+str(iteration_no)+"-itemset Frequent Pattern"
    if iteration_no == 1:
        for d in database:
            temp = d.split(" ")
            for item in temp:
                if not item in candidate:
                    count  = temp.count(item)
                    candidate[item] = count
                else:
                    count_prev = candidate[item]
                    count = temp.count(item) + count_prev
                    candidate[item] = count
    else:
        i = 0
        while i < len (Candidates):
            candidate[Candidates[i]] = 0
            for d in database:
                temp = d.split(" ")
                temp_candidates = Candidates[i].split(" ")
                x = 0
                count = 0
                while x < len(temp_candidates):
                    if temp_candidates[x] in temp:
                        count = count + 1
                    x = x + 1
                if len (temp_candidates) == count :
                    if Candidates[i] in candidate:
                        count_prev = candidate.get(Candidates[i])
                        candidate[Candidates[i]] = int(count_prev) + 1
                    else:
                        candidate[Candidates[i]] = 1
            i = i + 1
                     
                
   # print "Candidate",candidate
  
    
def apriori():
    k = 2 
    L_prev = large_itemset
    candidate.clear()
    
    while not L_prev == []:
        aprioriGen(L_prev,k)
        if k>2:
            prune(L_prev,k)
        clacCandidateItemsets(k)
        intermediate_Large_Itemset.clear()
        LargeItemsets(candidate)
        L_prev = intermediate_Large_Itemset.keys()
        
        k = k + 1
        #del Candidates[:]
        candidate.clear()
        
        #print L_prev
        
        
def aprioriGen(Prev,n):
    TempCandidates = []
    if n == 2:
        i = 0
        
        items = Prev.keys()
        while i < len(items):
            str1 = items[i]
            j = i +1
            while j < len(items):
                str2 = items[j]
                new_str = str1+" "+str2
                TempCandidates.append(new_str)
                j = j + 1
            i = i + 1
            
    else:
        
        i = 0
        y = len(Prev)
        while i < y:
            j = i + 1
            while j < y:
                temp1 = Prev[i].split(" ")
                temp2 = Prev[j].split(" ")
                x = 0
                first = ''
                second = ''
                while x < n-2:
                    if temp1[x] == temp2[x]:
                        first = temp1[x]+" "
                        second = temp2[x]+" "
                    x = x + 1
                if first == second and first != '' and second != '':
                    #temp = " ".join(temp2[:z])
                    #temp = str(temp2[:z])
                    
                    final = " ".join(temp1) + " " + temp2[-1]
                    if not final in TempCandidates:
                        TempCandidates.append(final)
                j = j + 1
            i = i + 1
    a = 0
    
    global Candidates
    Candidates = []
    for text in TempCandidates:
        Candidates.append(text)
        a = a + 1
    TempCandidates = []
    
    
def prune(prev,k):
    n = k - 1 
    item = prev
    global Candidates
    for can in Candidates:
        count  = 0
        intermediate = can.split(" ")
        subsets = set(itertools.combinations(intermediate,n))
        for s in subsets:
            str = " ".join(s)
            if str in item:
                count = count + 1
        if count != len(subsets):
            Candidates.remove(can)
    
        
        '''
        can = can.replace(" ",'')
        subsets = set(itertools.combinations_with_replacement(can , n))
        common = subsets.intersection(set(prev))
        not_common = list(subsets - common)
        if not_common != []:
            Candidates.remove(can)
        '''
def writeLargeItemsets():
    var = raw_input("Enter the filename where you want to save the Large Itemset file: ")
    var = var+".txt"
    fo = open(var,"w")
    fo.write("==Large itemsets "+ str(min_supp) +"\n")
    fo.write("\n")
    for key in large_itemset:
        fo.write(key+"      "+str(large_itemset[key])+"\n")
    fo.write("\n")
    fo.write("\n")
    fo.write("\n")
    fo.write("==High-confidence association rules "+str(min_conf)+" \n")
    fo.write("\n")
    for value in rule:  
        fo.write(str(value)+"      "+str(rule[value])+"\n")
    
    fo.close
        
 
        
make_database() 

clacCandidateItemsets(Pass)
if Pass == 1:
    L1 = candidate
Pass = Pass + 1
LargeItemsets(candidate)
apriori()
#print large_itemset
for item in large_itemset:
    generateRules(item)
writeLargeItemsets()

#displayRules()


    
    
    


   
    
        
    
