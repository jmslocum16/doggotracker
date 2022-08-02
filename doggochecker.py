import requests, time, datetime, random, os
from datetime import datetime
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
}

def fetch_url(url):
  result = requests.get(url, headers=headers)
  #print(result.status_code)
  
  return BeautifulSoup(result.content, 'html.parser')


# TODO add
# https://www.msrh.org/
# https://www.lilpaws-malteserescue.org/index.php/adopt/our-adoptable-dogs

ADR_URL = "https://www.austindog.org/adoption/available-dogs/all-available-dogs"

def parse_ADR():
  l = []
  soup = fetch_url(ADR_URL)
  root = soup.find(id="dj-classifieds")
  for item in root.find_all("div", {"class": "title"}):
    name = item.find("h2").find("a").text.encode('utf8')
    l.append(name)

  return l
  

APA_URL = "https://www.austinpetsalive.org/adopt/dogs?kids=&pets=dogs&alone=&traffic=&search=&location=&energy=&size=small&dogbreed=&sex=&age=&badge=&sort=&dog=&cat=&child=&home-alone=&tile=large&advanced=yes&scroll=filter"

def parse_APA():
  soup = fetch_url(APA_URL)
  l = []
  for tile in soup.find_all("div", {"class": "large-tile"}):
     inner_tile = tile.find("div", {"class": "inner-tile"})
     name = inner_tile.find("div", {"class": "left-panel"}).find("h3").text.encode('utf8')
     age = inner_tile.find("div", {"class": "right-panel"}).find("li").text.encode('utf8')
     try:
       age_years = int(age.decode('utf-8').strip().split(" ")[0])
       if age_years > 0:
         l.append(name)
     except:
       print('ignoring ' + name + ' ' + age) 

  return l 

AAC_URL="https://petharbor.com/results.asp?searchtype=ADOPT&friends=1&samaritans=1&nosuccess=0&rows=25&imght=120&imgres=thumb&tWidth=200&view=sysadm.v_austin&nobreedreq=1&bgcolor=ffffff&text=29abe2&link=024562&alink=017db3&vlink=017db3&fontface=arial&fontsize=10&col_hdr_bg=29abe2&col_hdr_fg=29abe2&col_fg=29abe2&SBG=ffffff&zip=78704&miles=10&shelterlist=%27ASTN%27&atype=&where=type_DOG,size_s,age_o"

AAC_TEXT_STR = "My name is "
def parse_AAC():
  soup = fetch_url(AAC_URL)
  table = soup.find("table", {"class": "ResultsTable"})

  l = []
  for tr in table.find_all("tr"):
    contents = tr.find_all("td", {"class": "TableContent1"}) + tr.find_all("td", {"class": "TableContent2"})
    for td in contents:
      # txt = td.text.encode('utf8')
      txt = td.text
      nidx = txt.find('name')
      period = txt.find('.')
      if nidx != -1 and period != -1 and nidx < period:
        prev_space_idx = txt.rfind(" ", nidx, period) + 1
        name = txt[prev_space_idx : period]
        l.append(name.encode('utf8'))
  return l
      

AHS_URL = "http://www.austinhumanesociety.org/perfect-pup/"

def parse_AHS():
  soup = fetch_url(AHS_URL)
  available_table = soup.find(id="available_pets_table")
  l = []
  for a_elem in available_table.find_all("a"):
    name = a_elem.find("h3").text.encode('utf8')
    size_str = a_elem.find("p").text.encode('utf8')
    # print(size_str)
    is_small = size_str.find("Small") != -1
    #print(name + ":" + str(is_small))
    if is_small:
      l.append(name)
  return l

DRR_AVAILABLE_URL = "https://www.doodlerockrescue.org/adopt/available-dogs/"

def parse_DRR_available():
  soup = fetch_url(DRR_AVAILABLE_URL)
  sidebar_elem = soup.find(id="wpv-view-layout-7849")
  a_elems = sidebar_elem.find_all("a")
  # TODO - filter "Adoption Pending"
  return [a.text.encode('utf8').strip() for a in a_elems]

DDR_UPCOMING_URL = "https://www.doodlerockrescue.org/adopt/coming-soon-for-adoption/"

def parse_DRR_upcoming():
  soup = fetch_url(DDR_UPCOMING_URL)
  centers = soup.find_all("center")
  doggos = []
  for center_elem in centers:
    strong_elem = center_elem.find("strong")
    if (strong_elem is not None):
      doggos.append(strong_elem.text.encode('utf8').strip())
  return doggos 

SRT_AVAILABLE_URL = "https://schnauzerrescuetexas.me/category/waitingonyou/"
SRT_REPAIR_URL = "https://schnauzerrescuetexas.me/category/inforrepair/"

def parse_SRT(url):
  soup = fetch_url(url)
  # TODO grab from URL
  # with open('/Users/jslocum/Documents/doggo/test.html') as f:
  #  soup = BeautifulSoup(f.read(), 'html.parser')
  articles = soup.find_all("article")
  doggos = []
  for article_elem in articles:
    title_elem = article_elem.find("h1", class_="entry-title")
    if (title_elem is None):
      continue
    a_elem = title_elem.find("a")
    if not "** Adoption Pending ** " in a_elem.text:
      doggos.append(a_elem.text.encode('utf8').strip())

  return doggos

def parse_SRT_available():
  return parse_SRT(SRT_AVAILABLE_URL)

def parse_SRT_repair():
  return parse_SRT(SRT_REPAIR_URL)

LPMR_URL = "https://www.lilpaws-malteserescue.org/index.php/adopt/our-adoptable-dogs"

def parse_LPMR():
  doggos = []
  soup = fetch_url(LPMR_URL)
  pet_names = soup.find_all("div", class_="pet-name-container")
  for pet_name in pet_names:
    a_elem = pet_name.find("a")
    doggos.append(a_elem.text.encode('utf8').strip())
  return doggos

GAS_URL = "https://fpm.petfinder.com/petlist/petlist.cgi?shelter=TX34&haspets=&hasprevious=&title=Georgetown+Animal+Shelter&limit=25&moreinfo=&style=8&sort=&status=A&picsize=&color1=&color2=&animal=Dog&breed=&age=&size=S"

def parse_petfinder_embedded(url):
  doggos = []
  soup = fetch_url(url)
  pets = soup.find_all("div", class_="name")
  for pet in pets:
    a_elem = pet.find("a")
    span_elem = a_elem.find("span")
    doggos.append(span_elem.text.encode('utf8').strip())
  return doggos
  
def parse_GAS():
  return parse_petfinder_embedded(GAS_URL)

def parse_MSRH(url):
  doggos = []
  soup = fetch_url(url)
  body = soup.find(id="PAGES_CONTAINER")
  pets = body.find_all("div", class_="_1ncY2")
  for pet in pets:
    elem = pet.find("h2")
    children = elem.findChildren("span", recursive=False)
    while len(children) > 0:
      elem = children[0]
      children = elem.findChildren("span", recursive=False)
    name = elem.text.strip().encode('utf8').strip()
    doggos.append(name)
  return doggos

MSRH_available_URL = "https://www.msrh.org/for-adoption"
def parse_MSRH_available():
  return parse_MSRH(MSRH_available_URL)

MSRH_arrived_URL = "https://www.msrh.org/rescue-icu"
def parse_MSRH_arrived():
  return parse_MSRH(MSRH_arrived_URL)

last_run_dir = "/Users/jslocum/Documents/doggotracker/last_run/"

def load_last_check(fname):
  path = last_run_dir + fname
  if (not os.path.exists(path)):
    print("warning - " + path + " does not exist")
    return []
  with open(path,'r') as f:
     return [line.rstrip() for line in f.readlines()]

def store_last_check(fname, doggos):
  path = last_run_dir + fname
  with open(path, 'w') as f:
    f.write("\n".join(doggos))


checks = [
#  ("Austin Humane Society", "ahs.txt", parse_AHS), # TODO - changed site

  ("Schnauzer Rescue Of Texas - Waiting On You", "srt_available.txt", parse_SRT_available),
  ("Schnauzer Rescue Of Texas - In For Repair", "srt_repair.txt", parse_SRT_repair),
  ("Doodle Rock Rescue - Available ", "drr_available.txt", parse_DRR_available),
  ("Doodle Rock Rescue - Upcoming", "drr_upcoming.txt", parse_DRR_upcoming),
  ("Austin Animal Center", "aac.txt", parse_AAC),
  ("Austin Pets Alive", "apa.txt", parse_APA),
  ("Austin Dog Rescue", "adr.txt", parse_ADR),
  ("Lil Paws Maltese Rescue", "lpmr.txt", parse_LPMR),
  ("Georgetown Animal Shelter", "gas.txt", parse_GAS),
  ("Mini Schnauzer Rescue Of Houston - For Adoption", "msrh_available.txt", parse_MSRH_available),
  ("Mini Schnauzer Rescue Of Houston - Just Arrived", "msrh_arrived.txt", parse_MSRH_arrived)
]

def do_check(check, flog, printedDate):
  last_doggos = load_last_check(check[1])
  new_doggos_b = check[2]()
  new_doggos = [d.decode('utf-8') for d in new_doggos_b]
  store_last_check(check[1], new_doggos)
  # do diff
  doggos_removed = []
  doggos_added = []
  last_set = set(last_doggos)
  new_set = set(new_doggos)
  for doggo in new_doggos:
    if not doggo in last_set:
      doggos_added.append(doggo)
  for doggo in last_doggos:
    if (not doggo in new_set):
      doggos_removed.append(doggo)
 
  if len(doggos_removed) > 0 or len(doggos_added) > 0:
    if not printedDate:
      now = datetime.now()
      dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
      flog.write(dt_string + "\n")
    print(check[0])
    flog.write(check[0] + "\n")
    for doggo in doggos_added:
      print(" +" + doggo)
      flog.write(" +" + doggo + "\n")
    for doggo in doggos_removed:
      print(" -" + doggo)
      flog.write(" -" + doggo + "\n")
    print()
    flog.write("\n")
    return True
  return False
  

def do_checks():
  flog = open('log.txt', 'a')
  printedDate = False
  random.shuffle(checks)
  for check in checks:
    printedDate |= do_check(check, flog, printedDate)
    # time.sleep(10 + random.randint(1, 30))
  print("Done")

def run():
  """
  while True:
    currentDT = datetime.datetime.now()
    if (currentDT.hour > 7 and currentDT.hour < 22):
      do_checks()
    print("----------------")
    time.sleep(7200 + random.randint(1, 5000))
  """
  do_checks()

run()
