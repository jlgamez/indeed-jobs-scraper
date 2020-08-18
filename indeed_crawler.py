import indeed_jobs_crawler.data_matcher as dm
import config.config_setup as cs
import config.url_builder as ub
import config.set_matching_data as smd
import indeed_jobs_crawler.info_scraper as scrape
import pandas as pd
import json

config_type = input('\nDo you wish to scrape Indeed with the default search config?(yes/no)\n').lower()

while config_type not in ['yes', 'no']:
    config_type = input('\nPlease enter "yes" or "no"\n').lower()

url_builder = ub.BuildUrl(config_type)

if url_builder.process == 'no':
    # let the user set the search data
    urls_list = url_builder.make_search_data()
    url = urls_list[0]
    view_job_url = urls_list[1]
    # and let the user set the matching data (to be stored in a json used later)
    smd.MatchingData.make_matching_data()

else:
    # load default search data
    url = cs.final_url
    view_job_url = cs.view_job_url


# ***************************************
#           START CRAWLING
# ***************************************

job_titles = []
company_names = []
jobs_ratings = []
jobs_locations = []
apply_urls = []
salaries = []
days = []
descriptions = []

while url:
    # Create a soup object
    site = scrape.set_soup_object(url)
    print('\nFetching data from ' + url + '\n')
    # Scrape job titles
    titles_list = []
    scraped_titles = scrape.get_jobs_titles(site, titles_list)
    for s in scraped_titles:
        job_titles.append(s)
    print('\njob titles: ' + str(job_titles) + '\n')

    # Scrape company names
    companies_list = []
    scraped_companies = scrape.get_company_names(site, companies_list)
    for s in scraped_companies:
        company_names.append(s)
    print('\nCompanies: ' + str(company_names) + '\n')

    # Scrape job rating
    ratings_list = []
    scraped_ratings = scrape.get_jobs_ratings(site, ratings_list)
    for s in scraped_ratings:
        jobs_ratings.append(s)
    print('\nJobs ratings: ' + str(jobs_ratings) + '\n')

    # Scrape jobs locations
    locations_list = []
    scraped_locations = scrape.get_jobs_locations(site, locations_list)
    for s in scraped_locations:
        jobs_locations.append(s)
    print('\nJobs locations: ' + str(jobs_locations) + '\n')

    # Scrape apply url
    apply_list = []
    scraped_urls = scrape.get_apply_url(site, apply_list, view_job_url)
    for s in scraped_urls:
        apply_urls.append(s)
    print('\nApply url: ' + str(apply_urls) + '\n')

    # Scrape job salaries
    salaries_list = []
    scraped_salaries = scrape.get_salaries(site, salaries_list)
    for s in scraped_salaries:
        salaries.append(s)
    print('\nSalaries: ' + str(salaries) + '\n')

    # Scrape days passed since the job was posted
    days_since_posted_list = []
    scraped_days = scrape.get_days_since_posted(site, days_since_posted_list)
    for s in scraped_days:
        days.append(s)
    print('\nPosts time: ' + str(days) + '\n')

    # Scrape jobs descriptions
    descriptions_list = []
    scraped_descriptions = scrape.get_job_description(url, descriptions_list)
    for s in scraped_descriptions:
        descriptions.append(s)
    print('\nJobs descriptions: ' + str(descriptions) + '\n')

    # paginate next
    url = scrape.paginate_next(url)

# Get jobs data that should be discarded
# load the matching data
title_disc = cs.title_discarded_terms

title_select = cs.title_selected_terms

description_disc = cs.description_discarded_terms

description_select = cs.description_selected_terms

data_match = dm.MatchJob(job_titles, descriptions, jobs_locations, company_names, salaries, jobs_ratings, apply_urls,
                         days, title_disc, description_disc, title_select, description_select)

final_titles, final_descriptions, final_locations, final_companies, final_salaries, final_ratings, final_urls, \
    final_days = data_match.get_targeted_jobs_data()

print('\n\n FINAL DATA SAMPLE\n\n')
print('\njob titles: ' + str(final_titles) + '\n')
print('\nSalaries: ' + str(final_salaries) + '\n')
print('\nJobs locations: ' + str(final_locations) + '\n')
print('\nCompanies: ' + str(final_companies) + '\n')
print('\nJobs ratings: ' + str(final_ratings) + '\n')
print('\nApply url: ' + str(final_urls) + '\n')
print('\nPosts time: ' + str(final_days) + '\n')
print('\nJobs descriptions: ' + str(final_descriptions) + '\n')


# Put all jobs data into a data frame
jobs_df = pd.DataFrame({"Job Title": final_titles, "Location": final_locations, "Salary": final_salaries, "Company": final_companies, "Job Rating": final_ratings, "Post time": final_days, "Description": final_descriptions, "Apply url": final_urls})

# Load the search title
with open('config/default_search_config.json') as dsc:
    search_data = json.load(dsc).get('defaultSearch')

for i in range(len(search_data)):
    if list(search_data[i].keys())[0] == 'searchTitle':
        search_name = search_data[i].get('searchTitle')
        break

file_id = search_name.replace(' ', '_')

# Save results in a csv file
jobs_df.to_csv('results/job_search_' + file_id + '.csv', encoding='utf8')

print('\nCongratulations! You\'ve successfully scraped Indeed for your job search. The results are in a csv file'
      'in the \'results\' folder\n')

