import config.query_string_maker as qsm
import json

# load default search data
with open('config/default_search_config.json') as dsc:
    search_input_data = json.load(dsc).get('defaultSearch')

base_url = search_input_data[0].get('baseUrl')

# load all query params into a list
# (i.e all defaultSearch elements except baseUrl )
query_items = []
for i in range(1, len(search_input_data) - 2):
    key = list(search_input_data[i].keys())[0]
    query_param = search_input_data[i].get(key)
    if query_param:
        query_items.append(query_param)

# make a full string with query params
query_str = qsm.make_full_query_str(query_items)
# concatenate base url and query string to have a full search url
final_url = base_url + query_str
# set view_job_url to apply url normalisation later
view_job_url = search_input_data[6].get('viewJobUrl')


def load_terms_list(dict_list):
    terms_list = []
    for i in range(len(dict_list)):
        key = list(dict_list[i].keys())[0]
        terms_list.append(dict_list[i].get(key))
    return terms_list


def open_json_matching_data(match_on, matching_type):
    with open('config/matching_terms.json') as mt:
        matching_data = json.load(mt).get(match_on).get(matching_type)
    return matching_data


# load matching data for job titles
selected_title_list = open_json_matching_data('titleMatching', 'select')

title_selected_terms = load_terms_list(selected_title_list)

# load discarding data for job titles
discarded_title_list = selected_title_list = open_json_matching_data('titleMatching', 'discard')

title_discarded_terms = load_terms_list(discarded_title_list)

# load selected data for description
selected_description_list = open_json_matching_data('descriptionMatching', 'select')

description_selected_terms = load_terms_list(selected_description_list)

# load discarding data for description
discarded_description_list = open_json_matching_data('descriptionMatching', 'discard')

description_discarded_terms = load_terms_list(discarded_description_list)

