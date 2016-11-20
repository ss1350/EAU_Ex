def isort(unsortiert):
    """Sort a list of objects using the insertion sort algorithm.

    Some longer description here ...
    """

    if not type(unsortiert) == list:
        return "Fehler: Eingabe muss eine Liste sein"
    if len(unsortiert) == 0:
        # return "Fehler: Liste leer"

        # An empty list can be defined as "sorted"
        # -> Just return the passed empty list
        return unsortiert

    sortiert = [0]
    sortiert[0] = unsortiert[0]

    for i in unsortiert[1:]:
        # Erster Wert bereits in Liste uebernommen
        pos = 0
        while pos < len(sortiert):
            if i > sortiert[pos]:
                if pos == len(sortiert) - 1:
                    # Liste am Ende und noch nicht einsortiert: hinten anhängen
                    sortiert.insert(pos + 1, i)
                    break
                else:
                    # Wert an Position ist kleiner, weitersuchen
                    pos += 1
            elif i <= sortiert[pos]:
                # Wert an Position ist größer/gleich, vorher einsetzen,
                # dann loop beenden und mit neuem i starten
                sortiert.insert(pos, i)
                break

    return(sortiert)


def ll():
    liste = []
    if isort(liste) != [] \
            or isort(1) != ("Fehler: Eingabe muss eine Liste sein"):
        print("Test \"leere Liste/falsches Format\" nicht bestanden")
    else:
        print("Test \"leere Liste/falsches Format\" bestanden")


def td():
    liste = [50, 50, 12, 46, 46, 55]
    if isort(liste) != [12, 46, 46, 50, 50, 55]:
        print("Test \"doppelte Werte/Doppelter erster Wert\" nicht bestanden")
    else:
        print("Test \"doppelte Werte/Doppelter erster Wert\" bestanden")


def tv():
    liste = [1, 2, 3, 4, 5, 6]
    if isort(liste) != [1, 2, 3, 4, 5, 6]:
        print("Test \"vorsortierte Liste\" nicht bestanden")
    else:
        print("Test \"vorsortierte Liste\" bestanden")


def ug():
    listeg = [5, 8, 9, 45, 11, 22]
    listeug = [5, 8, 9, 45, 11, 22, 11]
    if isort(listeg) != [5, 8, 9, 11, 22, 45] \
            or isort(listeug) != [5, 8, 9, 11, 11, 22, 45]:
        print("Test \"gerade/ungerade Anzahl\" nicht bestanden")
    else:
        print("Test \"gerade/ungerade Anzahl\" bestanden")


def el():
    liste = [2, 5, 6, 9, 8, 5, 22, 15, 48, 32, 546]
    if (len(isort(liste)) != len(liste)):
        print("Test \"Ergebnisliste gleich lang wie Eingangsliste\" nicht bestanden")
    else:
        print("Test \"Ergebnisliste gleich lang wie Eingangsliste\" bestanden")


def at():
    ll()
    td()
    tv()
    ug()
    el()


print("Anleitung:\n"
      "isort(unsortiert) : sortiert unsortierte Liste mit insertion sort\n"
      "ll()          : Testet isort(unsortiert) auf eine leere Liste oder falsches Eingabeformat\n"
      "td()          : Testet isort(unsortiert) mit einer Liste mit doppelten Werten\n"
      "tv()          : Testet isort(unsortiert) mit einer vorsortierten Liste\n"
      "ug()          : Testet isort(unsortiert) mit gerader/ungerader Anzahl an Elementen in der Liste\n"
      "el()          : Testet isort(unsortiert) auf gleiche Länge Eingabe - Erebnis\n"
      "at()          : Alle Tests durchführen")
