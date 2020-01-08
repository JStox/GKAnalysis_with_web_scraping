# Goal: Create a play by play for the premier league based on seasons

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import url_scrape

class Event:
    def __init__(self, time, event, team, player, label):
        self.time = time
        self.event = event
        self.team = team
        self.player = player
        self.label = label

    def __str__(self):
        return f'{self.time} - {self.player} - {self.team} - {self.event} - {self.label}'

def sort_arrays(arr0, arr1):
    final_arr = []
    i = 0
    j = 0
    while i < len(arr0) and j < len(arr1):
        if i < j:
            final_arr.append(arr0[i])
            i += 1
        elif i > j:
            final_arr.append(arr1[j])
            j += 1
        else:
            final_arr.append(arr1[j])
            j += 1
    return final_arr

# # given a url it will get all the game info for the url
# class GameParser:
#     def __init__(self, url):
#         with open(url) as html:
#             self.soup = BeautifulSoup(html, 'lmxl')
    
#     def __call__(self, table_class, *args):
#         all_tables = self.soup.find_all('table', class_=table_class)
#         for arg in args:
#             for table in all_tables:
#                 result = table.find('tr', class_=arg)
#                 if result is not None:
#                     break
#             table_rows = table.find_all('tr', class_=arg)
#             self.list_of_events = []
#             for tr in table_rows:
#                 if tr.strong is None:
#                     continue
#                 time = tr.find('td', class_='shsTotD shsEventsTimeCol')
#                 time = time.contents #time is now a list of one string with a number and a
#                 if time is not None:
#                     time = time[0]
#                     time = time[:-1]
#                 full_event = tr.find('td', class_='shsNamD shsEventsCol')
#                 event = full_event.strong.contents
#                 if event is not None:
#                     event = event[0]
#                 else:
#                     event = None
#                 full_event = full_event.contents
#                 team = full_event[-1]
#                 start_pos = team.find('(')
#                 end_pos = team.find(')')
#                 team = team[start_pos+1:end_pos]
#                 self.list_of_events.append(Event(time, event, team, arg))

#         def clean(self):
#             self.list_of_events.reverse()
#             try:
#                 int(list_of_events[0].time)
#             except:
#                 list_of_events.pop(0) # remove first element if it doesnt have a time


if __name__ == '__main__':
    o_url = 'http://scores.nbcsports.com/epl/fixtures.asp?month='
    months = [str(i) for i in range(8, 13)] + [1]
    urls = []
    df = pd.DataFrame(columns=['time', 'event', 'team', 'game'])
    for month in months:
        urls += url_scrape.scrape_urls(o_url, month)


    for url in urls:
        page = requests.get(url)
        if page.status_code != 200:
            print(f'Url returned {page.status_code}')
            break
        parser = BeautifulSoup(page.content, 'html.parser')
        all_tables = parser.find_all('table', class_='shsTable') # This website has 7 different tables with the same class, some nested inside each other...
        for table in all_tables:
            result = table.find('tr', class_='shsRow1Row')
            if result is None:
                continue
            else:
                break

        table_rows_1 = table.find_all('tr', class_='shsRow1Row')
        table_rows_0 = table.find_all('tr', class_='shsRow0Row')

        list_of_events_1 = []
        for tr in table_rows_1:
            if tr.strong is None:
                continue
            time = tr.find('td', class_='shsTotD shsEventsTimeCol')
            time = time.contents #time is now a list of one string with a number and a
            if time is not None:
                time = time[0]
                time = time[:-1]
            full_event = tr.find('td', class_='shsNamD shsEventsCol')
            event = full_event.strong.contents
            if event is not None:
                event = event[0]
            else:
                event = None
            full_event = full_event.contents
            team = full_event[-1]
            start_pos = team.find('(')
            end_pos = team.find(')')
            team = team[start_pos+1:end_pos]
            list_of_events_1.append(Event(time, event, team, 'shsRow1Row'))

        list_of_events_0 = []
        for tr in table_rows_0:
            if tr.strong is None:
                continue
            time = tr.find('td', class_='shsTotD shsEventsTimeCol')
            time = time.contents #time is now a list of one string with a number and a
            if time is not None:
                time = time[0]
                time = time[:-1]
            full_event = tr.find('td', class_='shsNamD shsEventsCol')
            event = full_event.strong.contents
            if event is not None:
                event = event[0]
            else:
                event = None
            full_event = full_event.contents
            team = full_event[-1]
            start_pos = team.find('(')
            end_pos = team.find(')')
            team = team[start_pos+1:end_pos]
            list_of_events_0.append(Event(time, event, team, 'shsRow0Row'))

        list_of_events_0.reverse()
        list_of_events_1.reverse()
        try:
            error = int(list_of_events_0[0].time)
        except:
            print('Removing first element of list because no minute')
            list_of_events_0.pop(0)
        try:
            error = int(list_of_events_1[0].time)
        except:
            print('Removing first element of list because no minute')
            list_of_events_1.pop(0)

        final_arr = sort_arrays(list_of_events_0, list_of_events_1)
        print(len(final_arr))
        times = []
        events = []
        teams = []
        for el in final_arr:
            times.append(el.time)
            events.append(el.event)
            teams.append(el.team)

        final_dict = {'time':times, 'event':events, 'team':teams, 'game':[set(teams) for i in range(len(teams))]}
        df_1 = pd.DataFrame(final_dict)
        df = pd.concat([df, df_1], axis=0)

    df.to_csv('play_by_play.csv')
                #print(full_event)

                # items = tr.find_all('td')
                # if tr.strong.contents[0] == 'Shot on Goal':
                #     print(items[0], items[1])

                #print(items[0])
                #print(items[1].contents)
                #shsTotD shsEventsTimeCol
