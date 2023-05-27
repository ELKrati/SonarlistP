from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
import uuid
import whois
from datetime import datetime, date
from urllib.parse import urljoin
import nltk
import re
import json
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from urllib.parse import urljoin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from urllib.parse import urlparse
import tldextract
import itertools
from io import BytesIO
from PIL import Image
import random
import csv
from nameparser import HumanName
import datetime
from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests
import re
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import time
from socketIO_client import SocketIO, ConnectionError, TimeoutError
import socketio
from concurrent.futures import ThreadPoolExecutor
import phonenumbers

# from email_validator import validate_email, EmailNotValidError

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


# Function to get a random IP address
def get_random_ip():
    response = requests.get("https://api.proxyscrape.com/v2/account/datacenter_shared/proxy-list?auth=tvmrk73kgpxssjfsmrb2&type=displayproxies&country[]=all&protocol=http&format=json&status=online")
    
    if response.status_code == 200:
        ip_data = response.json()["data"]
        ip_list = [entry[0] for entry in ip_data]
        return random.choice(ip_list)
    else:
        raise Exception("API request failed with status code {}".format(response.status_code))
def extract_email_with_domain(data, domain):
    return [email for email in data if email.split('@')[-1] == domain]

def create_and_validate_emails(first_name, last_name, domain):
    return 'elkrati.ayoub@gmail.com'
    # # Lowercase the names.
    # first_name = first_name.lower()
    # last_name = last_name.lower()
    
    # # Create possible email addresses.
    # emails = [
    #     f"{first_name}@{domain}",
    #     f"{last_name}@{domain}",
    #     f"{first_name}.{last_name}@{domain}",
    #     f"{first_name}_{last_name}@{domain}",
    #     f"{first_name}{last_name}@{domain}",
    #     f"{first_name[0]}{last_name}@{domain}",
    #     f"{first_name[0]}.{last_name}@{domain}",
    #     f"{first_name[0]}_{last_name}@{domain}",
    #     f"{first_name}{last_name[0]}@{domain}",
    #     f"{first_name}.{last_name[0]}@{domain}",
    #     f"{first_name}_{last_name[0]}@{domain}",
    #     f"{first_name[0]}{last_name[0]}@{domain}",
    #     f"{last_name}{first_name}@{domain}",
    #     f"{last_name}.{first_name}@{domain}",
    #     f"{last_name}_{first_name}@{domain}",
    #     f"{last_name[0]}{first_name}@{domain}",
    #     f"{last_name[0]}.{first_name}@{domain}",
    #     f"{last_name[0]}_{first_name}@{domain}",
    #     f"{last_name}{first_name[0]}@{domain}",
    #     f"{last_name}.{first_name[0]}@{domain}",
    #     f"{last_name}_{first_name[0]}@{domain}",
    #     f"{last_name[0]}{first_name[0]}@{domain}",
    # ]

    # for email in emails:
    #     try:
    #         # Validate.
    #         validate_email(email)
    #         print(f"Email {email} is valid.")
    #         return email
    #     except EmailNotValidError:
    #         continue

    # return None
def send_message_to_socketio(message):
    try:
        sio.emit('message',message)
    except ConnectionError:
        print('The server is down. Try again later.')
    except TimeoutError:
        print('The server is taking too long to respond.')

        
def extract_ceo(domain):
    url = 'https://www.google.com/search?q=linkedin+ceo+of+{}&rlz=1C1GCEU_enUS832US832&oq=linkedin+ceo+of+{}&aqs=chrome.0.0l8.3029j0j7&sourceid=chrome&ie=UTF-8'.format(domain, domain)
    
    headers = {
    }
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

# Example usage

def extractceo_name(domain):
    ceo = extract_ceo(domain)
    print(f"CEO of {domain}: {ceo}")
    if ceo:
        names=HumanName(ceo)
        if names:
            return str(names)
        else:
            return "No data found"
    else :
        return None
    
def get_domain_name(url):
    # Parse the URL using urlparse
    if '://' not in url:
        if url.startswith("www."):
            domain_name = url[4:]
        return url
    else:
        parsed_url = urlparse(url)

        # Get the domain name from the parsed URL
        domain_name = parsed_url.netloc

        # Remove the leading "www." if present
        if domain_name.startswith("www."):
            domain_name = domain_name[4:]

        return domain_name
print(get_domain_name('https://facebook.com'))
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

def extract_favicon(url):
    send_message_to_socketio('Look for favicon in url.')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Look for favicon in link tags
    favicon_link = soup.find(lambda tag: tag.name == 'link' and ('icon' in tag.get('rel', []) or 'shortcut icon' in tag.get('rel', [])))

    if favicon_link:
        favicon_url = favicon_link['href']
    else:
        print(f"No favicon found on the website: {url}")
        return None

    favicon_url = urllib.parse.urljoin(url, favicon_url)
    return favicon_url

def download_favicon(favicon_url, output_dir):
    if favicon_url:
        favicon_name = os.path.basename(urllib.parse.urlsplit(favicon_url).path)
        output_path = os.path.join(output_dir, favicon_name)
        response = requests.get(favicon_url)
        if response.status_code == 200:
            favicon = Image.open(BytesIO(response.content))
            new_size = (256, 256)
            resized_favicon = favicon.resize(new_size)
            random_number = str(random.randint(100000, 999999))
            save_path = f"/Users/buropa/Desktop/Projects2023/crunchbase-scraper/sonarlistapis/media/logos/favicon-{random_number}.png"
            resized_favicon.save(save_path, "PNG")
            return f"/media/logos/favicon-{random_number}.png"
        else:
            print(f"Error downloading favicon: {response.status_code}")
    else:
        return None
        print("No favicon URL provided.")

def ensure_valid_url(url):
    if not url.startswith(('http://', 'https://')):
        # Assumes 'https' if no protocol is provided
        return f'https://{url}'
    return url

def check_url_availability(url):
    send_message_to_socketio('Checks if a URL is online and accessible.')
    """
    Checks if a URL is online and accessible.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is online and accessible, False otherwise.
    """
    try:
        response = requests.head(url, timeout=5)
        if response.status_code == requests.codes.ok:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def find_data_by_website_csv(search_website):
    file_path = '/Users/buropa/Downloads/free_company_dataset_2.csv'
    send_message_to_socketio('Extract Ceo email.')
    with open(file_path, 'r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        print('begin process read file csv company')
        for row in reader:
            website = row['website']
            if website == search_website:
                print(row)
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

def extract_meta_data(url):
    send_message_to_socketio('Extract the title')
    response = requests.get(url)
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

def get_logo_url(website_url):
    clearbit_url = f'https://logo.clearbit.com/{website_url}'
    send_message_to_socketio('Find the logo image using.')
    # Check if Clearbit has a valid logo
    response = requests.get(clearbit_url)
    if response.status_code == 200:
        return clearbit_url
    
    # If Clearbit does not have a logo, scrape the website for the logo
    try:
        response = requests.get(website_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the logo image using common tags and attributes
        logo_img = soup.find_all('img', {'class': ['logo', 'site-logo', 'brand-logo']})
        if not logo_img:
            logo_img = soup.find_all('img', {'alt': ['logo', 'site logo', 'brand logo']})
        if not logo_img:
            logo_img = soup.find_all('img', {'src': lambda src: 'logo' in src.lower()})
        
        # Check if the image name is equal to "logo"
        if not logo_img:
            logo_img = soup.find_all('img', {'src': lambda src: src.lower().endswith('/logo.png') or src.lower().endswith('/logo.jpg') or src.lower().endswith('/logo.jpeg') or src.lower().endswith('/logo.svg')})
        
        # If a logo image is found, return the absolute URL
        if logo_img:
            return urljoin(website_url, logo_img[0]['src'])
    except Exception as e:
        print(f"Error: {e}")
    
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

# Example usage:



def get_number_of_indexed_pages(website_url):
    search_url = f"https://www.google.com/search?q=site:{website_url}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            result_stats = soup.find("div", {"id": "result-stats"})
            if result_stats:
                num_results = result_stats.text.split()[1]
                return num_results
            else:
                print("Error: Unable to find result-stats element.")
                return None
        else:
            print(f"Error: Google search request failed with status code {response.status_code}")
            return None
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

# Example usage:
def extract_phone_numbers(url):
    # Extract the top 5 valid URLs of the website
    urls = extract_urls(url)
    urls = [url if url.startswith(('http://', 'https://')) else 'http://' + url.lstrip('/') for url in urls if not url.startswith('mailto:')]

    # Send a GET request to each URL and extract the content
    with ThreadPoolExecutor(max_workers=5) as executor:
        responses = list(executor.map(requests.get, urls))

    # Check if any phone numbers appear in the content of the URLs
    for url, response in zip(urls, responses):
        content = response.content
        text = content.decode('utf-8', 'ignore')
        for match in phonenumbers.PhoneNumberMatcher(text, "US"):
            number = phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164)
            try:
                parsed_number = phonenumbers.parse(number, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    print("Invalid phone number.")
                    if number.startswith('+1'):
                        number = number[2:]  # Remove the "+1"
                    print(f"Modified phone number: {number}")
                else:
                    print(f"Found number {number} at URL {url}")
                    return number  # Return the first number found
            except phonenumbers.phonenumberutil.NumberParseException:
                print("Invalid phone number.")
                continue

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

def extractNameCompany(domain):
    url = 'https://apps.growmeorganic.com/api-product/incoming-webhook/convert-company-names'
    payload = {
	"api_key": "Q6S6C5O6-A5T8E1D8-T6Q7P4J1-F4K2C3O7",
	"company_name" : domain
    }

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

import re

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

def load_industries_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        industries = [line.strip() for line in file.readlines()]
    return industries


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))

    # Tokenize and remove punctuation
    tokens = word_tokenize(text)
    words = [word.lower() for word in tokens if word.isalnum()]

    # Remove stop words
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)


def get_internal_links(soup, base_url):
    internal_links = []
    if soup.body:
        # Extract URLs from the body of the website
        for link in soup.body.find_all('a'):
            href = link.get('href')

            if href and not href.startswith('#') and not href.startswith('mailto:'):
                url = urljoin(base_url, href)
                if base_url in url and url not in internal_links:
                    internal_links.append(url)

        return internal_links[:5]

def extract_emails(url):
    # Initialize a set to store email addresses
    emails = set()
    # Send a GET request to the website
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all links on the page
    links = soup.find_all('a')
    # Loop through the links
    for link in links:
        href = link.get('href')
        # If the link contains 'mailto:' followed by an email address, extract the email address
        if href and href.startswith('mailto:'):
            email = href.split(':')[1]
            emails.add(email)
    # Find all email addresses in the page content using regex
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(pattern, str(response.content))
    # Add the email addresses to the set
    for match in matches:
        emails.add(match)
    return emails

def extract_emails_from_pages(url, num_pages=5):
    # Initialize a set to store email addresses
    all_emails = set()
    # Loop through the number of pages to scrape
    for i in range(num_pages):
        # Send a GET request to the page
        page_url = url + f'?page={i}'
        response = requests.get(page_url)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract email addresses from the page using the extract_emails function
        emails = extract_emails(page_url)
        # Add the email addresses to the set
        all_emails.update(emails)
    return all_emails


def extract_text_from_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.decompose()

    # Extract text from the remaining elements
    text = ' '.join(soup.stripped_strings)
    internal_links = get_internal_links(soup, url)

    return text, internal_links

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

def extract_urls(url):
    # Send a GET request to the website
    response = requests.get(url)
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all links on the page
    links = soup.find_all('a')
    # Extract the top 5 valid URLs
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
                # Break the loop if the top 5 valid URLs have been found
    return urls



def extract_company_email(url, company_name):
    # Extract the top 5 valid URLs of the website
    urls = extract_urls(url)
    urls = [url if url.startswith(('http://', 'https://')) else 'http://' + url.lstrip('/') for url in urls if not url.startswith('mailto:')]

    # Send a GET request to each URL and extract the content
    contents = []
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



def validate_email(email):
    # Check if the email address is valid
    try:
        result = validate_email(email, check_mx=True, verify=True)
        return result is not None
    except :
        return False
def match_industry(text, categories, top_n=3, min_matches=7):
    text_lower = text.lower()

    # Check for exact matches
    exact_matches = [category for category in categories if category.lower() in text_lower]

    if exact_matches:
        return exact_matches[:top_n]

    token_counts = Counter()

    # Tokenize text to consider partial matches
    tokens = set(word_tokenize(text_lower))

    for category in categories:
        words = set(word_tokenize(category.lower()))
        count = sum(1 for word in words if word in tokens)
        token_counts[category] = count

    matched_categories = [category for category, count in token_counts.most_common(top_n) if count >= min_matches]

    return matched_categories

def getIndustry(domain):
    csv_file = '/Users/buropa/Desktop/Projects2023/crunchbase-scraper/sonarlistapis/app/industries_unique.csv'
    industries = load_industries_from_csv(csv_file)
    text, internal_links = extract_text_from_webpage(domain)
    
    if internal_links is None:
        internal_links = []  # Set internal_links to an empty list if it's None
    
    internal_links = [link for link in internal_links if not link.endswith('.pdf')]
    
    # Scrape content from up to 5 internal URLs and accumulate the text
    for link in internal_links[:5]:
        print(f"Scraping content from: {link}")
        internal_text, _ = extract_text_from_webpage(link)
        text += ' ' + internal_text

    preprocessed_text = preprocess_text(text)
    matched_industries = match_industry(preprocessed_text, industries)
    return matched_industries
@api_view(['GET', 'POST'])
def index(request):
    if request.method == 'POST':
        data=request.POST
        domain=request.data["domain"]
        domain=domain.lower()
        valid_url = ensure_valid_url(domain)
        try:
            check_url_availability(valid_url)
        except:
            return JsonResponse(status=404)
        favicon_url = extract_favicon(valid_url)
        meta_title, meta_description = extract_meta_data(valid_url)
        if meta_description:
            meta_description=meta_description
        else:
            meta_description=meta_title
        logo_url = get_logo_url(valid_url)
        Social_media = get_data_from_api(valid_url)
        w = whois.whois(valid_url)
        city = w.city
        country = w.country
        print(w.creation_date)
        age = get_website_age(w.creation_date)
        send_message_to_socketio('Get website age')
        print(age)
        num_indexed_pages = get_number_of_indexed_pages(domain)
        send_message_to_socketio('Extract website indexed.')
        legal_infos=extract_legal_info(valid_url)
        send_message_to_socketio('Extraction of legal information.')
        phone_numbers = extract_phone_numbers(valid_url)
        send_message_to_socketio('Extract phone number.')
        api=extractRS(valid_url)
        email_address=""
        company_name=""
        company_name=extract_company_name(meta_title,valid_url)
        industry=""
        industry=getIndustry(valid_url)
        CEO_name=""
        CEO_email=""
        c_linkedin=""
        c_twitter=""
        c_facebook=""
        url = 'http://localhost:3000/api/createsocity'
        headers = {'Content-type': 'application/json'}
        if isinstance(industry, list):
            industry_str = ','.join(industry)
        else:
            industry_str = industry
        email_address=extract_company_email(valid_url,company_name)
        if isinstance(email_address, list):
            email_address_str = ','.join(email_address)
        else:
            email_address_str = email_address
        if api:
            if api['state']==True:
                print(api['data'])
                # if api['data']['title']:
                #     company_name=extract_company_name(api['data']['title'])
                c_linkedin=api['data']['linkedin_username']
                c_twitter=api['data']['twitter_username']
                c_facebook=api['data']['facebook_username']
                if not phone_numbers:
                    phone_numbers=api['data']['phones']
                if api['data']['company_email']!="":
                    email_address_str=api['data']['company_email']
                    # if email_address_str:
                    #     emails = email_address_str.split(',')
                    #     valid_emails = []
                    #     for email in emails:
                    #         try:
                    #             # Validate the email address
                    #             result = validate_email(email.strip())
                    #             if result:
                    #                 valid_emails.append(email.strip())
                    #             # Add the email to the list of valid emails
                    #         except :
                    #             # The email address is not valid
                    #             pass
                    #     valid_email_string = ', '.join(valid_emails)
                    email_address_str=email_address_str
                print(api)
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
        if logo_url:
            logo_url=logo_url
        else:
            logo_url='http://127.0.0.1:8000'+download_favicon(favicon_url, '/Users/buropa/Desktop/Projects2023/crunchbase-scraper/sonarlistapis/media/logos')
        domain_csv=get_domain_name(valid_url)
        CEO_name=extractceo_name(domain_csv)
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
        domain_name=get_domain_name(valid_url)
        if len(CEO_name.split())>1:
            if CEO_email:
                CEO_email=CEO_email
            else:
                create_and_validate_emails(CEO_first_name,CEO_last_name,domain_name)
            data = find_data_by_website_csv(domain_csv)
        if data:
            print(data)
            company_name=data['name']
            industry_str=data['industry']
            city=data['locality']
            country=data['country']
            if data['linkedin']:
                linkedin_url = data['linkedin'].strip()
                url_parts = linkedin_url.split('/')
                c_linkedin=url_parts[-1]
                print(c_linkedin)
                send_message_to_socketio('Please be patient, you will receive your result in a few moments :)')
        if company_name not in domain_name:
            # If not, extract the company name from the domain name
            company_name = domain_name.split('.')[0]
            print(domain_name.split('.')[0])

        response_data={"company_name":company_name.capitalize() if company_name else company_name,"url": valid_url, "meta-title": meta_title, "meta-description": meta_description,"logo":logo_url,"rs":Social_media,"country":country.capitalize() if country else country,"city":city.capitalize() if city else city,"age":age,"Nbr_pages_index":num_indexed_pages,"legal_infos":legal_infos,"phone_numbers":phone_numbers,"industry":industry_str,"email":email_address_str,"CEO":CEO_name,"Email":CEO_email,"c_linkedin":c_linkedin,"c_twitter":c_twitter,"c_facebook":c_facebook,"employees":extractemployes}
        data = json.dumps(response_data)
        response = requests.post(url, data=data, headers=headers)
        return JsonResponse(response.json(), safe=False)
    else :
        return HttpResponse(status=401)


print(extractceo_name('Uprigs.com'))

