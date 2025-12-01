# networksecurity/utils/main_utils/feature_extraction.py

import re
import socket
import ssl
import requests
import tldextract
import whois
from bs4 import BeautifulSoup
from datetime import datetime
import dns.resolver

# ---------- Config ----------
REQUEST_TIMEOUT = 6
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) PyChecker/1.0"}
SHORTENERS_REGEX = re.compile(r"(bit\.ly|tinyurl\.com|goo\.gl|ow\.ly|t\.co|is\.gd|buff\.ly|adf\.ly)")

# ---------- Basic URL Features ----------
def having_IP_Address(url):
    return 1 if re.match(r'http[s]?://\d+\.\d+\.\d+\.\d+', url) else 0

def URL_Length(url):
    return len(url)

def Shortining_Service(url):
    return 1 if SHORTENERS_REGEX.search(url) else 0

def having_At_Symbol(url):
    return 1 if "@" in url else 0

def double_slash_redirecting(url):
    after_protocol = url.split("://", 1)[-1]
    return 1 if "//" in after_protocol else 0

def Prefix_Suffix(url):
    parsed = tldextract.extract(url)
    return 1 if "-" in parsed.domain else 0

def having_Sub_Domain(url):
    parsed = tldextract.extract(url)
    return len(parsed.subdomain.split('.')) if parsed.subdomain else 0

# ---------- SSL & Domain ----------
def SSLfinal_State(url):
    parsed = tldextract.extract(url)
    host = parsed.registered_domain
    if not host:
        return 0
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(3)
            s.connect((host, 443))
            cert = s.getpeercert()
        return 1 if cert else 0
    except:
        return 0

def Domain_registeration_length(url):
    parsed = tldextract.extract(url)
    domain = parsed.registered_domain
    try:
        w = whois.whois(domain)
        exp = w.expiration_date
        if isinstance(exp, list):
            exp = exp[0]
        if not exp:
            return -1
        return (exp - datetime.now()).days
    except:
        return -1

def age_of_domain(url):
    parsed = tldextract.extract(url)
    domain = parsed.registered_domain
    try:
        w = whois.whois(domain)
        created = w.creation_date
        if isinstance(created, list):
            created = created[0]
        if not created:
            return -1
        return (datetime.now() - created).days
    except:
        return -1

# ---------- HTML Features ----------
def _get_soup(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        return r, BeautifulSoup(r.text, "html.parser")
    except:
        return None, None

def Favicon(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0
    link = soup.find("link", rel=lambda v: v and 'icon' in v.lower())
    if not link or not link.get("href"):
        return 0
    href = link["href"]
    page_domain = tldextract.extract(url).registered_domain
    href_domain = tldextract.extract(href).registered_domain if href.startswith("http") else page_domain
    return 0 if href_domain == page_domain else 1

def Request_URL(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0.0
    resources = [tag.get("src") or tag.get("href") for tag in soup.find_all(["img","script","link"]) if tag.get("src") or tag.get("href")]
    if not resources:
        return 0.0
    page_domain = tldextract.extract(url).registered_domain
    external = sum(1 for res in resources if tldextract.extract(res).registered_domain and tldextract.extract(res).registered_domain != page_domain)
    return external / len(resources)

def URL_of_Anchor(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0.0
    anchors = soup.find_all("a", href=True)
    if not anchors:
        return 0.0
    page_domain = tldextract.extract(url).registered_domain
    suspicious = 0
    for a in anchors:
        href = a["href"]
        if href.startswith("#") or href.lower().startswith("javascript") or href == "" or (tldextract.extract(href).registered_domain and tldextract.extract(href).registered_domain != page_domain):
            suspicious += 1
    return suspicious / len(anchors)

def Links_in_tags(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0
    count = 0
    for tag_name in ["link","meta","script"]:
        count += len(soup.find_all(tag_name, href=True))
    return count

def SFH(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0
    forms = soup.find_all("form", action=True)
    page_domain = tldextract.extract(url).registered_domain
    suspicious = 0
    for f in forms:
        a = f["action"]
        if a == "" or a is None or (tldextract.extract(a).registered_domain and tldextract.extract(a).registered_domain != page_domain):
            suspicious += 1
    return suspicious

def Submitting_to_email(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0
    return 1 if soup.find(href=lambda href: href and href.startswith("mailto:")) else 0

def on_mouseover(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0
    return 1 if soup.find(attrs={"onmouseover": True}) else 0

def RightClick(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0
    if soup.find(attrs={"oncontextmenu": True}):
        return 1
    r_text = r.text.lower() if r else ""
    return 1 if ("event.button==2" in r_text or ("preventdefault" in r_text and "contextmenu" in r_text)) else 0

def popUpWidnow(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0
    return 1 if "window.open" in (r.text if r else "") else 0

def Iframe(url):
    r, soup = _get_soup(url)
    if not soup:
        return 0
    return 1 if soup.find_all("iframe") else 0

# ---------- DNS & Domain ----------
def DNSRecord(url):
    parsed = tldextract.extract(url)
    domain = parsed.registered_domain
    try:
        answers = dns.resolver.resolve(domain, 'A')
        return 1 if answers else 0
    except:
        return 0

def Abnormal_URL(url):
    parsed = tldextract.extract(url)
    domain = parsed.registered_domain
    if not domain:
        return 1
    try:
        w = whois.whois(domain)
        return 0 if w.domain_name else 1
    except:
        return 1

def Redirect(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        return len(r.history)
    except:
        return -1

# ---------- Misc / Placeholder ----------
def port(url):
    m = re.search(r":(\d+)", url)
    if m:
        return int(m.group(1))
    return 80 if url.startswith("http://") else 443

def HTTPS_token(url):
    parsed = url.split("://")[-1]
    host = parsed.split("/")[0]
    return 1 if "https" in host.lower() else 0

def web_traffic(url):
    return -1

def Page_Rank(url):
    return -1

def Google_Index(url):
    return -1

def Links_pointing_to_page(url):
    return -1

def Statistical_report(url):
    features = extract_all_features(url)
    suspicious_count = sum(1 for k,v in features.items() if isinstance(v,(int,float)) and v and v!=-1)
    return suspicious_count

# ---------- Composite Feature Extraction ----------
def extract_all_features(url):
    return {
        "having_IP_Address": having_IP_Address(url),
        "URL_Length": URL_Length(url),
        "Shortining_Service": Shortining_Service(url),
        "having_At_Symbol": having_At_Symbol(url),
        "double_slash_redirecting": double_slash_redirecting(url),
        "Prefix_Suffix": Prefix_Suffix(url),
        "having_Sub_Domain": having_Sub_Domain(url),
        "SSLfinal_State": SSLfinal_State(url),
        "Domain_registeration_length": Domain_registeration_length(url),
        "Favicon": Favicon(url),
        "port": port(url),
        "HTTPS_token": HTTPS_token(url),
        "Request_URL": Request_URL(url),
        "URL_of_Anchor": URL_of_Anchor(url),
        "Links_in_tags": Links_in_tags(url),
        "SFH": SFH(url),
        "Submitting_to_email": Submitting_to_email(url),
        "Abnormal_URL": Abnormal_URL(url),
        "Redirect": Redirect(url),
        "on_mouseover": on_mouseover(url),
        "RightClick": RightClick(url),
        "popUpWidnow": popUpWidnow(url),
        "Iframe": Iframe(url),
        "age_of_domain": age_of_domain(url),
        "DNSRecord": DNSRecord(url),
        "web_traffic": web_traffic(url),
        "Page_Rank": Page_Rank(url),
        "Google_Index": Google_Index(url),
        "Links_pointing_to_page": Links_pointing_to_page(url),
        "Statistical_report": Statistical_report(url)
    }
