inp_start = input("Enter start date (mm/dd/yyyy): ")
inp_dayoweek = input("Enter day of the week (number): ")
inp_days = input("Enter days passed: ")

month, day, year = inp_start.split("/")
month, day, year = int(month), int(day), int(year)
wday = int(inp_dayoweek)
days = int(inp_days)
days_31 = [1, 3, 5, 7, 8, 10, 12]
days_30 = [4, 6, 9, 11]
leap_years = [y for y in range(year, 9999) if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)]
passed = 0
while passed < days:
    passed += 1
    if month in days_31:
        day = day % 31 + 1
    elif month in days_30:
        day = day % 30 + 1
    else:
        day = day % 29 + 1 if year in leap_years else day % 28 + 1
    if day == 1:
        month = month % 12 + 1
        if month == 1:
            year += 1
    wday = wday % 7 + 1
wday_mapping = {7: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"}
print(f"End date: {wday_mapping[wday]}, {month}/{day}/{year}")