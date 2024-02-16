## Selecteren van rijen, kolommen
```python
.loc[]
```

1 kolom alle rijen -> pd.Serie
```python
.loc[:, 'kolomnaam']
```

meerdere kolommen -> pd.DataFrame
```python
.loc[:, ['naam', 'woonplaats']]
```

### Selecteren van rijen
!! Eerst een boolean serie maken voor selectie uit rij
vb:
```python
is_leiden = medewerker["woonplaats"] == 'Leiden'
medewerker.loc[(woonplaats_is_leiden), :]
```


### Boolean checks
Logische operatoren bij .loc:
```python
AND = &
OR  = |
NOT = ~
XOR = ^
```

NOT NULL kan met: .isna()
IS NULL kan met:  .notna()
```python
heeft_baas = medewerker['baas'].isna()
geen_baas  = medewerker['baas'].notna()
```

String waarde ophalen met hulp van .str
```python
begins_s = medewerker["naam"].str[0] == "S"
has_s    = medewerker["naam"].str.contains("s")
```

## Unieke waarden selecteren
.drop_duplicates()

```python
medewerker.loc[:, ['woonplaats']].drop_duplicates('woonplaats')
```


## Aggregratie functies
.count() op een DataFrame telt alle ingevulde rijen per kolom
```python
medewerker.count()
```

Group By + count
```python
medewerker.groupby('woonplaats', as_index = False)['nr'].count()
```

SUM
```python
medewerker.groupby('woonplaats', as_index=False)['uurloon'].sum()
```

### Aggregate
Met de .agg() functie kan je meerdere functies uitvoeren op een resultaten-set die elk een apparte kolom toevoegd

!! Average heeft numpy nodig !!
```python
import numpy as np
medewerker.groupby('woonplaats', as_index=False)['uurloon'].agg([sum, np.mean])
```

## Merging columns
### Horizontal merging
neem de volgende 2 DataFrames:
medewerker = ['nr', 'naam', 'functie']
functie    = ['id', 'uurloon', 'code']
```python
pd.merge(medewerker, functie, left_on="functie", how="inner", right_on="code")
```

of met Indicator:
```python
pd.merge(medewerker, functie, left_on="functie", how="outer", right_on="code", indicator=True)
```
Geeft een _merge kolom mee die aangeeft waar de Private Key voorkomt: left_only | right_only | both

### Vertical merging
axis = 0: row based
axis = 1: column based
```python
pd.concat([medewerker1, medewerker2], axis=0)
```


## Iterating over DataFrames + selectie op row index
```python
for index, row in medewerker.iterrows():
    huidig_uurloon = medewerker.at[index, 'uurloon']
```
