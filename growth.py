# Test bed to make compounding interest with a yearly contribution (begginingg of year)
# Compouning interest: A = P(1 + (r/n))^nt
from helpers import usd
import matplotlib.pyplot as plt

# Define variables
savings = 1000
salary = 55000
savingRate = 15
age = 22
yieldAnnual = 4.2
retirementAge = 80
payIncrease = 2.3
expense = 100000
contribution = (savingRate / 100) * salary
yearsSaving = (retirementAge - age)
p = savings
x = pow((1 + (yieldAnnual / 100)), yearsSaving)
a = p * x
totalBalance = a
empty = 0;

# compounding interest function
def compound(P, r, t):
    A = P * (pow((1 + (r / 100)), t))
    return A

ageByYear = []
moneyByYear = []
ageByYear.append(age)
moneyByYear.append(savings)

# Interest while saving
for year in range(yearsSaving):
    contribution = contribution * ((payIncrease / 100) + 1)
    totalBalance = compound(totalBalance, yieldAnnual, 1) + compound(contribution, yieldAnnual, 1)
    # Insert into array for graph
    myAge = age + year + 1
    ageByYear.append(myAge)
    moneyByYear.append(totalBalance)
peak = totalBalance

# Interest in retirement
for x in range(120):
    if totalBalance > 0:
        if myAge > 120:
            break
        else:
            totalBalance = compound((totalBalance - expense), yieldAnnual, 1)
            myAge = myAge + 1
            ageByYear.append(myAge)
            moneyByYear.append(totalBalance)

    # Years supported by retirement
    else:
        empty = myAge
        break

if empty > 0:
    print("Peak savings = " + str(usd(peak)))
    print("Retirment will run out at age " + str(empty))
else:
    print("Retirement will last indefinitely with set expense")
    print("You will have " + str(usd(totalBalance)) + " at age 120")

plt.plot(ageByYear, moneyByYear)
plt.ylabel('Cash')
plt.xlabel('Age')
plt.show()
