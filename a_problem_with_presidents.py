import pandas, statistics
from tabulate import tabulate
from datetime import datetime

# import excel file using pandas
workbook = pandas.read_csv('presidents.csv')

# parse spreadsheet to extract birth date
bdates = {}
ind = 0
for bdate in workbook['BIRTH DATE']:
    if pandas.isna(bdate):
        ind+=1
        continue
    if "June" in str(bdate) or "July" in str(bdate):
        date_format = "%B %d, %Y"
    else:
        date_format = "%b %d, %Y"
    bdate = datetime.strptime(str(bdate), date_format)
    bdates[workbook['PRESIDENT'][ind]] = bdate
    ind += 1

# parse spreadsheet to extract death date for deceased presidents
# associate death date with president and calculate number of days lived
lived_days = {}
ind = 0
for ddate in workbook['DEATH DATE']:
    if pandas.isna(ddate):
        ind+=1
        continue
    if "June" in str(ddate) or "July" in str(ddate):
        date_format = "%B %d, %Y"
    else:
        date_format = "%b %d, %Y"
    ddate = datetime.strptime(str(ddate), date_format)
    delta = ddate - bdates[workbook['PRESIDENT'][ind]]
    lived_days[workbook['PRESIDENT'][ind]] = delta.days
    ind += 1

# calculate months and years lived by each president
lived_months = {pres:round(days/12) for pres, days in lived_days.items()}
lived_years = {pres:round(days/365.25) for pres, days in lived_days.items()}

# create descending table of 10 longest-lived presidents
longest = sorted(lived_years.items(), key = lambda x:x[1], reverse = True)
long_table = [("PRESIDENT", "LIFESPAN")]
for pair in longest[0:10]:
    long_table.append(pair)
table_of_longest = tabulate(
long_table, headers = "firstrow", tablefmt = "fancy_grid"
)

# create ascending table of 10 shortest-lived presidents
shortest = sorted(lived_years.items(), key = lambda x:x[1])
short_table = [("PRESIDENT", "LIFESPAN")]
for pair in shortest[0:10]:
    short_table.append(pair)
table_of_shortest = tabulate(
short_table, headers = "firstrow", tablefmt = "fancy_grid"
)

# calculate statistics from the distribution of days lived
mean = statistics.mean(lived_days.values())
median = statistics.median(lived_days.values())
# check if there is a mode
if len(statistics.multimode(lived_days.values())) == 39:
    mode = "no mode"
else:
    mode = statistics.mode(lived_days.values())
maximum = max(lived_days.values())
minimum = min(lived_days.values())
deviation = statistics.stdev(lived_days.values())
stats_table = tabulate([
    ("mean", "%.3f" % mean), ("weighted average", "%.3f" % mean),
    ("median", "%.3f" % median), ("mode", mode), ("maximum", "%.3f" % maximum),
    ("minimum", "%.3f" % minimum), ("standard deviation", "%.3f" % deviation)
], headers = ("STATISTIC", "VALUE"), tablefmt = "fancy_grid")

# export data frame of presidents and days lived to excel file for visualizing
data = pandas.DataFrame(list(zip(
lived_years.keys(),lived_days.values())),
columns = ["president", "days lived"])
data.to_excel("presidents_data.xlsx")
