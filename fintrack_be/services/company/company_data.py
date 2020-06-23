from django.db.models import Q
from fintrack_be.models import Industry
from fintrack_be.models import Company
from fintrack_be.services.industry.industry_data import create_industry


def create_company(short_name, long_name, summary, industry):
    """
    Method used to create a company using the parameters, it is used in the seed management
    command to create the N/A company for unparented stocks.
    :param short_name: The Company short name
    :param long_name: The Company long name
    :param summary: The Company business summary
    :param industry: The Companies parent Industry
    """
    industry = Industry.objects.get(name=industry)
    Company.objects.update_or_create(short_name=short_name,
                                     long_name=long_name,
                                     business_summary=summary,
                                     industry=industry)


def create_company_json(json):
    """
    Method for creating a company taking a JSON object instead of individual parameters,
    if the Industry parent does not exist then it will call the method to create it.
    :param json: JSON that contains the needed data to create a Company
    """
    try:
        # Extracts needed data from JSON parameter
        short_company_name, long_company_name = extract_company_names_from_json(json)
        if 'longBusinessSummary' in json:
            business_summary = json['longBusinessSummary']
        else:
            business_summary = ""

        if 'industry' in json:
            industry_name = json['industry']
        else:
            industry_name = "N/A"

        industry = Industry.objects.get(name=industry_name)
        Company.objects.update_or_create(short_name=short_company_name,
                                         long_name=long_company_name,
                                         business_summary=business_summary,
                                         industry=industry)
        print('{} created'.format(short_company_name))

    except Industry.DoesNotExist:
        # If the parent Industry cannot be found then it creates it then retries to create Company
        sector = json['sector']
        create_industry(industry_name, sector)

        industry = Industry.objects.get(name=industry_name)
        Company.objects.update_or_create(short_name=short_company_name,
                                         long_name=long_company_name,
                                         business_summary=business_summary,
                                         industry=industry)

        print('{} created'.format(short_company_name))

    except KeyError as e:
        print(e)
        industry = Industry.objects.get(name='N/A')
        Company.objects.update_or_create(short_name=short_company_name,
                                         long_name=long_company_name,
                                         business_summary=business_summary,
                                         industry=industry)

        print('{} created'.format(short_company_name))


def get_company(short_name, long_name):
    """
    Gets a company that matches either the short or long name provided
    :param short_name: The Company short name
    :param long_name: The Company long name
    :return: A company object that matches either the short or long name
    """
    return Company.objects.get(Q(short_name=short_name) | Q(long_name=long_name))


def extract_company_names_from_json(json):
    """
    Extract company names from JSON data
    :return: Company short and long name
    """
    if 'shortName' in json and 'longName' in json:
        short_company_name = json['shortName']
        long_company_name = json['longName']
    elif 'shortName' in json and 'longName' not in json:
        short_company_name = json['shortName']
        long_company_name = json['shortName']
    elif 'shortName' not in json and 'longName' in json:
        short_company_name = json['longName']
        long_company_name = json['longName']
    else:
        short_company_name = 'N/A'
        long_company_name = 'Parent company for objects that cant be linked to a parent company'

    return short_company_name, long_company_name
