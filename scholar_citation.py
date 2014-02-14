#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <td valign="top">
# <a class="cit-dark-large-link" href="/citations?user=LhOAiXMAAAAJ&amp;hl=en">Duncan J Watts</a><br/>
# Principal Researcher, Microsoft<br>
# Verified email at microsoft.com<br>
# Cited by 46975<br>
# <form method="post" style="display:inline" action="/citations?hl=en&amp;mauthors=label:network_science&amp;view_op=search_authors">
# <input type="hidden" name="xsrf" value="AMstHGQAAAAAUv-3iDpzE3uqveGbrmNxoR9WIH2dG2F6"/>
# <input type="hidden" name="colleague" value="LhOAiXMAAAAJ"/>
# <input type="submit" name="add_colleague_btn" value="Add co-author"/></form>
# </td>
# </tr></table></div></div><div class="g-section g-tpl-50-50"><div class="g-unit g-first">
# <table style="margin: 5px 0px;"><tr><td style="text-align: center; padding: 0px 5px;width: 150px;">
# <a href="/citations?user=U3CXAPsAAAAJ&amp;hl=en">
# <img src="/citations?view_op=view_photo&amp;user=U3CXAPsAAAAJ&amp;citpid=1" width="100" height="150"/></a></td>

from bs4 import BeautifulSoup
import urllib2
import sys, os
import re, random, time
import smtplib

GOOG_URL = "http://scholar.google.com"
START_URL = "http://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=label:{0}"
MAX_LOOP = 100

def parse_a_url_for_citations(url, fout = None):
    next_link = None
    # <a class="cit-dark-large-link"
    # <a href="/citations?view_op=search_authors&amp;hl=en&amp;mauthors=label:network_science&amp;after_author=lOECAK7J__8J&amp;astart=10" class="cit-dark-link">Next &gt;</a>
    try:
        response = urllib2.urlopen(url)
        html_source = response.read()
        soup = BeautifulSoup(html_source)
    except:
        print '[ERROR][read source code]', sys.exc_info()
    
    
    # Get names and citation strings
    links = soup.find_all('a', attrs={'class': 'cit-dark-large-link'})
    cite_ptn = re.compile("Cited by \d+<br>")
    cites = cite_ptn.findall(html_source)
    if len(links) != len(cites):
        return next_link
    
    # Save to file
    for i,link in enumerate(links):
        name = link.get_text().strip()
        cite = int(cites[i][9:-4])
        print name, cite
        if fout:
            fout.write('{0},{1}\n'.format(name.encode('utf8'), cite))
    
    # Get next link string
    next_link = soup.find('a', attrs={'class','cit-dark-link'}, text=u"Next >")['href']
    next_link = GOOG_URL + next_link
    return next_link



def main(label):
    url = START_URL.format(label)
    fout = open("scholar_citation_{0}.csv".format(label), "w")
    loop = 0
    while url and loop < MAX_LOOP:
        loop += 1
        print "Parsing ...", url
        next_url = parse_a_url_for_citations(url, fout)
        url = next_url
        # Sleep random seconds
        sec = random.randint(0,5); print 'Sleep', sec, 'seconds ...'
        time.sleep(sec)
    fout.close()



if __name__ == "__main__":
    label = sys.argv[1] # "network_science"
    main(label)



    