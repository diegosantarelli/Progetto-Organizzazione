from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import requests
from bs4 import BeautifulSoup
import PyPDF2

# Leggi il file Excel
dataframe = pd.read_excel('Imprese_Agricole_Italia_SitoWeb.xlsx')
websites = list(dataframe['Website'])
partite_iva = list(dataframe['Partita IVA'])
websites = websites[0:100]
partite_iva = partite_iva[0:100]

def search_keyword_in_pdf(url, keyword):
    try:
        with open(url, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                if keyword.lower() in page.extract_text().lower():
                    return True
        return False
    except Exception as e:
        print(f'Error searching keyword in PDF: {e}')
        return False

def check_website(partita_iva) -> (bool, str, int):
    index = partite_iva.index(partita_iva)
    website = websites[index]
    print(index)

    try:
        # Tenta la connessione con HTTPS
        url = f'http://{website}'
        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if 'blockchain' in soup.get_text().lower():
            return True, None, partite_iva.index(partita_iva)
        
        links = {
            f'http://{link.get("href").rsplit("http://")[-1]}'
            if 'http://' in link.get('href') else
            f'http://{link.get("href").rsplit("http://")[-1]}'
            if 'http://' in link.get('href') else
            f'http://{website}{link.get("href")}'
            if (website not in link.get('href') and not link.get('href').startswith('http') and not link.get(
                'href').startswith('www') and len(link.get('href').split('.')) <= 2) and not website.startswith(
                'http') else
            f'{website}{link.get("href")}' if (website not in link.get('href') and not link.get('href').startswith(
                'http') and not link.get('href').startswith('www') and len(
                link.get('href').split('.')) <= 2) and website.startswith('http') else
            link.get('href') for link in soup.find_all('a')
            if link.get('href') and
               (website in link.get('href') or (
                       website not in link.get('href') and not link.get('href').startswith('http') and not link.get(
                   'href').startswith('www') and len(link.get('href').split('.')) <= 2)) and
               link.get('href') not in {
                   f'http://{website}',
                   f'http://{website}/',
                   f'http://{website}/#'
               } and 'tel:' not in link.get('href') and 'javascript' not in link.get(
                'href') and 'mailto:' not in link.get('href') and not link.get(
                'href').endswith('.mp4') and not link.get('href').endswith('.mp3') and not link.get('href').endswith(
                '.jpg') and not link.get('href').endswith('.jpeg') and not link.get('href').endswith(
                '.png') and not link.get('href').endswith('.gif') and not link.get('href').endswith(
                '.svg') and not link.get('href').endswith('.tiff') and not link.get('href').endswith(
                '.bmp') and not link.get('href').endswith('.ico') and not link.get('href').endswith('.webp')
        }

        for link in links:
            if not link.startswith("http"):
                link = f'http://{website}{link}'
            if link.endswith('.pdf'):
                if search_keyword_in_pdf(link, 'blockchain'):
                    return True, link, partite_iva.index(partita_iva)
            else:
                response = requests.get(link, timeout=60)
                soup = BeautifulSoup(response.text, 'html.parser')
                if 'blockchain' in soup.get_text().lower():
                    return True, link, partite_iva.index(partita_iva)
        
        return False, None, partite_iva.index(partita_iva)

    except Exception as e:
            print(f'Error checking website {website}: {e}')
            return None, None, partite_iva.index(partita_iva)

# Assicurati che le colonne abbiano il tipo di dato corretto
dataframe['blockchain nella Home Page (si/no)'] = dataframe['blockchain nella Home Page (si/no)'].astype(str)
dataframe['blockchain in altre pagine (si/no)'] = dataframe['blockchain in altre pagine (si/no)'].astype(str)
dataframe['Link altre pagine'] = dataframe['Link altre pagine'].astype(str)

# Utilizza ThreadPoolExecutor per eseguire le richieste HTTP in parallelo
with ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(check_website, partita_iva) for partita_iva in partite_iva]
    for future in as_completed(futures):
        result = future.result()
        if result[0] and result[1] is None:
            dataframe.at[result[2], 'blockchain nella Home Page (si/no)'] = 'si'
            dataframe.at[result[2], 'blockchain in altre pagine (si/no)'] = ''
            dataframe.at[result[2], 'Link altre pagine'] = ''
        elif result[0] and result[1] is not None:
            dataframe.at[result[2], 'blockchain nella Home Page (si/no)'] = 'no'
            dataframe.at[result[2], 'blockchain in altre pagine (si/no)'] = 'si'
            dataframe.at[result[2], 'Link altre pagine'] = result[1]
        elif result[0] is None and result[1] is None:
            dataframe.at[result[2], 'blockchain nella Home Page (si/no)'] = 'errore'
            dataframe.at[result[2], 'blockchain in altre pagine (si/no)'] = ''
            dataframe.at[result[2], 'Link altre pagine'] = ''
        else:
            dataframe.at[result[2], 'blockchain nella Home Page (si/no)'] = 'no'
            dataframe.at[result[2], 'blockchain in altre pagine (si/no)'] = 'no'
            dataframe.at[result[2], 'Link altre pagine'] = ''

# Salva il DataFrame in un nuovo file Excel
dataframe.to_excel('Result_Imprese_Agricole_Italia_SitoWeb.xlsx', index=False)
