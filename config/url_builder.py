import config.query_string_maker as qsm
import json
import requests


class BuildUrl:
    def __init__(self, process):
        # hard-code language as english
        self.sort = 'sort=date'
        self.process = process

    def make_search_data(self):
        # open dictionary with available countries to extract the tld
        with open('config/top_level_domains.json') as tld:
            countries = json.load(tld)

        # make a list with available countries to
        # perform input error checking
        available_countries = []
        for i in range(len(countries)):
            available_countries.append(countries[i]['fields']['country'])

        # Ask the user for a country to constrain the domain search
        country = input('\nEnter the country in which you want to search\n'
                        'This makes the search domain-specific even if it\'s something remote\n'
                        'Hit enter to default to ".com" searches\n').title()

        # set base search url according to user's input country
        # and according to whether url can be reached
        if len(country) < 1:
            # default to .com
            base_url = 'https://www.indeed.com/jobs?'
            view_job_url = 'https://www.indeed.com/viewjob?jk='
        elif country not in available_countries:
            # default to .com
            print('\nThe country you entered is not supported by Indeed. '
                  'Defaulting to www.indeed.com domain\n')
            base_url = 'https://www.indeed.com/jobs?'
            view_job_url = 'https://www.indeed.com/viewjob?jk='
        else:
            for i in range(0, len(countries)):
                if country == countries[i]['fields']['country']:
                    tld = countries[i]['fields']['tld']
                    base_url = 'https://www.indeed.' + tld
                    # Control for connection errors to get a valid base url
                    try:
                        requests.get(base_url)
                        base_url = 'https://www.indeed.' + tld + '/jobs?'
                        view_job_url = 'https://www.indeed.' + tld + '/viewjob?jk='
                    except requests.ConnectionError:
                        base_url = 'https://' + tld + '.indeed.com/jobs?'
                        view_job_url = 'https://' + tld + '.indeed.com/viewjob?jk='
                    break

        # Prompt the user to input the job title (search_title will be used to name the final csv)
        search_title = input('\nEnter job title: ')
        job_keywords = search_title.split()
        # send job_keywords list to the query string maker
        job_title = 'q=' + qsm.make_query_param(job_keywords).lower()

        # ask the user if they want a remote job
        location_input = input("\nlooking for something remote?\n"
                               "\tIf yes, enter \"yes\"\n"
                               "\tIf not, please enter your preferred location\n"
                               "\tTo omit location, hit enter\n")

        if len(location_input) < 1:
            location = None
        # set location according to user input
        elif location_input.lower() == 'yes':
            # hard-code location as "remote"
            location = 'l=Remote'
        else:
            location_keywords = location_input.split()
            # send location_keywords list to the query string maker
            location = 'l=' + qsm.make_query_param(location_keywords).lower()

        # Ask the user for their preferred base salary
        salary_input = input('\nWhat\'s your base salary?(in thousands - no \'0000\' '
                             'after the number)\n'
                             '\tHit enter to omit the salary\n')

        # set base salary according to user input
        if salary_input:
            salary = qsm.make_salary_query_str(salary_input)
        else:
            salary = None

        # ask the user for job publication date range
        date_input = input('\nHow recent do you want the job posts?\n'
                           '\tEnter the amount of days since the jobs were posted\n'
                           '\tHit enter to omit the date of posting\n')

        # set job posting date range according to user input
        if date_input:
            job_posted_since = 'fromage=' + str(date_input)
        else:
            job_posted_since = None

        # make dictionary to later append search config data and save it as json
        search_data = {'defaultSearch': [{'baseUrl': base_url}]}
        # store config data provided by user to lately be used as values in the json config
        config_items = [job_title, location, salary, job_posted_since, self.sort, view_job_url, search_title]
        # make a list of the "search data" json key names
        search_data_keys = ['jobTitle', 'location', 'salary', 'postsSince', 'sort', 'viewJobUrl', 'searchTitle']
        # make the config json
        for i in range(len(search_data_keys)):
            key = search_data_keys[i]
            val = config_items[i]
            search_data['defaultSearch'].append({key: val})

        # dump search data into json search config file for future searches
        with open('config/default_search_config.json', 'w', encoding='utf-8') as dsc:
            json.dump(search_data, dsc, ensure_ascii=False, indent=4)

        # make the full final url
        query_items = [job_title, location, salary, job_posted_since, self.sort]
        query_str = qsm.make_full_query_str(query_items)
        final_url = base_url + query_str

        # Return a list containing final_url and view_job_url
        urls = [final_url, view_job_url]
        return urls
