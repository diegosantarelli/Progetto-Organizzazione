import pandas as pd
import matplotlib.pyplot as plt

# Carica il file Excel
df = pd.read_excel('Result_Imprese_Agricole_Italia_SitoWeb.xlsx')

# Conta i siti con blockchain nella homepage
homepage_counts = df['blockchain nella Home Page (si/no)'].value_counts()

# Conta i siti con blockchain in altre pagine
link_counts = df['blockchain in altre pagine (si/no)'].value_counts()

# Conta i siti che danno errore
error_counts = df['Errore'].value_counts() if 'Errore' in df.columns else pd.Series([0, 0], index=['si', 'no'])

# Funzione per creare grafici a barre con limiti sull'asse Y e etichette
def create_bar_chart(data, title, xlabel, ylabel, filename, y_limit=None):
    ax = data.plot(kind='bar', color=['green', 'red'], figsize=(10, 6))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=0)
    
    # Imposta i limiti sull'asse Y se specificati
    if y_limit is not None:
        plt.ylim(0, y_limit)
    
    # Aggiungi etichette ai valori delle barre
    for i in ax.containers:
        ax.bar_label(i)
    
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

# Funzione per creare grafici a torta
def create_pie_chart(data, title, filename):
    data.plot(kind='pie', autopct='%1.1f%%', colors=['green', 'red'], figsize=(8, 8))
    plt.title(title)
    plt.ylabel('')  # Nasconde l'etichetta dell'asse Y
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()

# Creare grafico a barre per blockchain nella homepage con limiti
create_bar_chart(homepage_counts, 'Siti con Blockchain nella Homepage', 'Presenza Blockchain', 'Conteggio', 'bar_homepage_blockchain.png', y_limit=homepage_counts.max()*1.1)

# Creare grafico a torta per blockchain nella homepage
create_pie_chart(homepage_counts, 'Siti con Blockchain nella Homepage', 'pie_homepage_blockchain.png')

# Creare grafico a barre per blockchain in altre pagine con limiti
create_bar_chart(link_counts, 'Siti con Blockchain in Altre Pagine', 'Presenza Blockchain in Altre Pagine', 'Conteggio', 'bar_link_blockchain.png', y_limit=link_counts.max()*1.1)

# Creare grafico a torta per blockchain in altre pagine
create_pie_chart(link_counts, 'Siti con Blockchain in Altre Pagine', 'pie_link_blockchain.png')

# Creare grafico a barre per siti che danno errore con limiti (se la colonna esiste)
if 'Errore' in df.columns:
    create_bar_chart(error_counts, 'Siti che danno Errore', 'Errore', 'Conteggio', 'bar_error.png', y_limit=error_counts.max()*1.1)
    create_pie_chart(error_counts, 'Siti che danno Errore', 'pie_error.png')
