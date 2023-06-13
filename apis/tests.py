import re
from rest_framework.decorators import api_view
import requests
from urllib.parse import urlparse
from django.http import JsonResponse, HttpResponse
from PIL import Image
import requests
from io import BytesIO
import os
import random
import urllib.parse
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime
import whois
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=3)
session.mount('http://', adapter)
session.mount('https://', adapter)
session.verify = False
def get_random_ip():
    response = requests.get("https://api.proxyscrape.com/v2/account/datacenter_shared/proxy-list?auth=tvmrk73kgpxssjfsmrb2&type=displayproxies&country[]=all&protocol=http&format=json&status=online")
    
    if response.status_code == 200:
        ip_data = response.json()["data"]
        ip_list = [entry[0] for entry in ip_data]
        return random.choice(ip_list)
    else:
        raise Exception("API request failed with status code {}".format(response.status_code))
def get_valid_url(url):
    url_validity = r'(https?|ftp|file)://[-A-Za-z0-9\+&@#/%?=~_|!:,.;]*[-A-Za-z0-9\+&@#/%=~_|]'
    if re.match(url_validity, url):
        return url
    else:
        if not url.startswith(('http://', 'https://')):
        # Assumes 'https' if no protocol is provided
            return f'https://{url}'
    return url

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
def extractRS(domain):
    url = 'https://apps.growmeorganic.com/api-product/incoming-webhook/extract-emails-from-urls'
    payload = {
	"api_key": "Q6S6C5O6-A5T8E1D8-T6Q7P4J1-F4K2C3O7",
	"url" : domain
    }
    # Set custom headers if needed (e.g., for authentication)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print('Request successful:')
        try:
            data = response.json()
            print(data)
            return data
        except ValueError:
            return None
    else:
        return None
def extract_infos(valid_url):
    url_api="https://api.apollo.io/v1/organizations/enrich"
    domain_name=get_domain_name(valid_url)
    querystring = {
    "api_key": "B8UzzHy5VnKLg0oKowUt2A",
    "domain": domain_name
    }
    headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json'
    }
    response = requests.request("GET", url_api, headers=headers, params=querystring)
    if response.status_code == 200:
        print('Request successful:')
        try:
            data = response.json()
            print(data)
            return data
        except ValueError:
            return None
    else:
        return None
def extract_favicon(url):
    print('Look for favicon in url.')
    try:
        response = session.get(url, timeout=5)
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
def get_logo_url(website_url):
    print('Find the logo image using Clearbit.')
    clearbit_url = f'https://logo.clearbit.com/{website_url}'

    # Check if Clearbit has a valid logo
    response = requests.head(clearbit_url)
    try:
        # Check if Clearbit has a valid logo
        response = session.get(clearbit_url, timeout=5)

    except (requests.exceptions.Timeout, requests.exceptions.RequestException):
        print(f"Timed out or failed to connect while attempting to access {clearbit_url}")
        return None
    if response.status_code == 200:
        return clearbit_url

    # If Clearbit does not have a logo, scrape the website for the logo
    try:
        response = session.get(website_url, timeout=5)
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
        #     response = session.get(logo_url, timeout=5)
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
                response = session.get(favicon_url, timeout=5)
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

 
def find_legal_links(soup):
    legal_keywords = re.compile(r"\b(?:(?:terms (?:of service|and conditions|& conditions|of use|& use|of sale)|privacy policy|disclaimer|mentions légales|cookie policy|refund policy|user agreement|license agreement|acceptable use policy|data protection policy|gdpr compliance|imprint)|(?:politique de confidentialité|conditions générales|avertissement|politique de cookies|politique de remboursement|contrat d'utilisateur|contrat de licence|politique d'utilisation acceptable|politique de protection des données|conformité au RGPD)|(?:privacy policy|disclaimer|cookie policy|refund policy|user agreement|license agreement|acceptable use policy|data protection policy|gdpr compliance|imprint)|(?:गोपनीयता नीति|शर्तें और नियम|अस्त्यावेदन|कुकी नीति|धनवापसी नीति|उपयोगकर्ता समझौता|लाइसेंस समझौता|स्वीकार्य उपयोग नीति|डेटा संरक्षण नीति|जीडीपीआर अनुपालन)|(?:سياسة الخصوصية|الشروط والأحكام|إخلاء المسؤولية|سياسة ملفات تعريف الارتباط|سياسة الاسترداد|اتفاقية المستخدم|اتفاقية الترخيص|سياسة الاستخدام المقبول|سياسة حماية البيانات|الامتثال لـ GDPR)|(?:politique de confidentialité|conditions générales|avertissement|politique de cookies|politique de remboursement|contrat d'utilisateur|contrat de licence|politique d'utilisation acceptable|politique de protection des données|conformité au RGPD)|(?:politique de confidentialité|avis de non-responsabilité|politique de cookies|politique de remboursement|contrat d'utilisateur|contrat de licence|politique d'utilisation acceptable|politique de protection des données|conformité RGPD))\b")
    legal_links = []
    for link in soup.find_all("a", href=True):
        link_text = link.text.strip().lower()
        if legal_keywords.search(link_text):  # use the precompiled regex
            legal_links.append(link["href"])

    return legal_links

def extract_legal_info(website_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }
    ip=get_random_ip()
    print(ip)
    session.proxies = {
                'http': 'http://'+ip,
                'https': 'http://'+ip
    }
    try:
        response = session.get(website_url, headers=headers)
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

def extract_meta_data(url):
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract the title
    title_tag = soup.find('title')
    print(title_tag)
    if title_tag:
        meta_title = title_tag.string
    else:
        meta_title = None
        print(f"No meta-title found on the website: {url}")

    # Extract the meta-description
    meta_description_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    if meta_description_tag:
        meta_description = meta_description_tag['content']
    else:
        meta_description = None
        print(f"No meta-description found on the website: {url}")

    return meta_title, meta_description

@api_view(['GET','POST'])
def get_informations_website(request):
    session=requests.session()
    ip=get_random_ip()
    print(ip)
    session.proxies = {
                'http': 'http://'+ip,
                'https': 'http://'+ip
    }
    if request.method == 'POST':
        data=request.POST
        url=request.data["website"]
        url=url.lower()
        valid_url=get_valid_url(url) 

        c_linkedin=""
        c_twitter=""
        c_facebook=""
        meta_description=""
        meta_title=""
        meta_description,meta_title=extract_meta_data(valid_url)
        email_address_str=""
        phone_number=""
        industry=""
        city=""
        country=""
        name=""
        logo_url = download_favicon(valid_url)
        w = whois.whois(valid_url)
        age = get_website_age(w.creation_date)
        legal_infos=extract_legal_info(valid_url)
        industry=""
        try:
            api=extractRS(valid_url)
            if api:
                if api['state']==True:
                    c_linkedin=api['data']['linkedin_url']
                    c_twitter=api['data']['twitter_url']
                    c_facebook=api['data']['facebook_url']
                    if not meta_title:
                        meta_title=api['data']['title']
                    phone_number=api['data']['phones']
                    if not meta_description:
                        meta_description =api['data']['description']
                    if api['data']['company_email']!="":
                        email_address_str=api['data']['company_email']
            else:
                pass
        except:
            pass
        try:
            api2=extract_infos(valid_url)
            if api2:
                if len(api2) != 0:
                    print('hello')
                    if not c_linkedin:
                        c_linkedin=api2['organization']['linkedin_url']
                    if not c_twitter:
                        c_twitter=api2['organization']['twitter_url']
                    if not c_facebook:
                        c_facebook=api2['organization']['facebook_url']
                    phone_number=api2['organization']['phone']
                    industry=api2['organization']['industry']
                    city=api2['organization']['city']
                    country=api2['organization']['country']
                    name=api2['organization']['name']
            else:
                pass
        except:
            pass
        response_data={"company_name":name.capitalize() if name else name,"url": valid_url, "meta-title": meta_title, "meta-description": meta_description,"logo":logo_url,"country":country.capitalize() if country else country,"city":city.capitalize() if city else city,"phone_numbers":phone_number,"email":email_address_str,"c_linkedin":c_linkedin,"c_twitter":c_twitter,"c_facebook":c_facebook,"website_age":age
                       ,"privacy_link":legal_infos,"industry":industry
                       }
        print(response_data)
        return JsonResponse(response_data, safe=False)
    else :
        return HttpResponse(status=401)