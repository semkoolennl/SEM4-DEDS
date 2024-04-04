import pandas as pd
from sqlalchemy import Table, MetaData
from utils import DWTableLoader, SourceTable, Container

class SalesBranchTable(DWTableLoader):
    source_tables = {
        'SALES_BRANCH': SourceTable('go_sales', Table('SALES_BRANCH', MetaData())),
        'SALES_STAFF': SourceTable('go_sales', Table('SALES_STAFF', MetaData())),
        'COUNTRY': SourceTable('go_sales', Table('COUNTRY', MetaData())),
    }

    def __init__(self, container: Container):
        super().__init__(container, 'SALES_BRANCH', self.source_tables)

    def initialLoad(self) -> pd.DataFrame:
        return self.transform(self.load_source_tables())

    def transform(self, source_tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
        sales_branch  = source_tables['SALES_BRANCH'].add_prefix('SALES_BRANCH_')
        sales_staff   = source_tables['SALES_STAFF'].add_prefix('SALES_STAFF_')
        sales_country = source_tables['COUNTRY'].add_prefix('COUNTRY_')

        # Merge tables
        result = sales_branch.merge(sales_staff, left_on='SALES_BRANCH_SALES_BRANCH_CODE', right_on='SALES_STAFF_SALES_BRANCH_CODE', how='inner') # type: ignore
        result = result.merge(sales_country, left_on='SALES_BRANCH_COUNTRY_CODE', right_on='COUNTRY_COUNTRY_CODE', how='left') # type: ignore

        # Remove duplicate columns
        result = result.drop(columns=['SALES_BRANCH_COUNTRY_CODE', 'SALES_STAFF_SALES_BRANCH_CODE']) # type: ignore

        # Rename columns
        result = result.rename(columns={ # type: ignore
            'SALES_BRANCH_SALES_BRANCH_CODE': 'SALES_BRANCH_CODE',
            'SALES_STAFF_SALES_STAFF_CODE': 'SALES_STAFF_CODE',
        })

        # Convert to datetime
        result['SALES_STAFF_DATE_HIRED'] = pd.to_datetime(result['SALES_STAFF_DATE_HIRED'], format='%d-%m-%Y') # type: ignore

        return result



