from datetime import datetime, timedelta
from math import floor

def calculate_deposit(bill, due_date, next_pay_date, pay_freq):

    time_until_bill = (due_date - next_pay_date)
    print("time_until_bill: " + str(time_until_bill))

    days_until_bill = time_until_bill.days
    print("days_until_bill: " + str(days_until_bill))

    if pay_freq == "weekly":
        pay_period = 7
    elif pay_freq == "fortnightly":
        pay_period = 14

    pays_before_bill = 0

    # special case monthly because timedelta doesn't handle it
    if pay_freq == "monthly":
        test_date = next_pay_date

        while test_date < due_date:
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
        pays_before_bill = floor( days_until_bill / pay_period )

    print("pays_before_bill: " + str(pays_before_bill))

    deposit = bill/pays_before_bill
    deposit_rounded = round(deposit, 2)

    return deposit_rounded

def calc_reoccuring_cost (bill, due_date, debt_freq, next_pay_date, pay_freq):
    # debt_freq = "weekly", "fortnightly", "monthly", "quarterly", "biannually", "annually"
    # pay_freq = "weekly", "fortnightly", "monthly"

    deposit = calculate_deposit (bill, due_date, next_pay_date, pay_freq)

    if pay_freq == "weekly":
        pay_period = 7
    elif pay_freq == "fortnightly":
        pay_period = 14

    # Find next_pay_date after bill is paid
    if pay_freq in ["weekly", "fortnightly"]:
        while next_pay_date < due_date:
            next_pay_date = next_pay_date + timedelta(days=pay_period)

    # special case monthly because timedelta doesn't handle it
    if pay_freq == "monthly":
        next_pay_date = due_date

        while next_pay_date < due_date:
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

    reoccur_deposit = calculate_deposit (bill, due_date, next_pay_date, pay_freq)

    print("deposit " + str(deposit) + " every pay until " + str(next_pay_date) + "...")
    print("... then deposit " + str(reoccur_deposit) + " every pay until from then on.")

#
# Test
#

fake_due_date = datetime.today() + timedelta(days = 74)
fake_next_pay_date = datetime.today() + timedelta(days = 10)
fake_pay_freq = "fortnightly"
fake_bill = 4512.18
fake_debt_freq = "quarterly"

calc_reoccuring_cost (fake_bill, fake_due_date, fake_debt_freq, fake_next_pay_date, fake_pay_freq)
