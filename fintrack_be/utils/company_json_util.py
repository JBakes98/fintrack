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

    # Strip commas from company names as this stop the names being accepted in URLs
    short_company_name = short_company_name.replace(',', '')
    long_company_name = long_company_name.replace(',', '')

    return short_company_name, long_company_name