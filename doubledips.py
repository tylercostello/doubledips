#!/usr/bin/env python3

#By Tyler Costello


import requests
import re
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# what semester you want
# 4320 is winter of 2022
# they usually go up by 20 each quarter but you should check exactly which one you want by using the network developer tools on chrome when you search for a class
semester = "4400"

# gets input to search for all classes or open seats only
openinput = input("Type a for all classes or o for open seats only and press enter: ")
classcounter = 0

# the abbreviations that course avail uses for each core
# they are listed in the order they appear in the list on course avail in case you need to check what an abbreviation means
cores = ['I_AW', 'E_ARTS', 'E_CE', 'F_CI1', 'F_CI2', 'E_CI3', 'E_DV', 'E_ETH', 'I_EL', 'F_MATH', 'E_NTSC', 'E_ARTSPAR',
         'E_CEPAR', 'E_STSPAR', 'F_RTC1', 'E_RTC2', 'E_RTC3', 'E_STS', 'F_SLA2', 'F_SLA1', 'E_SOSC']

f = open("classes.txt", "w")
writeString = ""
# loops through check every combination of classes
for x in range(len(cores)):
    for y in range(x + 1, len(cores)):
        if openinput == "o":
            # post request for open seats only
            r = requests.post('https://www.scu.edu/apps/ws/courseavail/search/' + semester + '/ugrad',
                              data={'newcore': cores[x], 'newcore2': cores[y], 'openseats': 1})
        else:
            # post request for all classes
            r = requests.post('https://www.scu.edu/apps/ws/courseavail/search/' + semester + '/ugrad',
                              data={'newcore': cores[x], 'newcore2': cores[y]})
        classString = r.text
        # uses regex to find class numbers
        locations = [m.start() for m in re.finditer('class_nbr', classString)]
        # adds classes to list if they have a double dip
        if len(locations) > 0:
            writeString = writeString + "Double Dips: " + cores[x] + " " + cores[y] + ":\n"
            for loc in locations:
                print(loc)
                classcounter += 1
                # gets class number with string slicing
                writeString = writeString + classString[loc + 12:loc + 17] + " "
            writeString = writeString + "\n"
        print(cores[x] + " " + cores[y])
f.write(writeString)
f.close()
print("Number of classes found: "+str(classcounter))
