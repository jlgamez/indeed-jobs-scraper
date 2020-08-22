# **Indeed Jobs Scraper**
A Python web scraper to automate job search. 

## **Requirements**
- Google Chrome version 84
- pip3: `pip3 install --upgrade pip`
- pipenv: `pip3 install pipenv`
- Python 3.8 or higher: will be automatically installed in the local virtual environment

## **Indeed Jobs Scraper setup**
1. Clone this repository in your machine
2. Traverse to the project directory and create a virtual environment:
`pipenv install`
3. Run `pipenv run python indeed_crawler.py` to check it works.
    - It should open up a dialog saying: "Do you wish to scrape Indeed with the default search config?(yes/no)"
    - Enter "yes". It should look for Spanish teacher jobs in New York

## How to use Indeed Jobs Scraper

If you don't want to see how the bot interacts with the site through the browser open `config/driver_window.json`, change the `false` value to `true` and save it. This will minimise the browser.

To launch the bot, run `pipenv run python indeed_crawler.py`

Upon initiation, you will be prompted to either use the default search configuration or to create a new search.

If "yes" is entered, the bot will search with the parameters given in the previous search. To make a new search, enter "no".

You will be able to specify the following:

- **Country of search** (even if the job is remote, it will search for companies located wherever you specify)
- **The job title**
- **Specific location**: You can look for remote jobs or jobs located somewhere specifically
- **Your base salary**: This **will not filter out jobs not offering this salary** (since many of the posts don't show it). But it will be added as a search parameter
- **Job post recency**
- **Matching terms**: The bot will use your input to select or discard job posts containing specific terms. You can specify:
    - Words you want in the job title
    - Words you don't want in the job title
    - Words you want in the job description
    - Words you don't want in the description

You can also skip entering matching terms, in which case the bot will yield everything it finds with your search parameters.

Your search parameters and matching terms will be saved as default configuration. Therefore, in your next search you will only have to enter "yes" when prompted to use the default configuration.

#### **Warning**:

The logic behind the terms matching will make the bot bring you jobs which either title or description contains selected terms, provided either the description or the title doesn't contain unwanted terms.

This means that you might get jobs with unwanted terms in either the description or in the title because they contain wanted terms in one of those elements. Also you might see jobs which either the title or the description doesn't contain wanted terms because only one of them does.

This is done to make the crawling process more open so you don't miss out potentially interesting results. Nevertheless, the results should always have wanted terms at least in the title or in the description.

## What do you get at the end of the process?

You will get a csv file in the 'results' folder with:
- Jobs titles
- Jobs locations
- Jobs salaries (if shown)
- Companies names
- Jobs ratings (if shown)
- Post recency
- Jobs description
- Url to apply
