#!/usr/bin/python3
# coding=<UTF-8>
# <<< Start of code

def read_info_from_file(f, locality, countrycode):
    """read file    
    All lines in the file with a P in column 7 are localities (cities, villages .. )
    locality names in column 2
    Only consider localities with > 0 inhabitants (column 15)
    country code in column 9
    
    """
    line = f.readline()
    if len(line) == 0: # EOF
        return -1    
    if '#' in line:
        return 0    
    line = line[(line.find('/t')+2):] # next Tab:2
    locality = line[:(line.find('/t'))].strip() # Name der lokalitaet herausziehen
    line = line[(line.find('/t')+2):] # next Tab:3
    line = line[(line.find('/t')+2):] # next Tab:4
    line = line[(line.find('/t')+2):] # next Tab:5
    line = line[(line.find('/t')+2):] # next Tab:6
    line = line[(line.find('/t')+2):] # next Tab:7
    if not "P" in line[:(line.find('/t'))].strip(): # Ueberpruefung: P in column 7
        return 0
    line = line[(line.find('/t')+2):] # next Tab:8
    line = line[(line.find('/t')+2):] # next Tab:9
    countrycode = line[:(line.find('/t'))].strip()
    line = line[(line.find('/t')+2):] # next Tab:10
    line = line[(line.find('/t')+2):] # next Tab:11
    line = line[(line.find('/t')+2):] # next Tab:12
    line = line[(line.find('/t')+2):] # next Tab:13
    line = line[(line.find('/t')+2):] # next Tab:14
    line = line[(line.find('/t')+2):] # next Tab:15
    if float(line[:(line.find('/t'))].strip()) <= 0: 
        # Ueberpruefung: inhabitants in clumn 15 < 0
        return 0
    return 1


# def compute_most_frequent_city_names_by_sorting():

    
def compute_most_frequent_city_names_by_map():
    """bla
    
    """
    file = open("AT.txt", "r")
    
    a_array = dict()
    locality = ""
    countrycode = ""
    status = read_info_from_file(file, locality, countrycode)
    while (status != -1):
        if status == 1:
            if locality in a_array:
                a_array[locality] += 1
            else:
                a_array[locality] = 1
        status = read_info_from_file(file, locality, countrycode)
    file.close()
    
if __name__ == "__main__":
    """blubb
    """
    compute_most_frequent_city_names_by_map()
# <<< End of code