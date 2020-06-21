from dataclasses import dataclass


@dataclass
class CompanyDto:
    short_name: str
    long_name: str
    business_summary: str
    industry: str


class CompanyService:
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

    @staticmethod
    def _prepare_json_payload(json):
        

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