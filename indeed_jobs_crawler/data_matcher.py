# jobs which titles OR descriptions have selected items shall be kept


class MatchJob:
    def __init__(self, titles, descriptions, locations, companies, salaries, ratings, urls,
                 days, discarded_title_terms, discarded_desc_terms, selected_title_terms, selected_description_terms):

        self.keep_titles = []
        self.keep_description = []
        self.keep_locations = []
        self.keep_companies = []
        self.keep_salaries = []
        self.keep_ratings = []
        self.keep_urls = []
        self.keep_days = []

        self.titles = titles
        self.descriptions = descriptions
        self.locations = locations
        self.companies = companies
        self.salaries = salaries
        self.ratings = ratings
        self.urls = urls
        self.days = days

        self.discarded_title_items = discarded_title_terms
        self.discarded_desc_terms = discarded_desc_terms
        self.selected_title_terms = selected_title_terms
        self.selected_description_terms = selected_description_terms

    def keep_job_data(self, i):
        self.keep_titles.append(self.titles[i])
        self.keep_description.append(self.descriptions[i])
        self.keep_locations.append(self.locations[i])
        self.keep_companies.append(self.companies[i])
        self.keep_salaries.append(self.salaries[i])
        self.keep_ratings.append(self.ratings[i])
        self.keep_urls.append(self.urls[i])
        self.keep_days.append(self.days[i])

    def check_title_has_selected_terms(self, title):
        if self.selected_title_terms:
            if any(term in title.lower() for term in self.selected_title_terms):
                return True
            else:
                return False

    def check_description_has_selected_terms(self, description):
        if self.selected_description_terms:
            if any(term in description.lower() for term in self.selected_description_terms):
                return True
            else:
                return False

    def check_title_has_discarded_terms(self, title):
        if self.discarded_title_items:
            if any(term in title.lower() for term in self.discarded_title_items):
                return True
            else:
                return False

    def check_description_has_discarded_terms(self, description):
        if self.discarded_desc_terms:
            if any(term in description.lower() for term in self.discarded_desc_terms):
                return True
            else:
                return False

    def matching(self):
        for t, d in zip(self.titles, self.descriptions):
            if self.check_title_has_selected_terms(t) or self.check_description_has_selected_terms(d):
                if not self.check_title_has_discarded_terms(t) or not self.check_description_has_discarded_terms(d):
                    idx = self.titles.index(t)
                    self.keep_job_data(idx)

    def get_targeted_jobs_data(self):
        if self.selected_title_terms or self.selected_description_terms or self.discarded_title_items or self.discarded_desc_terms:
            self.matching()
            return self.keep_titles, self.keep_description, self.keep_locations, self.keep_companies,\
                self.keep_salaries, self.keep_ratings, self.keep_urls, self.keep_days
        else:
            return self.titles, self.descriptions, self.locations, self.companies, self.salaries, self.ratings, \
                   self.urls, self.days
