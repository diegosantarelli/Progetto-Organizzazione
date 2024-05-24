import pandas as pd
import matplotlib.pyplot as plt

# Carica il file Excel
df = pd.read_excel('Result_Imprese_Agricole_Italia_SitoWeb.xlsx')

# Conta i siti con blockchain nella homepage
homepage_counts = df['blockchain nella Home Page (si/no)'].value_counts().reindex(['no', 'si', 'errore'])

# Funzione per creare grafico a barre con limiti sull'asse Y e etichette
def create_bar_chart(data, title, xlabel, ylabel, y_limit=None):
    if data.empty:
        print(f"No data to plot for {title}.")
        return
    
    fig, ax = plt.subplots(figsize=(10, 6))
    data.plot(kind='bar', ax=ax, color=['red', 'green', 'blue'])  # Aggiungi il colore blu per gestire tre categorie

    ax.set_title(title, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=20)
    ax.set_ylabel(ylabel, fontsize=20)
    ax.tick_params(axis='both', which='major', labelsize=18)
    ax.tick_params(axis='x', rotation=0)
    
    # Imposta i limiti sull'asse Y
    if y_limit is not None:
        ax.set_ylim(0, y_limit)
    else:
        ax.set_ylim(0, data.max() * 1.1)  # Imposta un limite relativo al massimo valore
    
    # Aggiungi etichette ai valori delle barre
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='bottom', 
                    xytext=(0, 9), 
                    textcoords='offset points',
                    fontsize=14)

    plt.tight_layout()
    plt.show()

# Funzione per creare grafico a torta con dimensioni dei font personalizzate
def create_pie_chart(data, title):
    if data.empty:
        print(f"No data to plot for {title}.")
        return
    
    plt.figure(figsize=(8, 8))
    data.plot(kind='pie', autopct='%1.1f%%', colors=['red', 'green', 'blue'], fontsize=25)  # Aggiungi il colore blu per gestire tre categorie
    plt.title(title, fontsize=18)
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

# Creare grafico a barre per blockchain nella homepage con limiti
create_bar_chart(homepage_counts, 'Siti con Blockchain nella Homepage', 'Presenza Blockchain', 'Conteggio', y_limit=homepage_counts.max()*1.1)

# Creare grafico a torta per blockchain nella homepage
create_pie_chart(homepage_counts, 'Siti con Blockchain nella Homepage')
