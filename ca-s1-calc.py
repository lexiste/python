meal = 44.50
tax = 6.75 / 100
tip = 15.0 / 100

meal += meal * tax
# format the output into 2 decimal places since money
print("Meal and tax: " + format(meal * tax, '0.2f'))
print("Meal and tip (w/o tax): " + format(meal * tip, '0.2f'))

total = meal + (meal * tip)

# since all we did is change the display output to 2 decimal places and not the
# actual value stored in the variables, format the output here as well
print("Meal cost: " + format(meal, '0.2f') + " with tip and tax the total is: " + format(total, '0.2f'))
