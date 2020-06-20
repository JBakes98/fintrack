import requests
import bs4 as bs
from country.models import Country


def create_country_instances():
    """
    Method that creates the Country instances from the provided source
    """
    link = 'https://www.iban.com/country-codes'
    resp = requests.get(link)
    soup = bs.BeautifulSoup(resp.text, "lxml")
    table = soup.find('table', {'id': 'myTable'})

    for row in table.find_all('tr')[1:]:
        name = row.findAll('td')[0].text
        alpha2 = row.findAll('td')[1].text
        alpha3 = row.findAll('td')[2].text
        numeric = int(row.findAll('td')[3].text)
        Country.objects.update_or_create(name=name, alpha2=alpha2, alpha3=alpha3, numeric=numeric)
        print('Created {}'.format(alpha2))

    # Custom EU objects for EuroNext exchange
    Country.objects.update_or_create(name='European Union', alpha2='EU', alpha3='EEA')
