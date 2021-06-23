import pandas as pd
from bs4 import BeautifulSoup

html_file_path = 'result.html'

result_path = 'result.xlsx'


# name : article.alt
# position p.class = text-sm truncate m-0 truncate
# company p.class = text-sm truncate m-0 mb-1 truncate


def clean_text(text):
    cleaned_str = str(text).replace('\n', '')
    # Collapses multiple spaces to one space
    return ' '.join(cleaned_str.split())


def process_single_entry(participant_tag):
    # soup = BeautifulSoup(participant_tag, 'html.parser')

    name_tags = participant_tag.find_all('article')[0].find_all('img')
    position_tags = participant_tag.find_all('p', class_='text-sm truncate m-0 truncate')
    job_tags = participant_tag.find_all('p', class_='text-sm truncate m-0 mb-1 truncate')

    name = clean_text(name_tags[0]['alt'])
    position = clean_text(position_tags[0].get_text())
    job = clean_text(job_tags[0].get_text())

    print('Saving new record with name: ', name, ' job: ', job, ' position: ', position)

    return name, position, job


def save_data_to_excel(data):
    print('Saving data to excel.')
    df = pd.DataFrame(data=data,
                      columns=['Name', 'Position', 'Job'])

    df.to_excel(result_path)
    print('Data saved.')


def start_processing():
    result = list()
    f = open(html_file_path)
    soup = BeautifulSoup(f.read(), 'html.parser')
    all_participants_tags = soup.find_all('rli-participant-lib-participant-list-card')

    for participant_tag in all_participants_tags:
        # print(participant_tag)
        result.append(process_single_entry(participant_tag))

    print('Parsing done.')

    save_data_to_excel(result)

    print('Terminating.')


if __name__ == '__main__':
    start_processing()
