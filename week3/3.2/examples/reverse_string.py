def omgekeerde_tekst(invoer_tekst):
    # Converteer de string naar een lijst van karakters
    karakter_lijst = list(invoer_tekst)
    
    # Gebruik twee pointers om de string ter plaatse om te keren
    links, rechts = 0, len(karakter_lijst) - 1
    while links < rechts:
        # Wissel karakters bij de pointers links en rechts
        karakter_lijst[links], karakter_lijst[rechts] = karakter_lijst[rechts], karakter_lijst[links]
        
        # Verplaats de pointers naar elkaar toe
        links += 1
        rechts -= 1
    
    # Converteer de lijst van karakters terug naar een string
    omgekeerde_tekst = ''.join(karakter_lijst)
    
    return omgekeerde_tekst

# Voorbeeldgebruik:
invoer_tekst = "Hallo, Wereld!"
omgekeerde_tekst = omgekeerde_tekst(invoer_tekst)
print("Oorspronkelijke Tekst:", invoer_tekst)
print("Omgekeerde Tekst:", omgekeerde_tekst)
