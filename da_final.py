#DataAnalysis2.py

import re
import pandas as pd
from collections import Counter



# Regular Expressions for fetching Account type , Account number, Balance
pattern1= re.compile(r'([A-Z][A-Z]-\w\w\w\w\w\w)')
pattern2= re.compile(r'((?i)A(/)?c( no(:|\.)?)? (x{3,8}( )?\d{3,15}|\d{15})|account \*{12}\d{4}|CREDIT CARD ENDING \d{3,8})')
pattern3= re.compile(r'((?i)(A(/)?c|Avl|Avail)( balance| bal)( - Rs.)?( in A/c x{3}\d{3}:( RS. ))?( INR | RS )?(.{1,5}\.\d{2,4})( CR)?)')

# function converting bank codes to names          
def converttoname(aT):
    words = ['HDFC','SBI','BOI','AXIS','ICICI','PNB','YES']
    for w in words:
        if w in aT:
           return w
    return "Not Available"




# Function to parse the file

def parse_file(filepath):
    
    with open(filepath, 'r') as file_object:
         line = file_object.readline()
         info_Lines=[]      #Contains all lines
         banks=[]      # to store all bank names for counting transactions
         
         while line:        
            at = re.findall(pattern1,line)
            an = re.findall(pattern2,line)
            bl = re.findall(pattern3,line)
            
            # cleaning account type
            ats = str(at).strip("[]'")   
            ats = str(converttoname(ats))  #convet type to name:
            
            # cleaning account number
            ans =str(an)[3:28].strip(" '/', '', '',")
            if ans:
                if "CARD" in ans:
                     ans = 'CC XXXX' + ans[-4:]
                else:
                     ans = 'AC XXXX-' + ans[-4:]
            else :
                 ans="Not Available"

            # cleaning account balance
            bls=str(bl)[3:43].strip(" '/', '', '',")
            if bls:
                 bls=str(bls).strip("', 'Avl', '', ' bal B A/c A/C")
                 #if 'CR' in bls:
                 bls=bls[bls.index('R'):]
            else:
                 bls='Not Available'
            
            # writes information to a list only if both account number and account type are available

            if ats != 'Not Available' and ans != 'Not Available':
                 info= ats + '#' + ans + '#' + bls
                 info_Lines.append(info)
            
            line=file_object.readline()
        
    #writing info_Lines into  text file
    with open('parsedfile.txt','w') as fo:
          fo.write('\n'.join(str(line) for line in info_Lines))
    
    

    print("##"*25 + "RAW_DATA" + "##"*25)
    for l in info_Lines:   #info_Lines contains all inormation in the format bank_name#acc.no#balance
        print(l)
    
    print("##"*30 + "_"*20 + "##"*30)
    

    #splitting by # and saving all bank names to get number of transactions
    print('\n')
    print("*"*25 + 'TRANSACTIONS' + "*"*25)
    print('\n')
    banks=[]
    for li in info_Lines:
        banks.append(str(list(li.split("#"))[0]))
    trs = dict(Counter(banks))
    
    print("BANK   Transactions")
    for key,value in trs.items():
        print("{}   : {}".format(key,value))
    



    print('\n')
    print("*"*25 + "BALANCE_INFO" + "*"*25)
    print('\n')
    #Storing information in a dictionary
    dicti={}
    for li in info_Lines:
         dicti[str(list(li.split("#"))[1])]=[str(list(li.split("#"))[0]),str(list(li.split("#"))[2])]  #key
    print("Acc.No         BANK    Balance")
    for key,value in dicti.items():
        print("{}   {}  {}".format(key,value[0],value[1]))
    

    #output Files

    #Writing balance_info into csv file using dataframe to save list to csv file
    df_1 = pd.DataFrame.from_dict(dicti,orient="index")
    df_1.to_csv('balanceinfo.csv', index=True, header=['Bank','Balance'])
       
    #Writing number of transactions into csv file using dataframe to save list to csv file
    df_2 = pd.DataFrame.from_dict(trs,orient="index")
    df_2.to_csv('transactions.csv', index=True, header=['Transactions'])


if __name__ == '__main__':
    filepath = 'DA-2.txt'
    parse_file(filepath)




