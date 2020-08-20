import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import config.chromedriver_os as OS
import json


def set_soup_object(url):
    # make a request to the url
    link = requests.get(url)
    # Create a soup object using the html parser to read the page
    site = BeautifulSoup(link.text, 'html.parser')

    return site


def get_jobs_titles(site, titles_list):
    scraped_job_titles = titles_list
    # Extract <a> tags with class 'jobtitle turnstileLink'
    jobs_a = site.find_all(name='a', attrs={'data-tn-element': 'jobTitle'})
    for job in jobs_a:
        # store all attributes in a dictionary.
        # Then store the value of 'title' key in job_titles list
        job_attrs = job.attrs
        scraped_job_titles.append(job_attrs['title'])

    return scraped_job_titles


def get_jobs_locations(site, locations_list):
    scraped_job_locations = locations_list
    # Find <div> tags with class 'recJobLoc'
    loc_div = site.find_all('div', attrs={'class': 'recJobLoc'})
    # Store all attributes in a dictionary.
    # Then append the value of 'data-rc-loc' into job_locations
    for loc in loc_div:
        loc_attrs = loc.attrs
        scraped_job_locations.append(loc_attrs['data-rc-loc'])

    return scraped_job_locations


def get_company_names(site, companies_list):
    scraped_company_names = companies_list
    company_span = site.find_all('span', attrs={'class': 'company'})
    for span in company_span:
        scraped_company_names.append(span.text.strip())

    return scraped_company_names


def get_salaries(site, salaries_list):
    scraped_salaries = salaries_list
    jobs_divs = site.find_all('div', attrs={'class': 'jobsearch-SerpJobCard'})
    for div in jobs_divs:
        salary_span = div.find('span', attrs={'class': 'salaryText'})
        if salary_span:
            scraped_salaries.append(salary_span.string.strip())
        else:
            scraped_salaries.append('Not shown')

    return scraped_salaries


def get_jobs_ratings(site, ratings_list):
    scraped_ratings = ratings_list
    jobs_divs = site.find_all('div', attrs={'class': 'jobsearch-SerpJobCard'})
    for div in jobs_divs:
        rating_span = div.find('span', attrs={'class': 'ratingsContent'})
        if rating_span:
            scraped_ratings.append(float(rating_span.text.strip().replace(',', '.')))
        else:
            scraped_ratings.append(None)

    return scraped_ratings


def get_apply_url(site, apply_list, view_job_url):
    scraped_apply_urls = apply_list
    jobs_div = site.find_all(name='div', attrs={'class': 'jobsearch-SerpJobCard'})
    for div in jobs_div:
        job_id = div.attrs['data-jk']
        apply_url = view_job_url + job_id
        scraped_apply_urls.append(apply_url)

    return scraped_apply_urls


def get_days_since_posted(site, days_since_posted_list):
    scraped_days = days_since_posted_list
    days_spans = site.find_all('span', attrs={'class': 'date'})
    for day in days_spans:
        day_string = day.text.strip()

        if re.findall('[0-9]+', day_string):
            parsed_day = re.findall('[0-9]+', day_string)[0]
            if 'hour' in day_string:
                job_posted_since = str(parsed_day) + ' hours ago'
            elif 'day' in day_string:
                job_posted_since = str(parsed_day) + ' days ago'
            elif 'week' in day_string:
                job_posted_since = str(parsed_day) + ' weeks ago'
            elif 'month' in day_string:
                job_posted_since = str(parsed_day) + ' months ago'
            else:
                job_posted_since = str(day_string)
        else:
            job_posted_since = 'today'

        scraped_days.append(job_posted_since)

    return scraped_days


def set_driver():
    with open('config/driver_window.json') as window:
        minimised = json.load(window).get('minimised')
    chrome_driver = OS.get_driver_name()
    driver = webdriver.Chrome('indeed_jobs_crawler/' + chrome_driver)
    if minimised:
        driver.minimize_window()
    else:
        driver.maximize_window()

    return driver


def get_job_description(url, descriptions_list):
    # Use selenium to try to access job full description.
    scraped_descriptions = descriptions_list
    driver = set_driver()
    wait = WebDriverWait(driver, 10)

    print('\nGETTING JOBS DESCRIPTIONS...\n')

    driver.get(url)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'jobsearch-SerpJobCard')))
    jobs = driver.find_elements_by_class_name('jobsearch-SerpJobCard')

    def click_on_job_and_add_description(job_card):
        job_card.click()
        wait.until(EC.presence_of_element_located((By.ID, 'vjs-content')))
        scraped_descriptions.append(driver.find_element_by_id('vjs-content').text)

    for job in jobs:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'jobsearch-SerpJobCard')))
        try:  # click on the job card and add its description to descriptions list
            click_on_job_and_add_description(job)
        except (ElementClickInterceptedException, TimeoutException):
            # if ElementClickInterceptedException, scroll away and try again
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            click_on_job_and_add_description(job)

    driver.close()
    driver.quit()
    return scraped_descriptions


def paginate_next(url):
    driver = set_driver()
    wait = WebDriverWait(driver, 10)
    driver.get(url)

    # Exclude aria-label atr containing numbers
    # (elements doing so are NOT the "next button")
    try:
        aria_label = driver.find_element_by_xpath("//ul[@class='pagination-list']/li[last()]/a").get_attribute(
            'aria-label')
    except NoSuchElementException:
        # In case of NoSuchElementException
        # set aria-label to a non-valid string (process will end if it contains digits)
        aria_label = '4321'

    # if next button is present (i.e aria label doesn't contain numbers, try to click)
    if any(map(str.isdigit, aria_label)):
        next_url = None
    else:
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='pagination-list']/li[last()]/a")))
            next_button = driver.find_element(By.XPATH, "//ul[@class='pagination-list']/li[last()]/a")
            try:
                next_button.click()
                # time.sleep(2)
                next_url = driver.current_url
            except (ElementClickInterceptedException, TimeoutException):
                # if ElementClickInterceptedException, scroll away and try again
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[@class='pagination-list']/li[last()]/a")))
                next_button.click()
                time.sleep(2)
                next_url = driver.current_url
        except TimeoutException:
            next_url = None

    driver.close()
    driver.quit()

    return next_url
