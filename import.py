####################################################################################################################################################################################################################
#
# Copyright 2018 William Arbaugh
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
####################################################################################################################################################################################################################

import datetime
import csv
import re

def CleanTime (Time):
    "The kids often enter time in bizare ways. Normalize it."
    # Ensure the time string is of the form NN:NN.NN
    TimeList = re.findall('\d+', Time)
    TimeLen = len(TimeList)
    if TimeLen == 3:
        Time = TimeList[0] + ":" + TimeList[1] + "." + "{0:0<2}".format(TimeList[2])
    elif TimeLen == 2:
        Time = TimeList[0] + "." + "{0:0<2}".format(TimeList[1])
    elif TimeLen == 1:
        Time = TimeList[0] + ".00"
    else:
        # Yes - the spaces are necessary.
        # NT needs to be left justified,
        # while if we have a time it is
        # right justified. Who makes this
        # stuff up?
        Time = "NT      "
    return Time

def EmitC1 (TeamName):
    # TeamName[:6] is substitute for Team Code...and is presumed unique
    # Timestamp,Last Name,First Name,Email,Cell Phone,School,Grade,Available for Relays,Gender,MEvent 1,MTime 1,MEvent 2,MTime 2,WEvent 1,WTime 1,WEvent 2,WTime 2
    #
    print "{0:2}{1:1}{2:8}{3:6}{4:30}{5:16}{6:22}{7:22}{8:20}{9:2}{10:10}{11:3}{12:1}{13:6}{14:1}{15:10}\r".format(
    "C1","9", "", "MD"+TeamName[:4], TeamName, TeamName[:16], "", "", "", "MD", "", "USA", "1", "", "", "")

def EmitC2 (TeamName):
    print "{0:2}{1:1}{2:8}{3:6}{4:30}{5:12}{6:6}{7:6}{8:5}{9:6}{10:6}{11:16}{12:45}{13:1}{14:10}\r".format(
    "C2","9","", "MD" + TeamName[:4], TeamName, "", "", "", "", "", "", TeamName[:16], "", "", "")

def GenUSSNum (FirstName, LastName, Birthdate):
    if len(FirstName) < 3:
        FirstName = FirstName.ljust(3, '*')
    if len(LastName) < 4:
        LastName = LastName.ljust(4, '*')
    return Birthdate + FirstName[:3] + '*' + LastName[:4]

def EmitD0 (FirstName, LastName, School, Year, Gender, Event, Time):
    EventGender_List = ['X','X','X','X','X','M','W','X','X','X','X','X','X','X','M','W','X','X']
    FullName = LastName + ", " + FirstName

    # Look-up table for Class
    Class = {'9':'FR','10':'SO', '11':'JR', '12':'SR'}
    Strokes = {'Freestyle': 1, 'Backstroke':2, 'Breaststroke':3, 'Butterfly':4, 'Individual':5}

    # Parse out the event
    EventList = Event.split()
    EventNum = EventList[0]
    iEventNum = int(EventNum)
    EventGender = EventGender_List[iEventNum]
    EventDist = EventList[2]
    EventStroke = Strokes[EventList[4]]
    
    print "{0:2}{1:1}{2:8}{3:28}{4:12}{5:1}{6:3}{7:8}{8:2}{9:1}{10:1}{11:>4}{12:1}{13:>4}{14:4}{15:8}{16:>8}{17:1}{18:63}\r".format(
    "D0","9","", FullName[:28],"0101","A","USA","01011995",Class[Year],Gender[:1],EventGender, EventDist, EventStroke, EventNum, "UNOV", "04222012", CleanTime(Time), "Y", "")

def EmitD3 (FirstName, LastName):
    # Yup - another grand idea
    # This record has the USSNum as 14 Characters
    # The birthdate is hard coded since we don't care about that
    #
    USSNum = GenUSSNum(FirstName, LastName, "010195")
    print "{0:2}{1:14}{2:15}{3:129}\r".format("D3",USSNum,FirstName[:15],"")

def EmitSwimmer (FirstName, LastName, School, Year, Gender, Event1, Time1, Event2, Time2):
    # One per splash so we emit two D0 records and a D3.
    # We have to emit as D0, D3, D0 .... yeah it is stupid
    EmitD0(FirstName, LastName, School, Year, Gender, Event1, Time1)
    EmitD3(FirstName, LastName)
    EmitD0(FirstName, LastName, School, Year, Gender, Event2, Time2)

# File columns are:
# 
ifile = open('entries.csv', "rU")
reader = csv.DictReader(ifile)
CreateDate = datetime.date.today()

# Emit A0 - file description
print "{0:2}{1:1}{2:8}{3:2}{4:30}{5:20}{6:10}{7:20}{8:12}{9:8}{10:42}{11:2}{12:3}\r".format(
    "A0", "9", "3.0", "01", "", "Python Importer", "v0.01", "youraddresshere@gmail.com", "4105551212",
    CreateDate.strftime("%m%d%Y"),"", "MD", "")

# Emit B1 - Meet record
# You'll want to change this for your meet
#
print "{0:2}{1:1}{2:8}{3:30}{4:22}{5:22}{6:20}{7:2}{8:10}{9:3}{10:1}{11:8}{12:8}{13:4}{14:8}{15:1}{16:10}\r".format(
    "B1","9","","Howard Cty Swimming Champs","","","Columbia","MD","21045","USA","1","04302017","04302017","", "", "Y","")
 
# Emit B2 - Meet host
print "{0:2}{1:1}{2:8}{3:30}{4:22}{5:22}{6:20}{7:2}{8:10}{9:3}{10:12}{11:28}\r".format(
    "B2","9","","Columbia Aquatics","","","Columbia","MD","","USA","","")

Schools = {}
Swimmers = {}

for row in reader:
    #
    # New columns are: Timestamp,First Name,Last Name,Email,Cell Phone,School,Grade,Available for Relays,Gender,Event 1,Event 1,Event 2,Event 2
    #
    # NOTE: We assume that the CSV file is sorted by school name. It will not work otherwise.
    # Check school name, and if it is new emit a Team id record (C1)
    # and team stat record (C2)
    #
    School = Schools.get(row['School'])
    if School != row['School']:
        # This is the first entry for School
        # emit C1 and C2 records
        School = row['School']
        Schools[School] = School
        EmitC1(School)
        EmitC2(School)

    # School C1/C2 records have been emitted already
    # so emit D3 and D0 records for individual
    Gender = row['Gender']
    Event1 = row['Event 1']
    Time1 = row['Time Event 1']
    Event2 = row['Event 2']
    Time2 = row['Time Event 2']
        
    EmitSwimmer(row['First Name'], row['Last Name'], row['School'], row['Grade'], row['Gender'], Event1, Time1, Event2, Time2)

    

# Emit Z0 record
print "{0:2}{1:1}{2:8}{3:2}{4:147}\r".format("Z0","9","","01","")

    
ifile.close()
