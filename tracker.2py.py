# Name- Sonam Yadav, Date-10/11/2025 ,Title- DAILY CALORIE TRACKER
"""
DAILY CALORIE TRACKER

Author: Sonam Yadav
Date: 10/11/2025

This Python-based tool allows users to monitor daily calorie intake in a quick and simple way.
It prompts users to input meal names and calorie amounts, calculates total and average calorie 
consumption per meal, and validates user responses for interactive prompts.

Functions:
    - do_you_want_permission: Requests and validates yes/no input from the user.
    - calc_avg_calorie: Computes the average calorie intake per meal, rounded to two decimal places.

Usage:
    Run the script and follow the interactive prompts to track and analyze your daily meal calorie
    data.
"""

print("Welcome, This Python tool helps you quickly track and analyze your daily calorie intake")


#ALL FUNCTIONS HERE
def do_you_want_permission(question_prompt):
    """
    Prompts the user with a yes/no question and validates the input.

    Args:
        question_prompt (str): The question to display to the user.

    Returns:
        bool: True if the user answers 'yes', False if the user answers 'no'.
    """
    while True:
        user_input = input(f"{question_prompt} (yes/no)? - ").lower().strip()
        if user_input == "yes":
            return True
        if user_input == "no":
            return False
        print("Please enter a valid answer (Yes or No)")

def calc_avg_calorie():
    """
    Calculates the average calories per meal.

    Returns:
        float: The average calories per meal, rounded to two decimal places.
    """
    avg_calorie = CALORIE_SUM / num_MEALS
    rounded_avg_calorie = round(avg_calorie,2)
    return rounded_avg_calorie

#main code stars here
Meal = []
Calories = []
num_MEALS = int(input("Enter the number of meals you want to add - "))
for i in range(1,num_MEALS + 1):
    Meal_name = input("Enter the name of your meal - ")
    Meal.append(Meal_name)
    calorie_amt = float(input("Enter the amount of your calorie intake - "))
    Calories.append(calorie_amt)


CALORIE_SUM = 0
for p in Calories:
    CALORIE_SUM += p
print("Total amount of your calorie intake is - ", float(CALORIE_SUM))


if do_you_want_permission("Do you want to see the average calories per meal?"):
    print("Calculating your data...")
    print(calc_avg_calorie())        #calculating and printing the average
else:
    print("Action cancelled")


#daily calorie limit according to google it was 3000 for an avg healthy human so i set it to this
DAILY_LIMIT = 3000
if do_you_want_permission("Do you want to set your own daily calorie limit?"):
    DAILY_LIMIT = float(input("Enter your daily calorie limit: "))
    print("Daily calorie limit Set to - ",DAILY_LIMIT)
else:
    print("Using default daily calorie limit of 3000.")


if CALORIE_SUM > DAILY_LIMIT :
    print("Your calorie intake for today exceeded your daily limit!!!")
else:
    print("Your calorie intake for today is in your daily limit.")

print("Meal name\tCalories")
print("--------------------------")
print(f"{Meal[0]}\t{Calories[0]}")
for j in range(1,num_MEALS):
    print(f"{Meal[j]}\t\t{Calories[j]}")
print(f"Total calorie\t{CALORIE_SUM}")
print(f"Average calorie\t{calc_avg_calorie()}")

# process of saving tha daily log starts here
if do_you_want_permission("Do you want to save todays report"):
    print("Proceeding with action")
    filename = input("Enter the name as of the file to be created! - ").strip()
    Date = input("Enter todays date in any format - ").strip()
    with open(filename, "a", encoding="UTF-8") as report:
        report.write(f"{Date}\n")
        report.write("Meal name\tCalories\n")
        report.write("--------------------------\n")
        report.write(f"{Meal[0]}\t{Calories[0]}\n")
        for j in range(1, num_MEALS):
            report.write(f"{Meal[j]}\t\t{Calories[j]}\n")
        report.write(f"Total calorie\t{CALORIE_SUM}\n")
        report.write(f"Average calorie\t{calc_avg_calorie()}\n")
else:
    print("Action Cancelled!")
