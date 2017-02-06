# -*- coding: utf-8 -*-
'''Extract information from html and structure it in a db'''

from bs4 import BeautifulSoup
import pandas as pd


class Extractor(object):
    '''Pull the relevent data out of the page'''

    def __init__(self, html):
        '''Pass the webpage's HTML as a string which is then turned into a
        BeautifulSoup object'''
        self.html = html
        self.soup = BeautifulSoup(html, 'html5lib')

    def nResults(self):
        '''How many search results?'''
        try:
            n = self.soup.find('span', {'class': 'text-noOfSearch-result'})
            results = n.text.replace(',', '')
            print(results)
            return int(results)
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in nResults')

    def title(self):
        '''Extract title'''
        try:
            title = self.soup.title.text
            return title if title else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in title')

    def companies(self):
        '''The block of company info'''
        try:
            companies = self.soup.find_all('div', {'class': 'company-details'})
            return companies
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in companies')

    def rank(self, c):
        '''what rank are they?'''
        try:
            serials = c.find('div', {'class': 'serial-no'})
            return serials.span.get_text() if serials else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in rank')

    def logo(self, c):
        '''location of the company's logo'''
        try:
            logos = c.find('div', {'class': 'company-logo'})
            return c.a.img.get('src', '') if logos else ''
            # return c.a.img['src'] if logos else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in logo')

    def profileLoc(self, c):
        '''the url of the company's detailed info'''
        try:
            logos = c.find('div', {'class': 'company-logo'})
            # return logos.a['href'] if logos else ''
            return logos.a.get('href', '') if logos else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in profileLoc')

    def companyName(self, c):
        '''Name of the company'''
        try:
            companyNames = c.find('span', {'class': 'text-company-name'})
            return companyNames.get_text() if companyNames else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in companyName')

    def companyUrl(self, c):
        '''Company's website url'''
        try:
            companyUrls = c.find('a', {'class': 'company-directUrl-link'})
            # return companyUrls['href'] if companyUrls else ''
            return companyUrls.get('href', '') if companyUrls else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in companyUrl')

    def companyAddress(self, c):
        '''the address of the company'''
        try:
            addresses = c.find('div', {'class': 'company-address-holder'})
            trim = addresses.text.replace('\n', '').replace('\t', '')
            return trim if addresses else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in companyAddress')

    def companyBio(self, c):
        '''A description about the company'''
        try:
            cBios = c.find('div', {'class': 'company-description-holder'})
            return cBios.p.text if cBios else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in companyBio')

    def ceoTitle(self, c):
        '''title of the company's executive'''
        try:
            ceoTitles = c.find('div', {'class': 'position-name'})
            return ceoTitles.text if ceoTitles else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in ceoTitle')

    def ceoName(self, c):
        '''Name of company's executive'''
        try:
            ceoNames = c.find('div', {'class': 'ceo-name'})
            return ceoNames.text if ceoNames else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in ceoName')

    def twitter(self, c):
        '''location of company's twitter profile'''
        try:
            twitters = c.find('a', {'id': 'twitter-link'})
            # return twitters['href'] if twitters else ''
            return twitters.get('href', '') if twitters else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in twitter')

    def facebook(self, c):
        '''location of company's facebook profile'''
        try:
            fbs = c.find('a', {'id': 'fb-link'})
            # return fbs['href'] if fbs else ''
            return fbs.get('href', '') if fbs else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in facebook')

    def linkedin(self, c):
        '''location of company's linkedin profile'''
        try:
            linkedins = c.find('a', {'id': 'linkedin-link'})
            # return linkedins['href'] if linkedins else ''
            return linkedins.get('href', '') if linkedins else ''
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in linkedin')

    def getData(self):
        try:
            companyData = []
            colSequence = ['industryName',
                           'serial',
                           'companyName',
                           'companyUrl',
                           'companyDescription',
                           'companyAddress',
                           'ceoTitle',
                           'ceoName',
                           'facebook',
                           'linkedin',
                           'twitter',
                           'logo',
                           'profileUrl']
            companies = self.companies()
            for company in companies:
                data = {'industryName': 'Industrial Goods & Services',
                        'serial': self.rank(company),
                        'companyName': self.companyName(company),
                        'companyUrl': self.companyUrl(company),
                        'companyDescription': self.companyBio(company),
                        'companyAddress': self.companyAddress(company),
                        'ceoTitle': self.ceoTitle(company),
                        'ceoName': self.ceoName(company),
                        'facebook': self.facebook(company),
                        'linkedin': self.linkedin(company),
                        'twitter': self.twitter(company),
                        'logo': self.logo(company),
                        'profileUrl': self.profileLoc(company)
                        }
                companyData.append(data)
            df = pd.DataFrame(companyData, columns=colSequence)
            return df
        except Exception as e:
            raise SystemExit(e, e.args, 'Exited in getData')
