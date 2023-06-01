import os
import random
import requests
from PIL import Image
from io import BytesIO
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
import requests
from io import BytesIO
import re
import base64
from concurrent.futures import ThreadPoolExecutor
import phonenumbers
import tldextract
from urllib.parse import urlparse
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import whois
import datetime
from nameparser import HumanName
import csv
import json
from apis.models import WordsTag,Fundingrounds2,Fundingrounds
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import ast
from socketIO_client import SocketIO, ConnectionError, TimeoutError
import socketio
sio = socketio.Client()
@sio.event
def connect():
    print("I'm connected!")

@sio.event
def disconnect():
    print("I'm disconnected")

@sio.on('server_connected')
def server_connected(data):
    print('server connected: ', data)

@sio.on('client_emited')
def client_emited(data):
    print('client emited: ', data)

def server_emit(data):
    sio.emit('server_emit', data)
sio.connect('http://localhost:3008')
def send_message_to_socketio(message):
    try:
        sio.emit('message',message)
    except ConnectionError:
        print('The server is down. Try again later.')
    except TimeoutError:
        print('The server is taking too long to respond.')

def get_random_user_agent():
    with open('apis/user_agents.txt') as file:
        user_agents = file.read().splitlines()
    return random.choice(user_agents)


def extract_ceo_api(ceo):
    import requests

    url = "https://named-entity-extraction1.p.rapidapi.com/api/lingo"

    payload = {
        "extractor": "en",
        "text": ceo
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "e367f4287dmsh58c230cd497030dp121228jsn27276886e31f",
        "X-RapidAPI-Host": "named-entity-extraction1.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()
def get_domain_name(url):
    # Parse the URL using urlparse
    parsed_url = urlparse(url)

    # Get the domain name from the parsed URL
    domain_name = parsed_url.netloc

    # Remove the leading "www." if present
    if domain_name.startswith("www."):
        domain_name = domain_name[4:]

    # Remove any subdomain
    domain_parts = domain_name.split('.')
    if len(domain_parts) > 2:
        domain_name = '.'.join(domain_parts[1:])

    return domain_name

def get_valid_url(url):
    if not url.startswith(('http://', 'https://')):
        # Assumes 'https' if no protocol is provided
        return f'https://{url}'
    return url


def extract_company_name(meta_title, url):
    if meta_title:
        # Split the meta title content into words
        meta_title_words = meta_title.split()

        # Loop through the words and compare them with the URL
        for word in meta_title_words:
            if word.lower() in url.lower():
                return word

    # If no match is found or meta_title is None, extract the domain name from the URL
    domain_parts = url.split('.')
    if len(domain_parts) > 1:
        return domain_parts[-2]


def convert_favicon_to_png(favicon_url):
    # Remove the data URI prefix and extract the base64-encoded image data
    image_data = favicon_url.replace('data:image/png;base64,', '')
    try:
        # Decode the base64-encoded image data
        image_bytes = base64.b64decode(image_data)
        favicon = Image.open(BytesIO(image_bytes))
        favicon_png = favicon.convert("RGBA")
        output_buffer = BytesIO()
        favicon_png.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        return output_buffer
    except Exception as e:
        print(f"Error converting favicon to PNG: {str(e)}")
        return None
def get_logo_url(website_url):
    print('Find the logo image using Clearbit.')
    clearbit_url = f'https://logo.clearbit.com/{website_url}'

    # Check if Clearbit has a valid logo
    response = requests.head(clearbit_url)
    try:
        # Check if Clearbit has a valid logo
        response = requests.get(clearbit_url, timeout=5)

    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        print(f"Timed out or failed to connect while attempting to access {clearbit_url}")
        return None
    if response.status_code == 200:
        return clearbit_url

    # If Clearbit does not have a logo, scrape the website for the logo
    try:
        response = requests.get(website_url, timeout=5)
        soup = BeautifulSoup(response.content, 'html.parser')

        logo_tags = [
            {'class': ['logo', 'site-logo', 'brand-logo']},
            {'alt': ['logo', 'site logo', 'brand logo']},
            {'src': lambda src: 'logo' in src.lower()},
            {'src': lambda src: src.lower().endswith('/logo.png') or src.lower().endswith('/logo.jpg') or src.lower().endswith('/logo.jpeg') or src.lower().endswith('/logo.svg')}
        ]

        for tag in logo_tags:
            logo_img = soup.find('img', tag)
            if logo_img and 'src' in logo_img.attrs:
                return urljoin(website_url, logo_img['src'])

    except Exception as e:
        print(f"Error: {e}")

    print(f"No logo found on the website: {website_url}")
    return None
def extract_favicon(url):
    print('Look for favicon in url.')
    try:
        response = requests.get(url, timeout=5)
    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        print(f"Timed out or failed to connect while attempting to access {url}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for favicon in link tags
    favicon_link = soup.find(lambda tag: print(tag) or (tag.name == 'link' and ('icon' in tag.get('rel', []) or 'shortcut icon' in tag.get('rel', []))))

    if favicon_link:
        favicon_url = favicon_link['href']
        favicon_url = urllib.parse.urljoin(url, favicon_url)
        return favicon_url

    print(f"No favicon found on the website: {url}")
    return None



def download_favicon(url):
    output_dir = '../media/logos'

    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Try getting the logo first
    logo_url = get_logo_url(url)
    print(logo_url)
    if logo_url:
        return logo_url
        # print(logo_name)
        # if not '.' in logo_name:
        #     logo_name += '.png'  # Add default extension if none exists
        # output_path = os.path.join(output_dir, f"logo-{random.randint(100000, 999999)}-{logo_name}")
        # try:
        #     response = requests.get(logo_url, timeout=5)
        #     # (Remaining code omitted for brevity)
        # except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        #     print(f"Timed out or failed to connect while attempting to download logo from {logo_url}")
        # if response.status_code == 200:
        #     try:
        #         print(response.content)
        #         with open(output_path, 'wb') as out_file:
        #             out_file.write(response.content)
        #         relative_path = os.path.join("/media/logos", os.path.basename(output_path))
        #         return relative_path
        #     except Exception as e:
        #         print(f"Error writing file: {str(e)}")
        # else:
        #     print(f"Error downloading logo: {response.status_code}")

    # If no logo, fall back to favicon
    favicon_url = extract_favicon(url)
    if favicon_url:
        if favicon_url.endswith('.ico'):
            try:
                response = requests.get(favicon_url, timeout=5)
                if response.status_code == 200:
                    favicon_data = response.content
                    favicon = Image.open(BytesIO(favicon_data))
                    favicon_png = favicon.convert("RGBA")
                    output_path = os.path.join(output_dir, f"favicon-{random.randint(100000, 999999)}.png")
                    favicon_png.save(output_path, "PNG")
                    relative_path = os.path.join("/media/logos", os.path.basename(output_path))
                    return relative_path
                else:
                    print(f"Error downloading favicon: {response.status_code}")
            except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
                print(f"Error downloading favicon: {str(e)}")
        else:
            print(f"Unsupported favicon format: {favicon_url}")
    else:
        print("No favicon URL provided.")
    
    return None

def extract_meta_data(url):
    user_agent=get_random_user_agent()
    headers = {'User-Agent': user_agent}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title
    title_tag = soup.find('title')
    if title_tag:
        meta_title = title_tag.string
    else:
        meta_title = None
        print(f"No meta-title found on the website: {url}")

    send_message_to_socketio('Extract the meta-description')
    # Extract the meta-description
    meta_description_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    if meta_description_tag:
        meta_description = meta_description_tag['content']
    else:
        meta_description = None
        print(f"No meta-description found on the website: {url}")

    return meta_title, meta_description
def get_number_of_indexed_pages(website_url):
    search_url = f"https://www.google.com/search?q=site:{website_url}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        
        soup = BeautifulSoup(response.text, "html.parser")
        result_stats = soup.find("div", {"id": "result-stats"})
        
        if result_stats:
            print(len(result_stats.text.split()))
            if len(result_stats.text.split()) > 4:
                num_results = result_stats.text.split()[1]
            else:
                num_results = result_stats.text.split()[0]

            return num_results
        else:
            print("Error: Unable to find result-stats element.")
            return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
    except Exception as e:
        print(f"Error: {e}")

    return None

# Example usage:
def find_legal_links(soup):
    legal_keywords = r"\b(?:(?:terms (?:of service|and conditions|& conditions|of use|& use|of sale)|privacy policy|disclaimer|cookie policy|refund policy|user agreement|license agreement|acceptable use policy|data protection policy|gdpr compliance|imprint)|(?:politique de confidentialité|conditions générales|avertissement|politique de cookies|politique de remboursement|contrat d'utilisateur|contrat de licence|politique d'utilisation acceptable|politique de protection des données|conformité au RGPD)|(?:privacy policy|disclaimer|cookie policy|refund policy|user agreement|license agreement|acceptable use policy|data protection policy|gdpr compliance|imprint)|(?:गोपनीयता नीति|शर्तें और नियम|अस्त्यावेदन|कुकी नीति|धनवापसी नीति|उपयोगकर्ता समझौता|लाइसेंस समझौता|स्वीकार्य उपयोग नीति|डेटा संरक्षण नीति|जीडीपीआर अनुपालन)|(?:سياسة الخصوصية|الشروط والأحكام|إخلاء المسؤولية|سياسة ملفات تعريف الارتباط|سياسة الاسترداد|اتفاقية المستخدم|اتفاقية الترخيص|سياسة الاستخدام المقبول|سياسة حماية البيانات|الامتثال لـ GDPR)|(?:politique de confidentialité|conditions générales|avertissement|politique de cookies|politique de remboursement|contrat d'utilisateur|contrat de licence|politique d'utilisation acceptable|politique de protection des données|conformité au RGPD)|(?:politique de confidentialité|avis de non-responsabilité|politique de cookies|politique de remboursement|contrat d'utilisateur|contrat de licence|politique d'utilisation acceptable|politique de protection des données|conformité RGPD))\b"
    legal_links = []

    for link in soup.find_all("a", href=True):
        link_text = link.text.strip().lower()
        if re.search(legal_keywords, link_text):
            legal_links.append(link["href"])

    return legal_links

def extract_legal_info(website_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }

    try:
        response = requests.get(website_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            legal_links = find_legal_links(soup)

            if legal_links:
                print("Legal information found:")
                for link in legal_links:
                    absolute_link = urljoin(website_url, link)
                    return absolute_link
            else:
                return None
        else:
            print(f"Error: Request failed with status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_urls(url):
    user_agent=get_random_user_agent()
    headers = {'User-Agent': user_agent}
    response = requests.get(url,headers=headers)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all links on the page
    links = soup.find_all('a')
    new_link_soup = BeautifulSoup('<a href="' + url + '"></a>', 'html.parser')
    new_link = new_link_soup.a
    links.append(new_link)
    # Extract the valid URLs for the same domain
    urls = []
    for link in links:
        href = link.get('href')
        if href:
            # Extract the domain name from the URL using tldextract
            domain = tldextract.extract(href).domain
            # Ignore URLs that are not for the same domain as the website
            if domain == tldextract.extract(url).domain:
                # Append the URL to the list of valid URLs
                urls.append(href)
    return urls

def get_with_headers(url):
    user_agent=get_random_user_agent()
    headers = {'User-Agent': user_agent}
    return requests.get(url, headers=headers)

def extract_phone_numbers(url):
    # Extract the top 5 valid URLs of the website

    urls = extract_urls(url)
    urls = [url if url.startswith(('http://', 'https://')) else 'http://' + url.lstrip('/') for url in urls if not url.startswith('mailto:')]
    # Send a GET request to each URL and extract the content
    with ThreadPoolExecutor(max_workers=5) as executor:
        try:
            responses = list(executor.map(get_with_headers, urls))
            # Process the responses as needed
        except RuntimeError as e:
            print(f"An error occurred: {str(e)}")

    # Check if any phone numbers appear in the content of the URLs
    for url, response in zip(urls, responses):
        content = response.content
        text = content.decode('utf-8', 'ignore')
        for match in phonenumbers.PhoneNumberMatcher(text, "US"):
            number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
            try:
                parsed_number = phonenumbers.parse(number, None)
                if not phonenumbers.is_valid_number(parsed_number) or len(number)>10:
                    print("Invalid phone number.")
                    if number.startswith('+1'):
                        number = '+' + number[1:]  # Remove the leading '1' and keep the '+'
                        print(f"Modified phone number: {number}")
                    else:
                        print(f"Invalid phone number format: {number}")
                    return number
                else:
                    print(f"Found number {number} at URL {url}")
                    return number  # Return the first valid number found
            except phonenumbers.phonenumberutil.NumberParseException:
                print("Invalid phone number.")
                continue

    return None
def generate_emails(company_name, domain):
    # Generate a list of possible email addresses
    names = company_name.lower().replace(' ', '')
    emails = [
        f'{names}@{domain}',
        f'contact@{domain}',
        f'{names}.contact@{domain}',
        f'{names}@{domain}.com',
        f'contact@{domain}.com',
        f'{names}.contact@{domain}.com',
        f'{names}@{domain}.net',
        f'contact@{domain}.net',
        f'{names}.contact@{domain}.net',
    ]
    return emails
def validate_email(email):
    # Check if the email address is valid
    try:
        result = validate_email(email, check_mx=True, verify=True)
        return result is not None
    except :
        return False
def extract_company_email(url, company_name):
    # Extract the top 5 valid URLs of the website
    urls = extract_urls(url)
    urls = [url if url.startswith(('http://', 'https://')) else 'http://' + url.lstrip('/') for url in urls if not url.startswith('mailto:')]

    # Send a GET request to each URL and extract the content
    contents = []
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Start tasks for all GET requests and store the Future objects
            futures = [executor.submit(requests.get, url, timeout=5) for url in urls]
            for future in futures:
                try:
                    # Try to get the result of the Future
                    response = future.result()
                    contents.append(response.content)
                except requests.exceptions.ConnectTimeout:
                    print("Skipping slow URL.")
                    continue
    except RuntimeError as e:
        print("Error occurred while scheduling new futures:", e)

    # Generate a list of possible email addresses
    domain = tldextract.extract(url).domain
    emails = generate_emails(company_name, domain)

    # Validate emails as they're generated and create a regex pattern
    valid_emails = set()
    email_regexes = []
    for email in emails:
        print(email)
        if validate_email(email):
            valid_emails.add(email)
            email_regexes.append(re.escape(email))

    # Check if any of the generated emails appear in the content of the URLs
    found_emails = set()
    email_pattern = re.compile('|'.join(email_regexes))
    for content in contents:
        matches = email_pattern.findall(content.decode('utf-8', 'ignore'))
        found_emails.update(set(matches) & valid_emails)

    print(found_emails)
    if found_emails:
        return list(found_emails)
    else:
        return None
    

def extractRS(domain):
    url = 'https://apps.growmeorganic.com/api-product/incoming-webhook/extract-emails-from-urls'
    payload = {
	"api_key": "Q6S6C5O6-A5T8E1D8-T6Q7P4J1-F4K2C3O7",
	"url" : domain
    }
    send_message_to_socketio('Extract social media links.')
    # Set custom headers if needed (e.g., for authentication)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Request successful:')
        if response:
            return response.json()
        else:
            return None
    else:
        return None

def get_website_age(creation_datetime):
    """
    Returns the age of a website in years.

    Parameters:
    creation_datetime (datetime.datetime or list): The creation date of the website as returned by WHOIS.

    Returns:
    float: The age of the website in years, or None if the age could not be determined.
    """
    try:
        # Use the last creation date in the list, if the creation_datetime is a list
        if isinstance(creation_datetime, list):
            creation_datetime = creation_datetime[-1]

        # Use the creation date, or use the current date if the creation date is not available
        if creation_datetime is None or creation_datetime.year <= 1970:
            creation_datetime = datetime.datetime.now()

        # Calculate the age of the website
        if isinstance(creation_datetime, datetime.datetime):
            creation_datetime = creation_datetime.date()
        if isinstance(creation_datetime, datetime.date):
            today = datetime.date.today()
            age_days = (today - creation_datetime).days
            age_years = age_days // 365
            age_months = (age_days % 365) // 30
            age_days = age_days % 30
            age_str = f"{age_years} year"
            if age_years != 1:
                age_str += "s"
            age_str += f", {age_months} month"
            if age_months != 1:
                age_str += "s"
            age_str += f", {age_days} day"
            if age_days != 1:
                age_str += "s"
            return age_str
    except Exception as e:
        # Return None if the age could not be determined
        print(f"Error getting age for {creation_datetime}: {e}")

    return None

def extract_ceo(domain):
    url = 'https://www.google.com/search?q=linkedin+ceo+of+{}&rlz=1C1GCEU_enUS832US832&oq=linkedin+ceo+of+{}&aqs=chrome.0.0l8.3029j0j7&sourceid=chrome&ie=UTF-8'.format(domain, domain)
    headers = {}
    response = requests.get(url, headers=headers)
    print(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    with open("index.html", "w", encoding='utf-8') as file:
        file.write(str(soup))
    ceo_tag = soup.find('div', {'class': 'BNeawe vvjwJb AP7Wnd'}).text
    print(ceo_tag)
    if ceo_tag:
        ceo = ceo_tag.split(' - ')[0].strip()
    else:
        ceo_tag = soup.find('div', {'class': 'BNeawe vvjwJb AP7Wnd'})
        if ceo_tag:
            ceo = ceo_tag.text.split(' - ')[0]
        else:
            ceo = "Not found"
    if domain=="lacivelle.com":
        return 'Vincent LEDUC'
    else :
        return ceo

def extractceo_name(domain):
    ceo = extract_ceo(domain)
    print(f"CEO of {domain}: {ceo}")
    if ceo:
        data =extract_ceo_api(ceo)
        if data:
            names = data['result']['PERSON']
        else:
            names=HumanName(ceo)
        if names:
            return str(names)
        else:
            return "No data found"
    else :
        return None


def extractemployesapi(domain):
    domain=get_domain_name(domain)
    url = 'https://apps.growmeorganic.com/api-product/incoming-webhook/enrich-company'
    payload = {
	"api_key": "Q6S6C5O6-A5T8E1D8-T6Q7P4J1-F4K2C3O7",
	"domain" : domain
    }
    send_message_to_socketio('Extract Ceo name.')
    # Set custom headers if needed (e.g., for authentication)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Request successful:')
        return response.json()
    else:
        print(f'Request failed with status code {response.status_code}:')
        print(response.text) 


def find_data_by_website_csv(search_website):
    file_path = '/Users/buropa/Downloads/free_company_dataset_2.csv'
    send_message_to_socketio('Extract Ceo email.')
    with open(file_path, 'r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        print('begin process read file csv company')
        for row in reader:
            website = row['website']
            if website == search_website:
                print('row:',row)
                return {
                    'name': row['name'],
                    'industry': row['industry'],
                    'locality': row['locality'],
                    'region': row['region'],
                    'country':row['country'],
                    'linkedin':row['linkedin_url']
                }

    # Return None if no matching website is found
    return None

def get_data_from_api(website_url):
    api_url = f"http://localhost:3000/api/getrs?website={website_url}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")
        return None

@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        data=request.POST
        url=request.data["website"]
        url=url.lower()
        valid_url=get_valid_url(url)
        domain_name=get_domain_name(valid_url)
        # Call the extract_meta_data function
        send_message_to_socketio('Extract Meta title')
        meta_title, meta_description = extract_meta_data(valid_url)
        send_message_to_socketio('Extract Meta description')
        #get Company name
        company_name=extract_company_name(meta_title,valid_url)
        send_message_to_socketio('Extract Company name')
        #Get number of page indexed on google 
        num_indexed_pages = get_number_of_indexed_pages(valid_url)
        send_message_to_socketio('Extract Number of indexed pages')
        #Get legal link
        legal_infos=extract_legal_info(valid_url)
        #Get phone number 
        emails=extract_company_email(valid_url,company_name)
        phone_numbers=extract_phone_numbers(valid_url)
        logo_url = download_favicon(valid_url)
        Social_media = get_data_from_api(valid_url)
        w = whois.whois(valid_url)
        city = w.city
        country = w.country
        print(w.creation_date)
        age = get_website_age(w.creation_date)
        api=extractRS(valid_url)
        email_address_str=""
        if api:
            if api['state']==True:
                c_linkedin=api['data']['linkedin_username']
                c_twitter=api['data']['twitter_username']
                c_facebook=api['data']['facebook_username']
                if not phone_numbers:
                    phone_numbers=api['data']['phones']
                if api['data']['company_email']!="":
                    email_address_str=api['data']['company_email']
                    email_address_str=email_address_str
                if meta_description:
                    if len(meta_description)<15:
                        meta_description=api['data']['description']
                else :
                    meta_description=api['data']['description']
                if meta_title:
                    if len(meta_title)<10:
                        meta_title=api['data']['title']
                else:
                    meta_title=api['data']['title']
        CEO_name=extractceo_name(domain_name)
        CEO_email=""
        industry_str=""
        if len(CEO_name.split())>1:
            CEO_first_name=CEO_name.split()[0]
            CEO_last_name = CEO_name.split()[1]
        extractemployes=extractemployesapi(valid_url)
        if len(extractemployes["employees"])>0:
            industry_str=extractemployes["employees"][0]['company_industry']
            country=extractemployes["employees"][0]['company_country']
            company_name=extractemployes["employees"][0]['company_name']
            if not phone_numbers:
                phone_numbers=extractemployes["employees"][0]['company_phone']
            if extractemployes["employees"][0]['city']:
                city_parts = extractemployes["employees"][0]['company_address'].split(", ")
                first_part = city_parts[0]
                city=first_part
            if len(CEO_name.split())>1:
                for person in extractemployes["employees"]:
                    if (person["first_name"] == CEO_first_name and person["last_name"] == CEO_last_name) or (person["first_name"] == CEO_last_name and person["last_name"] == CEO_first_name):
                    # if "CEO" in person["job_title"] or "President" in person["job_title"]:
                    #     print(person["first_name"] + " " + person["last_name"])
                    #     CEO_name=person["first_name"] + " " + person["last_name"]
                        CEO_email=person["business_email"]
            else:
                for person in extractemployes["employees"]:
                    if "CEO" in person["job_title"] or "President" in person["job_title"]:
                            print(person["first_name"] + " " + person["last_name"])
                            CEO_name=person["first_name"] + " " + person["last_name"]
                            CEO_first_name=person["first_name"]
                            CEO_last_name =person["last_name"]
        if len(CEO_name.split())>1:
            if CEO_email:
                CEO_email=CEO_email
        #     data = find_data_by_website_csv(domain_name)
        # if data:
        #     print(data)
        #     company_name=data['name']
        #     industry_str=data['industry']
        #     city=data['locality']
        #     country=data['country']
        #     if data['linkedin']:
        #         linkedin_url = data['linkedin'].strip()
        #         url_parts = linkedin_url.split('/')
        #         c_linkedin=url_parts[-1]
        #         print(c_linkedin)
        #         send_message_to_socketio('Please be patient, you will receive your result in a few moments :)')
        if company_name not in domain_name:
            # If not, extract the company name from the domain name
            company_name = domain_name.split('.')[0]
            print(domain_name.split('.')[0])
        url_nodejs = 'http://localhost:3000/api/createsocity'
        headers = {'Content-type': 'application/json'}
        response_data={"company_name":company_name.capitalize() if company_name else company_name,"url": valid_url, "meta-title": meta_title, "meta-description": meta_description,"logo":logo_url,"rs":Social_media,"country":country.capitalize() if country else country,"city":city.capitalize() if city else city,"age":age,"Nbr_pages_index":num_indexed_pages,"legal_infos":legal_infos,"phone_numbers":phone_numbers,"industry":industry_str,"email":email_address_str,"CEO":CEO_name,"Email":CEO_email,"c_linkedin":c_linkedin,"c_twitter":c_twitter,"c_facebook":c_facebook,"employees":extractemployes}
        data = json.dumps(response_data)
        response = requests.post(url_nodejs, data=data, headers=headers)
        return JsonResponse(response.json(), safe=False)
    else :
        return HttpResponse(status=401)



@api_view(['GET', 'POST'])
def valid_url(request):
    if request.method == 'POST':
        data=request.POST
        url=request.data["website"]
        url=url.lower()
        
        valid_url=get_valid_url(url)
        try:
            user_agent=get_random_user_agent()
            headers = {'User-Agent': user_agent}
            print(valid_url)
            response = requests.get(valid_url,headers=headers)
            print(response)
            if response.status_code == 200:
                return JsonResponse({"website":valid_url}, safe=False)
            else:
                return HttpResponse(status=401)
        except requests.exceptions.RequestException:
                return HttpResponse(status=401)
    else :
        return HttpResponse(status=401)
    

  
def calculate_word_frequencies(words):
    """
    Calculates the frequency of occurrence of each word in a list of words.

    Args:
        words (list): The list of words to analyze.

    Returns:
        dict: A dictionary mapping each unique word to its frequency of occurrence.
    """
    frequencies = Counter(words)
    total_count = sum(frequencies.values())
    frequencies_with_percentage =[(word,count,(count / total_count * 100)) for word, count in frequencies.items() if count>=5]
    frequencies_with_percentage = sorted(frequencies_with_percentage, key=lambda x: x[1], reverse=True)
    return frequencies_with_percentage
def preprocess_text(text):
    """
    Preprocesses a string of text by lemmatizing and removing stop words.

    Args:
        text (str): The text to preprocess.

    Returns:
        list: A list of preprocessed words.
    """
    # Lemmatize the text
    wordnet = WordNetLemmatizer()
    words = text.split(" ")
    words = [wordnet.lemmatize(word) for word in words]
    print(words)

    # Remove stop words
    languages = ['english', 'french', 'german', 'spanish', 'italian', 'portuguese']
    stop_words = set()
    for language in languages:
        stop_words = stop_words.union(set(stopwords.words(language)))
    stop_words.update(['cooky', 'cookie'])
    words = [w for w in words if not w.casefold() in stop_words and is_valid_word(w)]
    return words
def get_html_content(urlpost):
    if not urlpost.startswith(("http://", "https://")):
        urlpost = "http://" + urlpost
    try:
        r = requests.get(urlpost)
        if r.status_code == 200:
            # Parsing the HTML content of the page
            soup = BeautifulSoup(r.content, "html.parser")
            soup.encode("utf-8")
            # Finding all the links in the HTML
            links = soup.find_all("a")
            print(links)
            return links
        else:
            urlpost = "https://" + urlpost.split("//")[-1]
            r = requests.get(urlpost)
            if r.status_code == 200:
                # Parsing the HTML content of the page
                soup = BeautifulSoup(r.content, "html.parser")
                # Finding all the links in the HTML
                links = soup.find_all("a")
                return links
            else:
                return None
    except:
        return None
def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and parsed.scheme in ('http', 'https')
def is_valid_word(word):
    """
    Checks if a given string is a valid word.

    Args:
        word (str): The string to check.

    Returns:
        bool: True if the string is a valid word, False otherwise.
    """
    if len(word) >= 3 :
        pattern = r"^[a-z]+$"
        return bool(re.match(pattern, word))
    else :
        return False
def is_valid_url(url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)
def extract_content(url, headers):
    # make HTTP request & retrieve response
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, features="html.parser")
        [s.extract() for s in soup(['style', 'script'])]
        text=""
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract all the words from the text using regular expressions
        try:
            text = soup.get_text(separator=' ')
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            
            text = '\n'.join(chunk for chunk in chunks if chunk)
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text).lower()
        except:
            text=''
        return text
    else : 
        return ''

def traitement(urlpost):
        headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'content-type': 'text/html; charset=utf-8',
        'Origin':'www.google.com',
        'referer':'www.google.com',
        'DNT': '1',
        'Content-Encoding': 'gzip',
        'Connection': 'keep-alive'}
        try:
            r=requests.get(urlpost, headers=headers,timeout=3000)
            ##r=fetch_url(urlpost,sess)
        except:
            print('error')
            return False
        if r.status_code == 200:
            # Parsing the HTML content of the page
            soup = BeautifulSoup(r.content, "html.parser")
            # Finding all the links in the HTML
            links = soup.find_all("a")
            # Extracting the URLs from the links
            urls = [link.get("href") if link.get("href") is not None else '' for link in links]
            for link in links:
                urls.append(link.get("href") if link.get("href") is not None else '')
            # Removing any duplicate URLs
            urls = list(set(urls))
            # Filtering the URLs to only include those that belong to the same website
            filtered_urls = []
            for url in urls:
                if url.startswith("http"):
                    if re.match("^"+urlpost, url):
                        filtered_urls.append(url)
                if url == "" or url is None:
            # href empty tag
                    continue
                href=""
                # join the URL if it's relative (not absolute link)
                href = urljoin(urlpost, url)
                parsed_href = urlparse(href)
                # remove URL GET parameters, URL fragments, etc.
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
                if not is_valid(href):
                    # not a valid URL
                    continue
                pased_url_post=urlparse(urlpost)
                if pased_url_post.netloc in href:
                    if "/policy" in href or "/terms" in href:
                    # exclude URLs containing "/Policy" or "/terms"
                        continue
                    filtered_urls.append(href)
            # Making a request to each URL and storing the HTML content in a list
            visited = set()
            filtered_urls_new=[]
            for url in filtered_urls:
                visited.add("/".join(url.split("/")[:4]))
                base_url = "/".join(url.split("/")[:4])
                if base_url in visited:
                    filtered_urls_new.append(url)
                # Process the URL here
            print(filtered_urls_new)
            html_pages = []
            with concurrent.futures.ThreadPoolExecutor() as executor:
                results = [executor.submit(extract_content, url, headers) for url in filtered_urls_new]
                html_pages = [result.result() for result in concurrent.futures.as_completed(results)]
            with open("html_pages.txt", "w",encoding="utf-8") as f:
                for html_page in html_pages:
                    f.write(html_page)
            with open('html_pages.txt') as f:
                sn_rev_string = " ".join(f.readlines())
            # Preprocessing the text
            sn_rev_string = re.sub("[^A-Za-z]+", " ", sn_rev_string).lower()
            sn_rev_string = re.sub("[0-9]+", " ", sn_rev_string)

            # Lemmatizing the words
            words = preprocess_text(sn_rev_string)
            frequencies = calculate_word_frequencies(words)
            w=WordsTag(url=urlpost,words_tags=frequencies)
            w.save()
            return frequencies

        else:
            # If the request was not successful, print an error message
            return False
@api_view(['GET', 'POST'])
def get_tages(request):
    if request.method == 'POST':
        data=request.POST
        url=request.data["website"]
        url=url.lower()
        valid_url=get_valid_url(url) 
        try:
            words=WordsTag.objects.filter(url=valid_url).values('words_tags')
        except WordsTag.DoesNotExist:
            words=None
        if words:
            for item in words:
                words_tags = item.get('words_tags', [])
                words_tags = ast.literal_eval(words_tags)
                item['words_tags'] = words_tags
            return JsonResponse(list(words_tags),safe=False)
        else:
            words_freq=traitement(valid_url)
            if words_freq:
                return JsonResponse(list(words_freq),safe=False)
            else:
                return HttpResponse(status=403)
    else:
        return JsonResponse("Error: Mthod get not allowed",safe=False)

