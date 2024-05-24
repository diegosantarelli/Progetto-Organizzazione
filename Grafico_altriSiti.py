import pandas as pd
import matplotlib.pyplot as plt

# Carica il file Excel
df = pd.read_excel('Result_Imprese_Agricole_Italia_SitoWeb.xlsx')

# Conta i siti con blockchain nella homepage
homepage_counts = df['blockchain nella Home Page (si/no)'].value_counts().reindex(['no', 'si', 'errore'])

# Conta i siti con blockchain in altre pagine
link_counts = df['blockchain in altre pagine (si/no)'].value_counts().reindex(['no', 'si', 'errore'])

# Conta i siti che danno errore
error_counts = df['errore'].value_counts().reindex(['si', 'no']) if 'errore' in df.columns else pd.Series([0, 0], index=['si', 'no'])

# Funzione per creare grafici a barre con limiti sull'asse Y e etichette
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

# Funzione per creare grafici a torta con dimensioni dei font personalizzate
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

# Creare grafico a barre per blockchain in altre pagine con limiti specifici
create_bar_chart(link_counts, 'Siti con Blockchain in Altre Pagine', 'Presenza Blockchain in Altre Pagine', 'Conteggio', y_limit=link_counts.max()*1.1)

# Creare grafico a torta per blockchain in altre pagine
create_pie_chart(link_counts, 'Siti con Blockchain in Altre Pagine')
