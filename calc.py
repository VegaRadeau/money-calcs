from datetime import datetime, timedelta
from math import floor
from collections import OrderedDict
from matplotlib import pyplot as plt

def get_pay_period(pay_freq):
    if pay_freq == "weekly":
        return 7
    elif pay_freq == "fortnightly":
        return 14

def calculate_deposits(bill, due_date, next_pay_date, pay_freq):

    pays_before_bill = 0
    test_date = next_pay_date

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
            pay_period = get_pay_period(pay_freq)
            test_date = test_date + timedelta(days = pay_period)

    if pays_before_bill == 0:
        return False
    else:
        deposit = bill/pays_before_bill

        if pay_freq in ["weekly", "fortnightly"]:
            for i in range(pays_before_bill):
                pay_date = next_pay_date + timedelta(days = (pay_period*i))
                pays_dict[pay_date] += deposit
        elif pay_freq == "monthly":
            # TODO
            print("TODO")
        return True

def calc_reoccuring_cost (bill, due_date, debt_freq, next_pay_date, pay_freq):

    if pay_freq == "weekly":
        due_date_1_year = due_date + timedelta(days = 52*7)
    elif pay_freq == "fortnightly":
        due_date_1_year = due_date + timedelta(days = 26*14)
    elif pay_freq == "monthly":
        due_date_1_year = due_date + timedelta(days = 365)
    else:
        print("TODO")

    deposit = calculate_deposits (bill, due_date, next_pay_date, pay_freq)

    while due_date <= due_date_1_year:

        # Find next_pay_date after bill is paid
        if pay_freq in ["weekly", "fortnightly"]:
            pay_period = get_pay_period(pay_freq)
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

        if (calculate_deposits (bill, due_date, next_pay_date, pay_freq)) == False:
            calculate_savings (bill, due_date, next_pay_date, pay_freq)

def calculate_savings (bill, due_date, next_pay_date, pay_freq):
    # need to go back in time to add savings
    # Find next_pay_date after bill is paid
    if pay_freq in ["weekly", "fortnightly"]:
        pay_period = get_pay_period(pay_freq)
        next_pay_date = next_pay_date + timedelta(days=pay_period)

#
# Test
#

next_pay_date = datetime(2017, 11, 3)
pay_freq = "fortnightly"

# initialize pay dates: deposits ammounts dict

pays_dict = {}

if pay_freq in ["weekly", "fortnightly"]:
    pay_period = get_pay_period(pay_freq)
    pay_date = next_pay_date
    pays_dict[pay_date] = 0
    # arbitrarily big
    for i in range(99):
        pay_date = pay_date + timedelta(days = pay_period)
        pays_dict[pay_date] = 0
elif pay_freq == "monthly":
    # TODO
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

# pays_dict = {key: value for key, value in pays_dict.items() if value != 0}

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
