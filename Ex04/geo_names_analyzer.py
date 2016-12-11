#!/usr/bin/python3
# coding=<UTF-8>
# <<< Start of code

import zipfile
import operator
import cProfile

def read_info_from_file(f):
    """read file    
    All lines in the file with a P in column 7 are localities (cities, villages .. )
    locality names in column 2
    Only consider localities with > 0 inhabitants (column 15)
    country code in column 9
    
    """
    line = f.readline().decode('utf8')
    if len(line) == 0: # EOF
        return "-1"
    if '#' in line:
        return "0"
    line = line[(line.find('\t')+1):] # next Tab:2
    locality = line[:(line.find('\t'))].strip() # Name der lokalitaet herausziehen
    line = line[(line.find('\t')+1):] # next Tab:3
    line = line[(line.find('\t')+1):] # next Tab:4
    line = line[(line.find('\t')+1):] # next Tab:5
    line = line[(line.find('\t')+1):] # next Tab:6
    line = line[(line.find('\t')+1):] # next Tab:7
    if not "P" in line[:(line.find('\t'))].strip(): # Ueberpruefung: P in column 7 -> Ortschaft
        status = 0
        # print("not a locality")
        return "0"
    line = line[(line.find('\t')+1):] # next Tab:8
    line = line[(line.find('\t')+1):] # next Tab:9
    countrycode = line[:(line.find('\t'))].strip() # Laendercode herausziehen
    line = line[(line.find('\t')+1):] # next Tab:10
    line = line[(line.find('\t')+1):] # next Tab:11
    line = line[(line.find('\t')+1):] # next Tab:12
    line = line[(line.find('\t')+1):] # next Tab:13
    line = line[(line.find('\t')+1):] # next Tab:14
    line = line[(line.find('\t')+1):] # next Tab:15
    inhabitants = int(line[:(line.find('\t'))].strip())
    if inhabitants <= 0: # Ueberpruefung: inhabitants in clumn 15 <= 0
        status = 0
        return "0"
    status = 1
    string = locality + "\t" + countrycode
    return string


def compute_most_frequent_city_names_by_sorting(filename):
    """Zeile fuer Zeile einlesen, array nach name durchsuchen und aufnehmen wenn nicht vorhanden oder value erhoehen wenn bereits vorhanden.
    speichert in 2d array ab (name, anzahl)

    >>> compute_most_frequent_city_names_by_sorting("")
    Traceback (most recent call last):
        ...
    ValueError: No filename given

    >>> compute_most_frequent_city_names_by_sorting(5)
    Traceback (most recent call last):
        ...
    ValueError: Filename must be of type String

    >>> compute_most_frequent_city_names_by_sorting("test")
    End Of File
    Ortsname:   2
    Ortsname4:	1
    """
    if type(filename) != str:
        raise ValueError("Filename must be of type String")
    if len(filename) == 0:
        raise ValueError("No filename given")
    
    zfile = zipfile.ZipFile(filename + ".zip")
    file = zfile.open(filename + ".txt")
    names = []
    string = read_info_from_file(file)
    while string != "-1":
        if string != "0":
            found = 0
            for i in range(0, len(names)):
                if names[i][0] == string[:(string.find('\t'))].strip():              
                    names[i][1] += 1
                    found = 1
            if found == 0:
                names.append([])
                names[len(names)-1].append(string[:(string.find('\t'))].strip())
                names[len(names)-1].append(1)
        string = read_info_from_file(file)
    print("End Of File")
    file.close()
    if len(names) > 0:
        sort = sorted(names,key=lambda x: x[1], reverse = True)
        if len(sort) >= 3:
            print(sort[0][0] + ":\t" + str(sort[0][1]) + "\n" +  sort[1][0] + ":\t" + str(sort[1][1]) + "\n" + sort[2][0] + ":\t" + str(sort[2][1]))
            return
        if len(sort) >= 2:
            print(sort[0][0] + ":\t" + str(sort[0][1]) + "\n" +  sort[1][0] + ":\t" + str(sort[1][1]))
            return
        if len(sort) >= 1:
            print(sort[0][0] + ":\t" + str(sort[0][1]))
            return
    else:
        print("Liste leer!")
    
    
def compute_most_frequent_city_names_by_map(filename):
    """Zeile fuer Zeile einlesen, in Dictionary aufnehmen oder value erhoehen wenn bereits vorhanden.
    >>> compute_most_frequent_city_names_by_map("")
    Traceback (most recent call last):
        ...
    ValueError: No filename given

    >>> compute_most_frequent_city_names_by_map(5)
    Traceback (most recent call last):
        ...
    ValueError: Filename must be of type String
    
    >>> compute_most_frequent_city_names_by_map("test")
    End Of File
    Ortsname:   2
    Ortsname4:  1
    """
    if type(filename) != str:
        raise ValueError("Filename must be of type String")
    if len(filename) == 0:
        raise ValueError("No filename given")
    
    zfile = zipfile.ZipFile(filename + ".zip")
    file = zfile.open(filename + ".txt")   
    a_array = dict()
    string = read_info_from_file(file)
    while string != "-1":
        if string != "0":
            if string[:(string.find('\t'))].strip() in a_array:
                a_array[string[:(string.find('\t'))].strip()] += 1
            else:
                a_array[string[:(string.find('\t'))].strip()] = 1                
        string = read_info_from_file(file)
    print("End Of File")
    file.close()
    if len(a_array) > 0:
        sort = sorted(a_array.items(), key=operator.itemgetter(1), reverse=True)
        if len(sort) >= 3:
            print(sort[0][0] + ":\t" + str(sort[0][1]) + "\n" +  sort[1][0] + ":\t" + str(sort[1][1]) + "\n" + sort[2][0] + ":\t" + str(sort[2][1]))
            return
        if len(sort) >= 2:
            print(sort[0][0] + ":\t" + str(sort[0][1]) + "\n" +  sort[1][0] + ":\t" + str(sort[1][1]))
            # print(sort[0][0] + str(sort[0][1]) +  sort[1][0] + str(sort[1][1]))
            return
        if len(sort) >= 1:
            print(sort[0][0] + ":\t" + str(sort[0][1]))
            return
    else:
        print("Liste leer!")

    
def compute_most_frequent_city_names_with_DE_countrycode_by_sorting(filename):
    """Zeile fuer Zeile einlesen, array nach name durchsuchen und aufnehmen wenn nicht vorhanden oder value erhoehen wenn bereits vorhanden.
    speichert in 3d array ab (Name, Anzahl, Countrycode = DE), wertet nur solche aus, die auch min ein Mal den richtigen Countrycode haben
    
    """
    zfile = zipfile.ZipFile(filename + ".zip")
    file = zfile.open(filename + ".txt")    
    names = []
    string = read_info_from_file(file)
    while string != "-1":
        if string != "0":
            found = 0
            for i in range(0, len(names)):
                if names[i][0] == string[:(string.find('\t'))].strip():              
                    names[i][1] += 1
                    found = 1
                    if string[(string.find('\t')):].strip() == "DE":
                        names[i][2] = 1
                    
            if found == 0:
                names.append([])
                names[len(names)-1].append(string[:(string.find('\t'))].strip())
                names[len(names)-1].append(1)
                if string[(string.find('\t')):].strip() == "DE":
                    names[len(names)-1].append(1)
                else:
                    names[len(names)-1].append(-1)
        string = read_info_from_file(file)
    print("End Of File")
    file.close()
    if len(names) > 0:
        sort = sorted(names,key=lambda x: x[1], reverse = True)
        for j in range(0, len(sort)):
            if sort[j][2] == -1:
                sort.pop(j)    
        if len(sort) >= 3:
            print(sort[0][0] + ":\t" + str(sort[0][1]) + "\n" +  sort[1][0] + ":\t" + str(sort[1][1]) + "\n" + sort[2][0] + ":\t" + str(sort[2][1]))
            return
        if len(sort) >= 2:
            print(sort[0][0] + ":\t" + str(sort[0][1]) + "\n" +  sort[1][0] + ":\t" + str(sort[1][1]))
            return
        if len(sort) >= 1:
            print(sort[0][0] + ":\t" + str(sort[0][1]))
            return
    else:
        print("Liste leer!")


def compare_runtimes(filename):
    """Laufzeit berechnen mit cProfile

    """
    cProfile.runctx("compute_most_frequent_city_names_by_sorting(filename)", globals(),locals())
    cProfile.runctx("compute_most_frequent_city_names_by_map(filename)", globals(),locals())

    
if __name__ == "__main__":
    """Main routine

    """
    import doctest
    # doctest.testmod()
    compute_most_frequent_city_names_by_map("DE")
    # compute_most_frequent_city_names_by_sorting("DE")
    # compute_most_frequent_city_names_with_DE_countrycode_by_sorting("DE")
    # compare_runtimes("DE")
# <<< End of code
