# Een lege dictionary aanmaken
mijn_dict = {}

# Gegevens toevoegen aan de dictionary
mijn_dict['naam'] = 'John Doe'
mijn_dict['leeftijd'] = 25
mijn_dict['stad'] = 'Amsterdam'

# Gegevens ophalen uit de dictionary
print("Naam:", mijn_dict['naam'])
print("Leeftijd:", mijn_dict['leeftijd'])
print("Stad:", mijn_dict['stad'])

# Gegevens wijzigen in de dictionary
mijn_dict['leeftijd'] = 26

# Gegevens opnieuw ophalen na wijziging
print("Gewijzigde leeftijd:", mijn_dict['leeftijd'])

# Controleren of een sleutel bestaat in de dictionary
if 'gewicht' in mijn_dict:
    print("Gewicht:", mijn_dict['gewicht'])
else:
    print("Gewicht is niet beschikbaar in de dictionary.")

data = [
    {'naam': 'Alice', 'leeftijd': 25},
    {'naam': 'Bob', 'leeftijd': 30},
    {'naam': 'Charlie', 'leeftijd': 20}
]

# Sorteer de lijst van dictionaries op basis van leeftijd
gesorteerde_data = sorted(data, key=lambda x: x['leeftijd'])

# Toon de gesorteerde lijst
print(gesorteerde_data)

