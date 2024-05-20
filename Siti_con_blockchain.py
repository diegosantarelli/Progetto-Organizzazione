import pandas as pd

# Carica il file Excel
df = pd.read_excel('Result_Imprese_Agricole_Italia_SitoWeb.xlsx')

# Filtra il DataFrame per visualizzare solo le righe con "si" nella colonna desiderata
Homepage_con_blockchain = df[df['blockchain nella Home Page (si/no)'] == 'si']
Link_con_blockchain = df[df['blockchain in altre pagine (si/no)'] == 'si']

# Conta i siti con "si" nella colonna "blockchain nella Home Page (si/no)"
count_homepage = Homepage_con_blockchain['Website'].count()
count_link = Link_con_blockchain['Website'].count()

# Visualizza i siti con "si" nella colonna "blockchain nella Home Page (si/no)"
print("Siti con blockchain nella Home Page:", count_homepage)
print(Homepage_con_blockchain[['Website']])

# Visualizza i siti con "si" nella colonna "blockchain in altre pagine (si/no)" insieme ai link e all'indice
print("Siti con blockchain in altre pagine:", count_link)
for index, row in Link_con_blockchain.iterrows():
    print(f"{index}, SITO: {row['Website']}, LINK: {row['Link altre pagine']}")
