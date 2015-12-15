#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Monetary Muscle IS210 Final."""


def loopresponse(promptmessage, validchoices, failuremessage,
                 entermessage="", exitmessage=""):
    """Loops until a valid user resopnse is entered.
    Returns: users string
    """

    try:
        if entermessage != "":
            print entermessage

        keeplooping = True
        while keeplooping:
            choice = str(input(promptmessage)).upper()
            if choice in validchoices:
                keeplooping = False
            else:
                print failuremessage

        if exitmessage != "":
            print exitmessage

        return choice
    except Exception:
        return None


def pnotempty(message):
    """User will be prompted until they enter a response"""
    while True:
        result = str(input(message)).strip()
        if result != "":
            return result
        print "Empty input is invalid, try again"


def plegalnumer(message="", bepositive=False):
    """User will be prompted to enter a positive number"""
    if message == None:
        message = "Enter a {0}number".format("positive " if bepositive else "")

    while True:
        choice = pnotempty(message)
        try:
            if float(choice) >= 0 or float(choice) < 0 and not bepositive:
                return float(choice)
        except:
            pass

        print "Invalid number - please try again"


def enterincome(budgetlist):
    """ User enteres income."""
    print "Enter Income:"
    source = loopresponse("(check/cash):",
                          ["CHECK", "CASH"], "Invalid choice").capitalize()
    amount = plegalnumer("Amount:(positive numbers only)", True)
    if source.upper() == "CHECK":
        account = loopresponse("Which Account: Savings or Checking",
                               ["SAVINGS", "CHECKING"],
                               "Invalid account choice").capitalize()
        budgetlist.addincome(source, amount, account)
    else:
        account = loopresponse("Which Account: Savings or Checking",
                               ["SAVINGS", "CHECKING"],
                               "Invalid account choice").capitalize()
        budgetlist.addincome(source, amount, account)


def enterexpense(budgetlist, addnew=True):
    """User enters expenses."""
    print "All expenses:"
    for expense in budgetlist.expenses:
        print "Exp: {0} Cost: {1} account: {2}".format(expense[1],
                                                       expense[0], expense[2])
    print()

    if addnew:
        print "Enter New Expense:"
        etype = pnotempty("Enter the type of the expense")
        amount = plegalnumer("Expense Amount:", True)
        account = loopresponse("Which Account: Savings or Checking",
                               ["SAVINGS", "CHECKING"],
                               "Invalid account choice").capitalize()
        budgetlist.addexpense(etype, amount, account)


def balancedisplay(budgetlist):
    """User picks what blance they want to display"""
    account = loopresponse("Which Account Savings or Checking",
                           ["SAVINGS", "CHECKING"],
                           "Invalid account choice").capitalize()
    print "Balance:"
    print budgetlist.getbalance(account)


def getgoal(budgetlist):
    """User enters goals and sets goals. Does some math to show how much to goal."""
    print "All goals so far:"
    for goal in budgetlist.goals:
        print str(goal)

    target = float(plegalnumer("Enter new goal", True))
    budgetlist.addgoal(target)

    checkbudget = budgetlist.getbalance("Checking")
    savingsbudget = budgetlist.getbalance("Savings")
    total = checkbudget + savingsbudget

    # Displays checking goal details:
    if target - checkbudget > 0:
        print "You have {0} dollars in your checking account and need\
              {1} more to your goal.".format(checkbudget, target - checkbudget)
    else:
        print "Using your checking balance  ({0}) you have exeeded your\
               goal by {1} dollars".format(checkbudget, checkbudget-target)

    # Displays savings goal details:
    if target - savingsbudget > 0:
        print "You have {0} dollars in your savings and need {1} more to reach\
               your goal.".format(savingsbudget, target - savingsbudget)
    else:
        print "Using your savings balance ({0}) you have exeeded your goal by \
               {1} dollars".format(savingsbudget, savingsbudget-target)

    # Displays total goal details:
    if target - total > 0:
        print "You have {0} dollars in all accounts combined and need {1} more \
               to reach your goal.".format(total, target - total)
    else:
        print "Using money from all accounts combined ({0}) you have exeeded \
               your goal by {1} dollars".format(total, total-target)


def getreminders(budgetlist, addnew):
    """User sets remiders and can view reminders."""
    print "List Reminders:"
    for reminder in budgetlist.reminders:
        print str(reminder)

    if addnew:
        reminder = pnotempty("Enter Reminder:")
        budgetlist.addnewreminder(reminder)


class GOBUDGETLIST:
    """This constructor accepts a list of the format
    [[Incomes],[Expenses],[Reminders],[Goals]]"""
    def __init__(self, budgetaslist=[[], [], [], []]):
        """Constructor"""
        if len(budgetaslist) != 4:
            self.incomes = []
            self.expenses = []
            self.reminders = []
            self.goals = []
        else:
            self.incomes = budgetaslist[0]
            self.expenses = budgetaslist[1]
            self.reminders = budgetaslist[2]
            self.goals = budgetaslist[3]

    def addincome(self, source, amount, account):
        """User adds to income."""
        self.incomes.append([float(amount), source, account])

    def addexpense(self, expensetype, amount, account):
        """User adds to expenses"""
        self.expenses.append([float(amount), expensetype, account])

    def getbalance(self, account):
        """Does some math and gets totals for checking or savings."""
        ret = 0
        for elem in self.incomes:
            if elem[2].upper() == account.upper():
                ret += elem[0]
        for expense in self.expenses:
            if expense[2].upper() == account.upper():
                ret -= float(expense[0])

        return ret

    def addnewreminder(self, reminder):
        """Adds reminder."""
        self.reminders.append(reminder)

    def addgoal(self, goal):
        """Adds goals."""
        self.goals.append(goal)

    def loadfromfile(self, fileaddress):
        """Loads data from file into the current class instance. Looks for errors if more than 4 lines there is an error."""
        counter = 0
        try:
            for line in open(fileaddress, 'r'):
                if counter == 0:
                    self.incomes = eval(line)
                elif counter == 1:
                    self.expenses = eval(line)
                elif counter == 2:
                    self.goals = eval(line)
                elif counter == 3:
                    self.reminders = eval(line)
                counter += 1
            if counter != 4:
                raise Exception("Unexpected number of lines in the input file")
        except Exception as exc:
            print "Load failed with error: {0}".format(str(exc))
            return False
        print "Load suceeded"
        return True


    def savetofile(self, fileaddress):
        """Converts & converts the 4 class attributes, saves it to specified file"""
        try:
            file = open(fileaddress, "w")
            file.writelines([repr(self.incomes)+"\n", repr(self.expenses)+"\n",
                             repr(self.goals)+"\n", repr(self.reminders)])
            print "Save suceeded"
        except Exception as exp:
            print "Save failed with error {0}".format(str(exp))
        finally:
            file.close()


def mainmenu():
    """ Points to file load and save."""
    budget_file = "budget.txt"
    budgetlist = GOBUDGETLIST()
    if budgetlist.loadfromfile(budget_file) == False:
        print "Load budget file failed. Starting with a blank budget file."
        budgetlist = GOBUDGETLIST()

    while True:

        # This wall of text gets the user selction
        choice = loopresponse("1: Open File\n2: Save File\n3: Enter Income \
                              \n4: List Expenses\n5: Enter Expense\n6: Balance \
                              \n7: Goals\n8: List All Reminders \
                              \n9: Add New Reminder\n10: Quit",
                              ['1', '2', '3', '4', '5', '6', '7', '8',
                               '9', '10'],
                              "Invalid choice - please choose again")

        if choice == "1":
            if budgetlist.loadfromfile(budget_file) == False:
                print "Load Error, reverting to an empty budget."
                budgetlist = GOBUDGETLIST()
        elif choice == "2":
            budgetlist.savetofile(budget_file)
        elif choice == "3":
            enterincome(budgetlist)
        elif choice == "4":
            enterexpense(budgetlist, False)
        elif choice == "5":
            enterexpense(budgetlist, True)
        elif choice == "6":
            balancedisplay(budgetlist)
        elif choice == "7":
            getgoal(budgetlist)
        elif choice == "8":
            getreminders(budgetlist, False)
        elif choice == "9":
            getreminders(budgetlist, True)
        elif choice == "10":
            print "Goodbye"
            quit()
        print()

if __name__ == '__main__':
    mainmenu()


