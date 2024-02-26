from collections import deque

# Initialisatie van de deque
mijn_deque = deque()

# Gegevens toevoegen aan de deque
mijn_deque.append(10)
mijn_deque.append(20)
mijn_deque.append(30)

# Gegevens ophalen en weergeven
print("Inhoud van de deque:")
for item in mijn_deque:
    print(item)

# Gegevens verwijderen vanaf de linkerzijde van de deque
verwijderd_item = mijn_deque.popleft()
print(f"\nVerwijderd item vanaf de linkerzijde: {verwijderd_item}")

# Nieuwe gegevens toevoegen aan de deque
mijn_deque.appendleft(5)

# Gegevens ophalen en weergeven na toevoeging aan de linkerzijde
print("\nInhoud van de deque na toevoeging aan de linkerzijde:")
for item in mijn_deque:
    print(item)
