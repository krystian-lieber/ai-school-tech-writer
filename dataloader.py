import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from utility import download_url_to_file

data_dir=os.getenv("DATA_DIR", "data")
characteristics_directory = f'{data_dir}/characteristics'

def download_charasteristic(product):
    characteristics_url = product.get('charakterystyka')
    product_id = product.get('id')
    filename = f'{characteristics_directory}/charakterystyka_{product_id}.pdf'
    
    download_url_to_file(characteristics_url, filename)
   

def main():
    url = 'https://rejestry.ezdrowie.gov.pl/api/rpl/medicinal-products/public-pl-report/4.0.0/overall.xml'
    xml_file_path = 'data/Rejestr_Produktow_Leczniczych_calosciowy.xml'   
    download_url_to_file(url, xml_file_path)

    
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
    namespace = {'ns': 'http://rejestry.ezdrowie.gov.pl/rpl/eksport-danych-v4.0.0'}
    
    if not os.path.exists(characteristics_directory):
        os.makedirs(characteristics_directory)
    
    products = root.findall('ns:produktLeczniczy', namespace)
    
    progress_bar = tqdm(total=len(products), unit='file', desc='Downloading files')
    
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_charasteristic, product) for product in products]
        
        for future in as_completed(futures):
            if future.result():
                progress_bar.update(1)
    
    progress_bar.close()
    
    print('Finished downloading and saving PDF files.')


if __name__ == '__main__':
    load_dotenv()
    main()