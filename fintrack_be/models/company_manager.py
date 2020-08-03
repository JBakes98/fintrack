from django.db import models

from fintrack_be.models.industry import Industry


class CompanyManager(models.Manager):
    use_in_migrations = True

    def _create_company(self, short_name, long_name, summary, industry):
        company = self.model(
            short_name=short_name,
            long_name=long_name,
            business_summary=summary,
            industry=industry
        )
        company.save(using=self._db)

        return company

    def create_company(self, short_name, long_name, summary, industry):
        return self._create_company(short_name, long_name, summary, industry)

    def create_company_json(self, json):
        from fintrack_be.services.company.company_service import CompanyDataService
        try:
            # Extracts needed data from JSON parameter
            short_company_name, long_company_name = CompanyDataService.extract_company_names_from_json(json)

            if 'longBusinessSummary' in json:
                business_summary = json['longBusinessSummary']
            else:
                business_summary = ""
            if 'industry' in json:
                industry_name = json['industry']
            else:
                industry_name = "N/A"

            industry = Industry.objects.get(name=industry_name)
            self._create_company(short_company_name, long_company_name, business_summary, industry)

            print('{} created'.format(short_company_name))

        except Industry.DoesNotExist:
            # If the parent Industry cannot be found then it creates it then retries to create Company
            sector = json['sector']
            Industry.objects.create_industry(industry_name, sector)

            industry = Industry.objects.get(name=industry_name)
            self._create_company(short_company_name, long_company_name, business_summary, industry)

            print('{} created'.format(short_company_name))

        except KeyError as e:
            print(e)
            industry = Industry.objects.get(name='N/A')
            self._create_company(short_company_name, long_company_name, business_summary, industry)

            print('{} created'.format(short_company_name))
