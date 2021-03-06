from datetime import datetime, timedelta
from math import floor
from collections import OrderedDict
from matplotlib import pyplot as plt

def get_num_days(pay_freq):
    if pay_freq == "weekly":
        return 7
    elif pay_freq == "fortnightly":
        return 14

def calculate_deposits(bill, due_date, pay_date, pay_freq):

    pays_before_bill = 0
    test_date = pay_date

    # special case monthly because timedelta doesn't handle it
    if pay_freq == "monthly":
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
        while test_date < due_date:
            pays_before_bill = pays_before_bill + 1
            pay_period = get_num_days(pay_freq)
            test_date = test_date + timedelta(days=pay_period)

    if pays_before_bill == 0:
        return False
    else:
        deposit = bill/pays_before_bill

        if pay_freq in ["weekly", "fortnightly"]:
            for i in range(pays_before_bill):
                pay_date = pay_date + timedelta(days = (pay_period*i))
                pays_dict[pay_date] += deposit
        elif pay_freq == "monthly":
            print("TODO")
        return True

def calculate_savings (bill, due_date, debt_freq, pay_date, pay_freq):

    if pay_freq in ["weekly", "fortnightly"]:
        pay_period = get_num_days(pay_freq)
        next_pay_date = pay_date + timedelta(days=pay_period)

    bills_before_next_pay = 0

    while due_date < next_pay_date:
        bills_before_next_pay += 1
        if debt_freq in ["weekly", "fortnightly"]:
            bill_period = get_num_days(debt_freq)
            print("due_date: " + str(due_date))
            due_date = due_date + timedelta(days=bill_period)
        elif debt_freq == "monthly":
            print("TODO")

    print("next_pay_date: " + str(next_pay_date))

    if bills_before_next_pay > 0:
        deposit = bill * bills_before_next_pay
        pays_dict[pay_date] += deposit
        return bills_before_next_pay
    else:
        print("error")


def calc_reoccuring_cost (bill, due_date, debt_freq, pay_date, pay_freq):

    if pay_freq == "weekly":
        one_year = due_date + timedelta(days = 52*7)
    elif pay_freq == "fortnightly":
        one_year = due_date + timedelta(days = 26*14)
    elif pay_freq == "monthly":
        one_year = due_date + timedelta(years = 1)
    else:
        print("TODO")

    bill_futures = 0

    calculate_deposits (bill, due_date, pay_date, pay_freq)
    # TODO account for calculate_deposits first time through

    #debug
    one_year = due_date + timedelta(days = 12*7)

    while due_date <= one_year:

        # Find pay_date after bill is paid
        if pay_freq in ["weekly", "fortnightly"]:
            pay_period = get_num_days(pay_freq)
            pay_date = pay_date + timedelta(days=pay_period)
        # special case monthly because timedelta doesn't handle it
        elif pay_freq == "monthly":
            while pay_date <= due_date:
                test_month = int(pay_date.strftime("%m")) + 1
                # replace with mod
                if test_month == 13:
                    new_year = int(pay_date.strftime("%Y")) + 1
                    pay_date = pay_date.replace(month=1)
                    pay_date = pay_date.replace(year=new_year)
                else:
                    pay_date = pay_date.replace(month=test_month)

        if debt_freq in ["weekly", "fortnightly"]:
            debt_period = get_num_days(debt_freq)     
            due_date = due_date + timedelta(days=(debt_period + debt_period*bill_futures))
        # special case monthly because timedelta doesn't handle it
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
            # TODO replace with mod
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

        if calculate_deposits (bill, due_date, pay_date, pay_freq) == False:
            bill_futures = calculate_savings (bill, due_date, debt_freq, pay_date, pay_freq) - 1
        else:
            bill_futures = 0

#
# Test
#

next_pay_date = datetime(2017, 11, 3)
pay_freq = "fortnightly"

# initialize pay dates: deposits ammounts dict

pays_dict = {}

if pay_freq in ["weekly", "fortnightly"]:
    pay_period = get_num_days(pay_freq)
    pay_date = next_pay_date
    pays_dict[pay_date] = 0
    # arbitrarily big
    for i in range(99):
        pay_date = pay_date + timedelta(days = pay_period)
        pays_dict[pay_date] = 0
elif pay_freq == "monthly":
    print("TODO")

# Tests

fake_bill_1 = 50.00
fake_due_date_1 = datetime(2017, 11, 8)
fake_debt_freq_1 = "fortnightly"

fake_bill_2 = 821.00
fake_due_date_2 = datetime(2018, 1, 18)

fake_bill_3 = 68.00
fake_due_date_3 = datetime(2017, 11, 6)
fake_debt_freq_3 = "weekly"

fake_bill_4 = 3279.00
fake_due_date_4 = datetime(2018, 4, 6)

#calc_reoccuring_cost (fake_bill_1, fake_due_date_1, fake_debt_freq_1, next_pay_date, pay_freq)

#calculate_deposits(fake_bill_2, fake_due_date_2, next_pay_date, pay_freq)

calc_reoccuring_cost (fake_bill_3, fake_due_date_3, fake_debt_freq_3, next_pay_date, pay_freq)

#calculate_deposits(fake_bill_4, fake_due_date_4, next_pay_date, pay_freq)


# graphing

pays_dict = {key: value for key, value in pays_dict.items() if value != 0}

pays_dict = OrderedDict(sorted(pays_dict.items(), key=lambda x: x[0]))

for date, deposit in pays_dict.items():
    print(str(date) + ": " + str(round(deposit, 2)))

# lists = sorted(pays_dict.items())
# x, y = zip(*lists)
#
# plt.bar(x, y, 1, color="blue")
#
# fig = plt.gcf()
# plt.show()
