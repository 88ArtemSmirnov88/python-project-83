from bs4 import BeautifulSoup


def get_page_data(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    h1_tag = soup.find('h1').get_text() if soup.find('h1') is not None else ''
    title_tag = soup.find('title').get_text() if soup.find('title') is not None else ''
    description = soup.find('meta', attrs={'name': 'description'})
    if description:
        description = description['content']
    else:
        description = ''

    return {
        'h1': h1_tag,
        'title': title_tag,
        'description': description
    }
