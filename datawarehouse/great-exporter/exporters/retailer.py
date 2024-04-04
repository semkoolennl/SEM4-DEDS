import pandas as pd
from utils import DWTableLoader, SourceTable, Container, Dependencies
from sqlalchemy import Table, MetaData

class RetailerTable(DWTableLoader):
    source_tables = {
        'RETAILER': SourceTable('go_crm', Table('RETAILER', MetaData())),
        'RETAILER_SITE': SourceTable('go_crm', Table('RETAILER_SITE', MetaData())),
        'SALES_TERRITORY': SourceTable('go_crm', Table('SALES_TERRITORY', MetaData())),
        'COUNTRY': SourceTable('go_crm', Table('COUNTRY', MetaData())),
        'RETAILER_TYPE': SourceTable('go_crm', Table('RETAILER_TYPE', MetaData())),
    }

    insert_dependencies = Dependencies([], [])

    def __init__(self, container: Container):
        super().__init__(container, 'RETAILER', self.source_tables, self.insert_dependencies)
        
    def initialLoad(self) -> pd.DataFrame:
        tables = self.load_source_tables()
        result = self.transform(tables)

        return result
    
    def updateLoad(self, source_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
        result = self.transform(source_tables)

        return result

    def transform(self, source_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
        retailer         = source_tables['RETAILER'].add_prefix('RETAILER_')
        retailer_type    = source_tables['RETAILER_TYPE'].add_prefix('RETAILER_TYPE_')
        retailer_country = source_tables['COUNTRY'].add_prefix('RETAILER_COUNTRY_')
        sales_territory  = source_tables['SALES_TERRITORY'].add_prefix('SALES_TERRITORY_')
        retailer_site    = source_tables['RETAILER_SITE'].add_prefix('RETAILER_SITE_')

        # Merge tables
        retailer_with_type = retailer.merge(retailer_type, left_on='RETAILER_RETAILER_TYPE_CODE', right_on='RETAILER_TYPE_RETAILER_TYPE_CODE', how='left') # type: ignore

        retailer_country_and_territory = retailer_country.merge(sales_territory, left_on='RETAILER_COUNTRY_SALES_TERRITORY_CODE', right_on='SALES_TERRITORY_SALES_TERRITORY_CODE', how='left') # type: ignore

        retailer_site_with_country_and_territory = retailer_site.merge(retailer_country_and_territory, left_on='RETAILER_SITE_COUNTRY_CODE', right_on='RETAILER_COUNTRY_COUNTRY_CODE', how='left') # type: ignore

        result = retailer_site_with_country_and_territory.merge(retailer_with_type, left_on='RETAILER_SITE_RETAILER_CODE', right_on='RETAILER_RETAILER_CODE', how='left') # type: ignore


        # Remove duplicate columns
        result = result.drop(columns=[ # type: ignore
            'RETAILER_SITE_RETAILER_CODE',
            'RETAILER_SITE_COUNTRY_CODE',
            'RETAILER_COUNTRY_SALES_TERRITORY_CODE',
            'RETAILER_RETAILER_TYPE_CODE',
        ])

        return result