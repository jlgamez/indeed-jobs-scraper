# normalise provided keywords to indeed query param format
def make_query_param(keywords_list):
    query_param = ''
    for i in range(len(keywords_list) - 1):
        keyword = (keywords_list[i]) + '+'
        query_param += keyword
    keywords_list.reverse()
    query_param += keywords_list[0]
    return query_param


# make the query string with the salary
def make_salary_query_str(salary):
    base_salary = '%24' + salary + '%2C000'
    return base_salary


# make the full query string
def make_full_query_str(query_parameters):
    query_str = query_parameters[0]
    for i in range(1, len(query_parameters)):
        if query_parameters[i]:
            query_str += '&' + str(query_parameters[i])
    return query_str
