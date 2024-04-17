from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Leggi il file Excel
df = pd.read_excel('Imprese_Agricole_Italia_Sitoweb-xlsx')
websites = list(df['website'])
websites = websites[0:100]

def check_website(website) -> (bool, str, int):
    try:
        url = f'https://{website}'  # Correggi la costruzione dell'URL
        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.text, 'html.parser')

        if 'blockchain' in soup.get_text().lower():
            return True, None, websites.index(website)

        links = list({link.get('href') for link in soup.find_all('a') if
                      link.get('href') and website in link.get('href') and
                      link.get('href') not in {f'https://{website}/', f'https://{website}/#'}})

        for link in links:
            if not link.startswith("http"):
                link = f'https://{website}{link}'
            response = requests.get(link, timeout=60)
            soup = BeautifulSoup(response.text, 'html.parser')
            if 'blockchain' in soup.get_text().lower():
                return True, link, websites.index(website)

        return False, None, websites.index(website)
    except Exception as e:
        print(f'Error checking website {website}: {e}')
        return False, None, websites.index(website)

# Esegui la verifica per ciascun sito web
for website in websites:
    result = check_website(website)
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
df.to_excel('Imprese_Agricole_Italia_SitoWeb_Output.xlsx', index=False)
