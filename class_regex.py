import csv
import re

class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def set_banks(self,banks):
        self.bank_dict={}
        for bank in banks:
            self.bank_dict[bank]={}
            self.bank_dict[bank]["Balance"]=0
            self.bank_dict[bank]["total_transaction"]=0
            self.bank_dict[bank]["credit_spent"] = 0
            self.bank_dict[bank]["credit_returned"] = 0
            self.bank_dict[bank]["cc_balance"] = 0

    def deposit_or_credited(self,bank_name,amount):
        self.bank_dict[bank_name]["Balance"] += amount

    def withdrawal_or_debited(self,bank_name,amount):
        self.bank_dict[bank_name]["Balance"] -= amount

    def debitcard_transaction(self,bank,amount):
        self.bank_dict[bank]["Balance"]-= amount
        self.bank_dict[bank]["total_transaction"]+= amount

    def creditcard_transaction(self,bank,amount):
        self.bank_dict[bank]["credit_spent"]+= amount

    def creditcard_payback(self,bank,amount):
        self.bank_dict[bank]["credit_due"]=amount

def yesbank_transfer(msg):
    pattern = re.compile(r'Dear ([a-z]+), Transfer of  Rs.([0-9]+) to [0-9]+ [\w ]+ [\w]+ with REF No:[A-Za-z0-9]+.Fees\s[(](\w)+\s\w\w\s\w\w[)]: Rs\.([0-9]+)')
    matches = pattern.finditer(msg)
    for match in matches:
        credited = float(match.group(2))
        tax = float(match.group(3))
        return (credited-tax)
    return 0

def sbi_debited(msg):
    pattern = re.compile(r'Your AC \w+ Debited \w+ ([0-9.]+) on [0-9/]+ [A-za-z-. ]+([0-9.,]+)')
    matches = pattern.finditer(msg)
    for match in matches:
        debited = match.group(1)
        debited=float(debited)
        bal = match.group(2)
        bal = bal.rstrip(".")
        bal=float("".join(bal.split(",")))
        return debited,bal
    return 0,0
def sbi_debit(msg):
    pattern = re.compile(r'Your [a-zA-Z0-9/ ]{46}([0-9.]+)[a-zA-Z0-9/ ]+[a-zA-Z .]+([0-9,.]+)')
    matches = pattern.finditer(msg)
    for match in matches:
        debit = match.group(1)
        debit = float(debit.rstrip("."))
        bal = match.group(2)
        bal = bal.rstrip(".")
        bal = float("".join(bal.split(",")))
        return (debit,bal)
    return 0,0
def sbi_credit(msg):
    pattern = re.compile(r'[0-9]{1,2}[/][0-9]{1,2}[/][0-9]{4}[0-9,: ]+[\n]?[a-zA-Z/0-9: ]+[. ]+([0-9.]+) CR')
    matches = pattern.finditer(msg)
    for match in matches:
        credit_bal = float(match.group(1))
        return (credit_bal)
    return 0
def sbibank(msg):
    pattern = re.compile(r'[\w\s]+SBI Debit Card \w+ [a-zA-Z]{3} a [a-zA-Z]{8} [a-zA-Z]{5} [A-Za-z]{2}([0-9.]{2,5})')

    matches = pattern.finditer(msg)
    for match in matches:
        purchase = float(match.group(1))
        return purchase
    return 0

def sbi_withdrawn(msg):
    pattern = re.compile(r'Rs ([0-9]+) [\w ,/.]+#[0-9 .Avl]+ [A-Za-z ]+([0-9.]+)')
    matches = pattern.finditer(msg)
    for match in matches:
        withdrawn = float(match.group(1))
        bal = match.group(2)
        bal=float(bal.rstrip("."))

        return withdrawn,bal
    return 0,0

def sbi_credited(msg):
    pattern = re.compile(r'Your [A-Z/]+ [A-Z0-9 ]{24} ([0-9,.]+)[a-zA-Z0-9 /-]+[a-zA-Z./ ]+([0-9.,]+)')
    matches = pattern.finditer(msg)
    for match in matches:
        credited = match.group(1)
        credited = credited.rstrip(".")
        credited=float("".join(credited.split(",")))
        bal = match.group(2)
        bal=bal.rstrip(".")
        bal=float("".join(bal.split(",")))
        print(credited, bal)
        return (credited,bal)
    return 0,0

def hdfc_credit_card_credited(msg):
    pattern = re.compile(r'Dear [A-Za-z ,.]+([0-9.,]+) R') #CARDMEMBER
    matches = pattern.finditer(msg)
    for match in matches:
        recieved = match.group(1)
        recieved = recieved.rstrip(".")
        recieved = float("".join(recieved.split(",")))

        return recieved
    return 0

def hdfc_credit_card_spent(msg):
    pattern = re.compile(r'Rs.[0-9.]+ was spent [a-zA-Z ]+ HDFCBank CREDIT[a-zA-Z0-9 :-]+[a-zA-Z. -]+([0-9. ]+)')
    matches = pattern.finditer(msg)
    for match in matches:
        spent = match.group(1)
        bal = match.group(2)
        spent=float(spent)
        bal=float(bal)
        return spent,bal
    return 0,0

def hdfc_credit_card_otp(msg):
    pattern = re.compile(r'OTP is [0-9]{6}[a-zA-Z ]+([0-9.]+)')
    matches = pattern.finditer(msg)
    for match in matches:
        spent = match.group(1)
        spent = spent.rstrip(".")
        spent = float("".join(spent.split(",")))

        return spent
    return 0

def hdfc_credit_card_due(msg):
    pattern = re.compile(r'Dear Customer[,][a-zA-Z .]+([0-9.]+) is')
    matches = pattern.finditer(msg)
    for match in matches:
        dues = float(match.group(1))

        return dues
    return 0
def hdfc_cc_stmt_dues(msg):
    pattern = re.compile(r'Stmt for HDFCBank [a-zA-Z.0-9 ]{47}([0-9]+)')
    matches = pattern.finditer(msg)
    for match in matches:
        dues = float(match.group(1))
        return dues
    return 0
def hdfc_neft(msg):
    pattern = re.compile(r'NEFT Transaction[a-zA-Z0-9 ]{48}(0-9,.)+')
    matches = pattern.finditer(msg)
    for match in matches:
        added = (match.group(0))
        print(added)
        added = added.rstrip(".")
        added = float("".join(added.split(",")))
        print(added)
        return added

def resp_bank_name(number):
    if(number):
        for i in range(len(number)):
            if(number[i:i+3]=="YES"):
                return "YES"
            elif(number[i:i+3]=="SBI"):
                return "SBI"
            elif (number[i:i + 4] == "HDFC"):
                return "HDFC"

with open ("csvdata.csv","r") as csv_file:
    global bank_user
    csv_reader=csv.DictReader(csv_file)
    user_id_set = set()
    bank_user = {}
    for line in csv_reader:
        print(line)
        user_id_set.add(line["user_id"])
    for id in user_id_set:
        bank_user[id]= User(id)

    for id in user_id_set:
        csv_file.seek(0)
        bank_setlist=set()
        for line in csv_reader:
            if(line['user_id']==id) :
                if(line["number"]):
                    name=resp_bank_name(line["number"])
                if(name!=None):
                    bank_setlist.add(name)

            bank_user[id].set_banks(bank_setlist)

    def yes_func(sms):
        for i in range(len(sms)):
            if(sms[-1-i:-1-i+4]=="Rs."):
                credited_money = yesbank_transfer(sms)
                return credited_money
            else:
                return 0

    def sbi_func(sms,id,name):
        # print(len(sms))
        for i in range(len(sms)):
            if(sms[0:0+7]=="Your AC"):
                debited,bal = sbi_debited(sms)
                if(debited!=0 and bal!=0):
                    bank_user[id].withdrawal_or_debited(name, debited)
                    bank_user[id].bank_dict[name]["Balance"] = bal
            elif(sms[0:0+8]=="Your A/C"):
                debit, bal = sbi_debit(sms)
                if(debit!=0 and bal!=0):
                    bank_user[id].withdrawal_or_debited(name, debit)
                    bank_user[id].bank_dict[name]["Balance"] = bal
            elif(sms[-2:]=="CR"):
                credit_bal = sbi_credit(sms)
                if(credit_bal!=0):
                    bank_user[id].deposit_or_credited(name, credit_bal)
            elif(sms[i:i+8]=="Credited"):
                credited,bal=sbi_credited(sms)
                if(credited!=0 and bal!=0):
                    bank_user[id].deposit_or_credited(name,credited)
                    bank_user[id].bank_dict[name]["Balance"] = bal
            elif(sms[i:i+10]=="Thank you"):
                purchase=sbibank(sms)
                if (purchase != 0):
                    bank_user[id].debitcard_transaction(name,purchase)
            elif(sms[0:0+2]=="Rs"):
                withdrew,bal=sbi_withdrawn(sms)
                if (withdrew != 0 and bal!=0):
                    bank_user[id].withdrawal_or_debited(name,withdrew)
                    bank_user[id].bank_dict[name]["Balance"] = bal
            else:
                pass

    def hdfc_func(sms,id,name):
        for i in range(len(sms)):
            if(sms[i:i+7]=="CARDMEMBER"):
                received = hdfc_credit_card_credited(sms)
                if(received!=0):
                    bank_user[id].creditcard_payback(name,received)

            elif(sms[i:i+4]=="Stmt"):
                dues=hdfc_cc_stmt_dues(sms)
                if (dues != 0):
                    bank_user[id].bank_dict[name]["credit_due"]=dues

            elif(sms[i:9]=="spent on"):
                spent,bal= hdfc_credit_card_spent(sms)
                if(spent!=0 and bal !=0):
                    bank_user[id].creditcard_transaction(name,spent)
                    bank_user[id].bank_dict[name]["cc_balance"] = bal

            elif(sms[i:4]=="Greetings"):
                dues=hdfc_credit_card_due(sms)
                if (dues!= 0):
                    bank_user[id].bank_dict[bank]["credit_due"] = dues

            elif(sms[i:7]=="OTP is"):
                spent= hdfc_credit_card_otp(sms)
                if (spent != 0):
                    bank_user[id].creditcard_transaction(name,spent)
            elif(sms[0:4]=="NEFT"):
                bal=hdfc_neft(sms)
                bank_user[id].bank_dict["Balance"] = bal

    for id in user_id_set:
        csv_file.seek(0)
        for line in csv_reader:
            if(line['user_id']==id ) :
                if(line["number"] and line["body"]):
                    name=resp_bank_name(line["number"])
                    if(name=="YES"):
                        deposit = yes_func(line["body"])
                        bank_user[id].deposit_or_credited(name,deposit)

                    elif(name=="SBI"):
                        sbi_func(line["body"],id,name)
                    elif(name=="HDFC"):
                        hdfc_func(line["body"],id,name)




while (1):
    print("Select the User_name from the options below: ")
    print("1) 70006\n2) 70007 \n3) 70009\n4) 70010")
    choice = int(input("Enter your choice: "))
    if (choice == 1):
        print(bank_user["70006"].bank_dict)

    elif (choice == 2):
        print(bank_user["70007"].bank_dict)

    elif (choice == 3):
        print(bank_user["70009"].bank_dict)

    elif (choice == 4):
        print(bank_user["70006"].bank_dict)

    else:
        print("Invalid option.")
        continue
