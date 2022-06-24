from datetime import date, timedelta
import streamlit as st
import pandas as pd
import numpy as np



file = st.file_uploader("Upload your file")
cinema_name = st.text_input("Name:")
start_date = st.date_input("Date:")
button = st.button('Start')


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
def special_hall(k,venue):
        """
        This function transform the venue list, replacing strings with integers for venues

        """
        if k in venue:
            a = [j for j in range(len(venue)) if venue[j] == k]
            if a[0] == 0:
                venue[a[0]:a[-1] + 1] = [1 for _ in range(len(a))]
            else:
                venue[a[0]:a[-1]+1] = [int(venue[a[0]-1])+1 for venue[a[0]] in range(len(a))]
def main_function(file,cinema_name,start_date,button):
    # --- Initialising SessionState ---
    if "load_state" not in st.session_state:
        st.session_state.load_state = False
    xml_files = []
    if button:
        week_dict = {"Monday":"L","Tuesday":"Ma","Wednesday":"Mi","Thursday":"J","Friday":"V","Saturday":"S","Sunday":"D"}
        day = start_date.day
        day_name = start_date.strftime("%A")
        weekdays = [(day,week_dict[day_name])]
        for i in range(1,7):
            next_date = start_date + timedelta(days=i)
            next_date_name =  week_dict[next_date.strftime("%A")]
            weekdays.append((next_date.day, next_date_name))
        print(weekdays)
        file = pd.read_excel(file, sheet_name=cinema_name)
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

        special_hall('4DX',venue)
        special_hall('IMAX',venue)
        special_hall('VIP',venue)
        # print(venue)
        # st.dataframe(file)
        file['Venue'] = np.array(venue)

        cineworld = cinema_city(file)
        # xml_files = []
        print(weekdays)
        for item in weekdays:
            number = int(item[0])
            day  = item[1]
            with open(f'cpc-{number}.xml', 'w') as f:
                for kvp in cineworld.items():
                    print(f'<hall{kvp[0]}>', file=f)
                    for element in kvp[1]:
                        if 'Only' in element[0]:
                            if str(day) in element[0]:
                                print(f"<a title='{element[1]}' h='{element[0][:2]}' m='{element[0][3:5]}' />", file=f)
                        elif 'W/O' in element[0]:
                            if str(day) not in element[0]:
                                print(f"<a title='{element[1]}' h='{element[0][:2]}' m='{element[0][3:5]}' />", file=f)
                        else:
                            print(f"<a title='{element[1]}' h='{element[0][:2]}' m='{element[0][3:5]}' />", file=f)
                    print(f'</hall{kvp[0]}>', file=f)
                xml_files.append(f)
    return xml_files
    
        # os.remove(xml)
# for xml in xml_files:
#     # st.download_button(f'Download {xml}')
#     # time.sleep(1)
#     os.remove(xml)

files = main_function(file,cinema_name,start_date,button)
# for xml in files:
#     with open(xml, 'r') as f:
#         st.download_button(label = f'Download {f.name}',data = f.read(),file_name=f.name)