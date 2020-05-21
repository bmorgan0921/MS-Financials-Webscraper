from datetime import datetime

import requests
from bs4 import BeautifulSoup
import html5lib
import pandas as pd

class MorningStarFinancials:
    def __init__(self, ticker, start_date = None, end_date = None):
        '''
        Arguments:
            ticker -- to plug into the scraper
            start_date -- scraper will return an expanded dataframe from start_date in the scraped data to the end_date and forward fill the missing data. 
            end_date -- scraper will return an expanded dataframe from start_date in the scraped data to the end_date and forward fill the missing data. 

        Objective: 
            The objective of this scraper is to return the financials of a company listed on Morningstar's website. 

        Description: 
            This class will first, webscrape a company's Morningstar ratios link to find another link which contains the financials for that company. 
            The scraper then scrapes the second link to find and organize the financials to output.
            
        '''
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        
        self.__main()
    
    def __main(self):
        try:
            self.__get_financials()
        except:
            self.__financials = pd.DataFrame(columns = ['Shares'])
        
    def __get_financials_link(self):
        '''
        Description: 
            This function gets the financials link located on the company/stock financials page on Morningstar. 
            It obtains the financials link from the page data of a base link that can easily be configured for any stock.
            It then returns the financials link for the stock. 
        
        '''


        base_link = 'http://financials.morningstar.com/ratios/r.html?t=' + self.ticker
        response = requests.get(base_link)
        soup = BeautifulSoup(response.content, 'html5lib')
        scriptTags = soup.find_all('script')
        for script in scriptTags:
            if 'function loadFinancePart()' in script.text:
                txt = script.get_text()
                start = txt.find("function loadFinancePart()") + len("function loadFinancePart()")
                end = txt.find(".html(data.componentData);")
                txt = txt[start:end]
                
                start = txt.find('var urlstr = ') + len('var urlstr = ')
                end = txt.find('+orderby;')
            
                link = "https:" + eval(txt[start:end])[:-6]
                return link

    def __get_financials(self):
        '''
        Description: 
            This function scrapes the Financials page for a company/stock and returns the financials dataframe 
            using the specified dates or the entire dataframe if dates are not specified. 
        '''
        url = self.__get_financials_link()
        response = requests.get(url)
        webpage_text = eval(response.text[1:])['componentData']

        id_list = ["Y0", "Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "Y10"]

        soup = BeautifulSoup(webpage_text, 'html5lib')
        date_list = []
        dates = [soup.thead.tr.find('th', id = i).text.split('<')[0] for i in id_list]
        dates[-1] = datetime.now().strftime("%Y-%m-%d")
        i = 0
        temp_dict = {'Dates':dates}
        for tr in soup.find('tbody').find_all('tr'):
            table_row_heading = tr.find('th', attrs = {'class':'row_lbl', 'id': 'i' + str(i)})
            if table_row_heading:
                table_row_heading_value = table_row_heading.find(text = True).strip().split('<')[0]
                temp_dict[table_row_heading_value] = []
                i += 1
                table_data = tr.find_all('td')
                for td in table_data:
                    try:
                        temp_dict[table_row_heading_value].append(float(td.text.split('<')[0].replace(',','')))
                    except ValueError:
                        temp_dict[table_row_heading_value].append(None)


        
        df = pd.DataFrame.from_dict(temp_dict).set_index('Dates')
        df.index = pd.to_datetime(df.index)
        df = df.reindex(pd.date_range(df.index[0], df.index[-1]), method = 'ffill')
        df = df[:-1]
        try: 
            self.__financials = df[self.start_date:self.end_date]
        except:
            self.__financials = df

        return df

    def Financials(self):
        '''
        Description: 
            Returns the financials from the object created. 
        '''
        return self.__financials
