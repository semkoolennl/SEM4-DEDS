
tekst = "Hallo, dit is een voorbeeldtekst."

# String weergeven
print("Oorspronkelijke tekst:", tekst)

# Append aan de string
tekst += " Dit is toegevoegde tekst."
print("Na appenden:", tekst)

# String vervangen
vervangende_tekst = "een ander stukje tekst"
tekst = tekst.replace("voorbeeldtekst", vervangende_tekst)
print("Na vervangen:", tekst)

# Substring verwijderen
te_verwijderen_substring = "Dit is "
tekst = tekst.replace(te_verwijderen_substring, "")
print("Na verwijderen van substring:", tekst)

# Lengte van de string
lengte = len(tekst)
print("Lengte van de tekst:", lengte)

# Hoofdletters omzetten
tekst = tekst.upper()
print("Na omzetten naar hoofdletters:", tekst)

# Kleinletters omzetten
tekst = tekst.lower()
print("Na omzetten naar kleine letters:", tekst)
