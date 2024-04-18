from concurrent.futures import ThreadPoolExecutor, as_completed  # Importa moduli per esecuzione parallela
import pandas as pd  # Importa pandas per la manipolazione dei dati
import requests  # Importa requests per le richieste HTTP
from bs4 import BeautifulSoup  # Importa BeautifulSoup per il parsing dell'HTML

# Leggi il file Excel
df = pd.read_excel('Imprese_Agricole_Italia_SitoWeb.xlsx')  # Legge il file Excel in un DataFrame
websites = list(df['Website'])  # Estrae i siti web dalla colonna 'Website'
websites = websites[0:200]  # Limita l'analisi ai primi 200 siti web

def check_website(website) -> (bool, str, int):
    """
    Controlla la presenza della parola "blockchain" nelle pagine del sito web.
    
    Args:
        website (str): URL del sito web da controllare.
        
    Returns:
        Tuple: Una tupla contenente un booleano per la presenza nella homepage,
        una stringa per l'URL della pagina contenente "blockchain" (se presente), e l'indice del sito nel DataFrame.
    """
    try:
        url = f'https://{website}'  # Costruisce l'URL corretto con il protocollo
        response = requests.get(url, timeout=60)  # Effettua una richiesta GET al sito web
        soup = BeautifulSoup(response.text, 'html.parser')  # Parsing dell'HTML
        
        # Controlla se "blockchain" è presente nella home page
        if 'blockchain' in soup.get_text().lower():
            return True, None, websites.index(website)
        
        # Trova tutti i link interni al sito
        links = list({link.get('href') for link in soup.find_all('a') if
                      link.get('href') and website in link.get('href') and
                      link.get('href') not in {f'https://{website}/', f'https://{website}/#'}})
        
        # Controlla ogni link interno per la presenza di "blockchain"
        for link in links:
            if not link.startswith("http"):
                link = f'https://{website}{link}'  # Costruisce l'URL completo per i link relativi
            response = requests.get(link, timeout=60)  # Effettua una richiesta GET per il link
            soup = BeautifulSoup(response.text, 'html.parser')  # Parsing dell'HTML
            if 'blockchain' in soup.get_text().lower():
                return True, link, websites.index(website)  # Ritorna True se "blockchain" è trovata in una pagina
        
        return False, None, websites.index(website)  # Ritorna False se "blockchain" non è trovata in nessuna pagina
    except Exception as e:
        print(f'Error checking website {website}: {e}')  # Gestisce eventuali eccezioni
        return False, None, websites.index(website)  # Ritorna False in caso di errore

# Esegui la verifica per ciascun sito web utilizzando ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(check_website, website): website for website in websites}  # Esegue il controllo per ciascun sito web
    for future in as_completed(futures):
        website = futures[future]  # Ottiene l'URL del sito web dal future
        result = future.result()  # Ottiene il risultato del controllo
        # Aggiorna il DataFrame con i risultati del controllo
        if result[0] and result[1] is None:
            df.at[result[2], 'blockchain nella Home Page (si/no)'] = 'si'
            df.at[result[2], 'blockchain in altre pagine (si/no)'] = ''
            df.at[result[2], 'Link altre pagine'] = ''
        elif result[0] and result[1] is not None:
            df.at[result[2], 'blockchain nella Home Page (si/no)'] = 'no'
            df.at[result[2], 'blockchain in altre pagine (si/no)'] = 'si'
            df.at[result[2], 'Link altre pagine'] = result[1]
        else:
            df.at[result[2], 'blockchain nella Home Page (si/no)'] = 'no'
            df.at[result[2], 'blockchain in altre pagine (si/no)'] = 'no'
            df.at[result[2], 'Link altre pagine'] = ''

# Salva il DataFrame in un nuovo file Excel
df.to_excel('Result_Imprese_Agricole_Italia_SitoWeb.xlsx', index=False)  # Salva il DataFrame aggiornato in un nuovo file Excel
