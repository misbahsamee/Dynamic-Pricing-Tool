import os
import pricing


print("Dynamic Pricing Tool:\n")

username = os.getlogin()
print(f"Hello, {username}!\n")
while True:
    try:
        day = int(input("Enter the day: "))
        month = int(input("Enter the month: "))
        if month < 1 or month > 12:
            raise ValueError("Month must be between 1 and 12")
        if day < 1 or day > 31:
            raise ValueError("Day must be between 1 and 31")
        if (month == 2 and day > 29) or ((month == 4 or month == 6 or month == 9 or month == 11) and day > 30):
            raise ValueError("Invalid day for the given month")
        break
    except ValueError as e:
        print("Invalid input: ", e)


print("Generating 'result.csv'...")

df = pricing.max_revenue(day, month)

print("File has been generated!")

df.to_csv('result.csv', index=False)
