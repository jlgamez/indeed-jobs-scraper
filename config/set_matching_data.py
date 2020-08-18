import json


class MatchingData:

    @staticmethod
    def make_matching_data():
        # Prompt the user for matching keywords

        print('\nTERMS MATCHING: Let\'s make your search more specific!'
              '\tNow you will have the chance to introduce keywords you would like the job titles and description'
              'to contain')

        user_input = True
        title_selected_keywords = []
        while user_input:
            term = input('\nEnter a term you want in the title'
                         '\n\tIf you don\'t want to add more title words, hit enter\n').lower()
            if len(term) < 1:
                user_input = False
                break
            title_selected_keywords.append(term)

        user_input = True
        title_discarded_keywords = []
        while user_input:
            term = input('\n\nEnter a term DON\'T want in the job title'
                         '\n\tIf you don\'t want to add more title words, hit enter\n').lower()
            if len(term) < 1:
                user_input = False
                break
            title_discarded_keywords.append(term)

        user_input = True
        description_selected_keywords = []
        while user_input:
            term = input('\n\nEnter a term you want in the job description\n'
                         '\tIf you don\'t want to add more description words, hit enter\n').lower()
            if len(term) < 1:
                user_input = False
                break
            description_selected_keywords.append(term)

        user_input = True
        description_discarded_keywords = []
        while user_input:
            term = input('\n\nEnter a term you DON\'T want in the job description\n'
                         '\tIf you don\'t want to add more words, hit enter\n').lower()
            if len(term) < 1:
                user_input = False
                break
            description_discarded_keywords.append(term)

        # Make the keyword matching dictionary to later append the matching data
        # and save it to a json file
        matching_data = {'titleMatching': {'select': [], 'discard': []}, 'descriptionMatching': {'select': [],
                                                                                                 'discard': []}}
        # Add selected terms for title
        for i in range(len(title_selected_keywords)):
            matching_data['titleMatching']['select'].append({'term': title_selected_keywords[i]})

        # Add discarded terms for title
        for i in range(len(title_discarded_keywords)):
            matching_data['titleMatching']['discard'].append({'term': title_discarded_keywords[i]})

        # Add selected terms for description
        for i in range(len(description_selected_keywords)):
            matching_data['descriptionMatching']['select'].append({'term': description_selected_keywords[i]})

        # Add discarded terms for description
        for i in range(len(description_discarded_keywords)):
            matching_data['descriptionMatching']['discard'].append({'term': description_discarded_keywords[i]})

        # Dump matching data into json file
        with open('config/matching_terms.json', 'w', encoding='utf-8') as mt:
            json.dump(matching_data, mt, ensure_ascii=False, indent=4)
