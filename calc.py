from datetime import datetime, timedelta
from math import floor
from collections import OrderedDict

def calculate_deposit(bill, due_date, next_pay_date, pay_freq):

    if pay_freq == "weekly":
        pay_period = 7
    elif pay_freq == "fortnightly":
        pay_period = 14

    pays_before_bill = 0

    # special case monthly because timedelta doesn't handle it
    if pay_freq == "monthly":
        test_date = next_pay_date

        while test_date <= due_date:
            test_month = test_date.strftime("%m")
            new_test_month = int(test_month) + 1

            if new_test_month == 13:
                test_year= test_date.strftime("%Y")
                new_test_year = int(test_year) + 1
                test_date = test_date.replace(month=1)
                test_date = test_date.replace(year=new_test_year)
                pays_before_bill += 1
            else:
                test_date = test_date.replace(month=new_test_month)
                pays_before_bill += 1

    else:
        # weekly and fortnightly
        test_date = next_pay_date
        while test_date < due_date:
            pays_before_bill = pays_before_bill + 1
            test_date = test_date + timedelta(days = pay_period)
        
    if pays_before_bill == 0:
        deposit_rounded = 0
        print("here")
    else:
        deposit = bill/pays_before_bill
        deposit_rounded = round(deposit, 2)
        print("there")

    if pay_freq in ["weekly", "fortnightly"]:
        for i in range(pays_before_bill):
            pay_date = next_pay_date + timedelta(days = (pay_period*i))
            pays_dict[pay_date] += deposit_rounded
    elif pay_freq == "monthly":
        # TODO
        print("TODO")

    return deposit_rounded

def calc_reoccuring_cost (bill, due_date, debt_freq, next_pay_date, pay_freq):
    # debt_freq = "weekly", "fortnightly", "monthly", "quarterly", "biannually", "annually"
    # pay_freq = "weekly", "fortnightly", "monthly"

    if pay_freq == "weekly":
        due_date_1_year = due_date + timedelta(days = 52*7)
    elif pay_freq == "fortnightly":
        due_date_1_year = due_date + timedelta(days = 26*14)
    elif pay_freq == "monthly":
        due_date_1_year = due_date + timedelta(days = 365)
    else:
        print("TODO")

    deposit = calculate_deposit (bill, due_date, next_pay_date, pay_freq)

    while due_date <= due_date_1_year:

        # Find next_pay_date after bill is paid
        if pay_freq in ["weekly", "fortnightly"]:
            if pay_freq == "weekly":
                pay_period = 7
            elif pay_freq == "fortnightly":
                pay_period = 14
            next_pay_date = next_pay_date + timedelta(days=pay_period)

        # special case monthly because timedelta doesn't handle it
        if pay_freq == "monthly":
            while next_pay_date <= due_date:
                test_month = next_pay_date.strftime("%m")
                new_test_month = int(test_month) + 1

                if new_test_month == 13:
                    new_year = int(next_pay_date.strftime("%Y")) + 1
                    next_pay_date = next_pay_date.replace(month=1)
                    next_pay_date = next_pay_date.replace(year=new_year)
                else:
                    next_pay_date = next_pay_date.replace(month=new_test_month)

        if debt_freq == "weekly":
            due_date = due_date + timedelta(days=7)
        elif debt_freq == "fortnightly":
            due_date = due_date + timedelta(days=14)
        elif debt_freq == "monthly":
            test_month = int(due_date.strftime("%m")) + 1
            # replace with mod
            if test_month == 13:
                new_year = int(due_date.strftime("%Y")) + 1
                due_date = due_date.replace(month=1)
                due_date = due_date.replace(year=new_year)
            else:
                due_date = due_date.replace(month=test_month)
        elif debt_freq == "quarterly":
            test_month = int(due_date.strftime("%m")) + 3
            # replace with mod
            if test_month in [13, 14, 15]:
                new_month = test_month - 12
                new_year = int(due_date.strftime("%Y")) + 1
                due_date = due_date.replace(month=new_month)
                due_date = due_date.replace(year=new_year)
            else:
                due_date = due_date.replace(month=test_month)
        elif debt_freq == "biannually":
            test_month = int(due_date.strftime("%m")) + 6
            # replace with mod
            if test_month in [13, 14, 15, 16, 17, 18]:
                new_month = test_month - 12
                new_year = int(due_date.strftime("%Y")) + 1
                due_date = due_date.replace(month=new_month)
                due_date = due_date.replace(year=new_year)
            else:
                due_date = due_date.replace(month=test_month)
        elif debt_freq == "annually":
            due_date = due_date + timedelta(years=1)

        calculate_deposit (bill, due_date, next_pay_date, pay_freq)

#
# Test
#

fake_due_date = datetime(2017, 11, 8)
fake_next_pay_date = datetime(2017, 11, 3)
fake_pay_freq = "fortnightly"
fake_bill = 50.00
fake_debt_freq = "fortnightly"

pay_freq = fake_pay_freq
next_pay_date = fake_next_pay_date

pays_dict = {}

if pay_freq == "weekly":
    pay_period = 7
elif pay_freq == "fortnightly":
    pay_period = 14

if pay_freq in ["weekly", "fortnightly"]:
    pay_date = next_pay_date
    pays_dict[pay_date] = 0
    for i in range(50):
        pay_date = pay_date + timedelta(days = pay_period)
        pays_dict[pay_date] = 0
elif pay_freq == "monthly":
    # TODO
    print("TODO")

calc_reoccuring_cost (fake_bill, fake_due_date, fake_debt_freq, next_pay_date, pay_freq)

pays_dict = OrderedDict(sorted(pays_dict.items(), key=lambda x: x[0]))

for date, deposit in pays_dict.iteritems():
    print(str(date) + ": " + str(deposit))