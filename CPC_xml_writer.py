# Import the necessary packages
import pandas as pd
import numpy as np
from open_excel_file import open_file
from GUI import return_strings

# This part of code opens a 'open window'

file = open_file()


e1, e2 = return_strings()


file = pd.read_excel(file,
                     sheet_name=e1.get())

# delete the first row
file = file.drop(0, axis=0)

# delete the unnecessary columns
file = file.drop(['Rating', 'Language', 'Sub & Dub',	'Length',
                  'Gross Length',	'Distributor',	'Week Number',
                  'Unnamed: 9', 'Unnamed: 10'], axis=1)

# fill the venue column using 'ffill'
file['Venue'].fillna(method='ffill', inplace=True)

# use a counter to count the rows of the 'Event Master' column until we reach the legend, then we take a step back
count = 0
for _ in file['Event Master']:
    if _ != 'Legend':
        count += 1
    else:
        count -= 1
        break

# delete the last rows that we don't need ('legend', 'Movies In', 'Movies OUT' etc)
file = file.loc[0:count, :]


# iterate over Venue to find if we have a 4DX, IMAX or VIP venue
venue = [i.split()[0] for i in file['Venue']]


def special_hall(k):
    """
    This function transform the venue list, replacing strings with integers for venues

    """
    if k in venue:
        a = [j for j in range(len(venue)) if venue[j] == k]
        if a[0] == 0:
            venue[a[0]:a[-1] + 1] = [1 for _ in range(len(a))]
        else:
            venue[a[0]:a[-1]+1] = [int(venue[a[0]-1])+1 for venue[a[0]] in range(len(a))]


special_hall('4DX')
special_hall('IMAX')
special_hall('VIP')


file['Venue'] = np.array(venue)


def cinema_city(a):
    """
    This function take the modified excel file and returns a dictionary with halls,hours and shows
    """
    cc = {}
    # iterating through dataframe rows
    cinema = [list(row.dropna()) for index, row in a.iterrows()]
    for _ in cinema:
        hall, show, hours = _[0], _[1], _[2:]
        for hour in hours:
            if hall not in cc:
                cc[hall] = [(hour, show)]
            else:
                cc[hall].append((hour, show))
        cc[hall].sort()
        return cc


cineworld = cinema_city(file)
week = ['V', 'S', 'D', 'L', 'Ma', 'Mi', 'J']

friday = e2.get().split('/')

month = int(friday[1])

if month in [1, 3, 5, 7, 8, 10, 12]:
    month = 31
elif month in [4, 6, 9, 11]:
    month = 30
elif month == 2:
    month = 28
for zi in week:
    data = int(friday[0]) + week.index(zi)
    if data > month:
        data -= month
    with open(f'cpc-{data}.xml', 'w') as f:
        for kvp in cineworld.items():
            print(f'<hall{kvp[0]}>', file=f)
            for element in kvp[1]:
                if 'Only' in element[0]:
                    if zi in element[0]:
                        print(f"<a title='{element[1]}' h='{element[0][:2]}' m='{element[0][3:5]}' />", file=f)
                elif 'W/O' in element[0]:
                    if zi not in element[0]:
                        print(f"<a title='{element[1]}' h='{element[0][:2]}' m='{element[0][3:5]}' />", file=f)
                else:
                    print(f"<a title='{element[1]}' h='{element[0][:2]}' m='{element[0][3:5]}' />", file=f)
            print(f'</hall{kvp[0]}>', file=f)
