# MS-Financials-Webscraper

## Description:

financials_webscraper.py gives the user the ability to webscrape for the financials of a company from Morningstar's website. This was made pretty quickly as an addition to a previous project that was in need of a list of financials. Has not been tested with all companys. The script will return financials for companies in the Dow Jones, S&P 100, and S&P 500. Keep in mind that these are annual numbers from Morningstar's website, not quarterly. 

Returns financials from this (example) link: [AAPL Financials](https://financials.morningstar.com/ratios/r.html?t=0P000000GY&culture=en&platform=sal)

## Execution:
```
AAPL = MorningStarFinancials(ticker = 'AAPL').Financials()
print(AAPL)
```

```
             Revenue  Gross Margin %  ...  Cap Spending  Free Cash Flow
2010-09-01   65225.0            39.4  ...       -2121.0         16474.0
2010-09-02   65225.0            39.4  ...       -2121.0         16474.0
2010-09-03   65225.0            39.4  ...       -2121.0         16474.0
2010-09-04   65225.0            39.4  ...       -2121.0         16474.0
2010-09-05   65225.0            39.4  ...       -2121.0         16474.0
...              ...             ...  ...           ...             ...
2020-05-17  260174.0            37.8  ...      -10495.0         58896.0
2020-05-18  260174.0            37.8  ...      -10495.0         58896.0
2020-05-19  260174.0            37.8  ...      -10495.0         58896.0
2020-05-20  260174.0            37.8  ...      -10495.0         58896.0
2020-05-21  267981.0            38.1  ...       -8737.0         66636.0
```