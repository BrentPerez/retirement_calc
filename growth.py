# Test bed to make compounding interest with a yearly contribution (begginingg of year)
# Compouning interest: A = P(1 + (r/n))^nt
from helpers import usd

# Define variables
savings = float(input("Current savings: "))
salary = float(input("Current Salary: "))
savingRate = float(input("Percent of Salary Saved: "))
age = int(input("Current Age: "))
yieldAnnual = float(input("Expected Annual Return: "))
retirementAge = int(input("Age of Retirement: "))
expense = 100000
contribution = (savingRate / 100) * salary
yearsSaving = (retirementAge - age)
p = savings
x = pow((1 + (yieldAnnual / 100)), yearsSaving)
a = p * x
totalBalance = a

# compounding interest function
def compound(P, r, t):
    A = P * (pow((1 + (r / 100)), t))
    return A

yearByYear = []
yearByYear.append([age,savings])

for year in range(yearsSaving):
    numYear = yearsSaving - year
    totalBalance = totalBalance + compound(contribution, yieldAnnual, numYear)
    # Insert into array for graph
    myAge = age + year + 1
    yearByYear.append([myAge,totalBalance])

# Years supported by retirement w/o interest
empty = (totalBalance / expense) + retirementAge


print("Retirment will run out at age " + "{:.1f}".format(empty))
print(usd(totalBalance))

