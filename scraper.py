import re
import requests
from bs4 import BeautifulSoup
import pprint
pp = pprint.PrettyPrinter(indent=4) 

def get_p(page_request):
    # Finds all <p> tags and returns them in a list. If a <p> is embedded
    # in another <p>, it extracts any embedded <p>s and adds the topmost
    # to the list before continuing
    plist = []
    soup = BeautifulSoup(page_request.text, "html.parser")
    paragraphs = soup.find_all('p')

    for par in reversed(paragraphs):
        if par.p:
            par.p.extract()
            plist.append(par)
        else:
            plist.append(par)

    return plist

def new_url(_url, number):
    # Converts an integer to a string and formats it for a the new URL
    return _url.format(str(number))

def get_sites():
    with open('testfile.tex', 'w') as f:
        # Create LaTeX file and preamble
        f.write('\\documentclass{article}' + '\n')
        f.write('\\usepackage{geometry}' + '\n')
        f.write('\\begin{document}' + '\n')
        f.write('\\noindent')
        numby = 1 

        # Choose the number of entries to find
        while numby < 10: 
            current_site = new_url(url, numby)
            r = requests.get(current_site)
            soup = BeautifulSoup(r.text, "html.parser") 

            # Replace strange HTML linebreaks with text linebreaks
            for br in soup.find_all("br"):
                br.replace_with("\n")
            
            try:
                # Grab title
                title = soup.title
                ready = " \\textbf{" + title.text + "}\\\\"
                
                # Grab a list of all <p> tags
                embed_p = get_p(r) 
                actual_page = None
                actual_date = None
                entry = '' 
                page = None
                date = None 


                # Grab page numbers
                for p in embed_p:
                    is_page = re.search('Page \d+', p.text)
                    if is_page:
                        page = is_page.group()
                        actual_page = p            
                if page == None:
                    page = "Page N/A"
          

                # Grab dates
                for p in embed_p:
                    if not p.a:
                        has_date = re.search(' \d+, \d+', p.text)
                        if has_date and len(p.text) < 20:
                            date = p.text 
                            actual_date = p   
                if date == None:
                    date = "Date N/A"
                
                # Convert remaining paragraphs to LaTeX provided they do not
                # contain a web address
                for p in embed_p:
                    text = p.text + '\n'
                    if "PREVIOUS SECTION" not in text and "Link to date-related" not in text and "Page image" not in text:
                        entry = ' ' + text + '***' + entry
                f.write('\\textbf{' + str(numby) + '})')
                f.write(ready + '\\\\\n') 
                f.write(date + ' ' + page + '\\\\\n')
                f.write('\\\\\n')
                f.write(entry + '\\\\\n')
                f.write('\\\\')
            
                numby += 1
            except:
                numby += 1

        f.write('\\end{document}')

url = "https://memory.loc.gov/cgi-bin/query/D?hlaw:{}:./temp/~ammem_akPe::"
get_sites()

