import pandas as pd
from sqlalchemy import Table, MetaData
from utils import DWTableLoader, SourceTable, Container, Dependencies


class RetailerContactTable(DWTableLoader):
    insert_dependencies = Dependencies([], ['RETAILER'])
    update_dependencies = Dependencies([], ['RETAILER'])

    source_tables = {
        'RETAILER_CONTACT': SourceTable('go_crm', Table('RETAILER_CONTACT', MetaData()))
    }    

    def __init__(self, container: Container):
        super().__init__(container, 'RETAILER_CONTACT', self.source_tables, self.insert_dependencies, self.update_dependencies)    


    def initialLoad(self) -> pd.DataFrame:
        tables        = self.load_source_tables()
        retailer_site = pd.read_sql("SELECT RETAILER_SITE_RETAILER_SITE_CODE AS RETAILER_SITE_CODE, MAX(RETAILER_SITE_RETAILER_SITE_CODE_SK) AS RETAILER_SITE_CODE_SK FROM RETAILER GROUP BY RETAILER_SITE_RETAILER_SITE_CODE", self.engine) # type: ignore
        
        tables['RETAILER_CONTACT'] = tables['RETAILER_CONTACT'].add_prefix('RETAILER_CONTACT_')
        result = self.transform(tables['RETAILER_CONTACT'], retailer_site)
        
        return result
    
    def updateLoad(self, retailer_contact: pd.DataFrame) -> pd.DataFrame:
        retailer_site = pd.read_sql((
            f"SELECT RETAILER_SITE_RETAILER_SITE_CODE AS RETAILER_SITE_CODE, MAX(RETAILER_SITE_RETAILER_SITE_CODE_SK) AS RETAILER_SITE_CODE_SK FROM RETAILER "
            f"WHERE RETAILER_SITE_RETAILER_SITE_CODE IN ({','.join(retailer_contact['RETAILER_SITE_CODE'].astype(str).unique())})"
            f"GROUP BY RETAILER_SITE_RETAILER_SITE_CODE"
        ), self.engine) 

        matched_to_surrogates = self.matchRetailerSiteSurrogateKeys(retailer_contact, retailer_site)
        
        # Remove primary key column, to make sure a new surrogate key is generated
        matched_to_surrogates.drop(columns=['RETAILER_CONTACT_CODE_SK'], inplace=True) # type: ignore

        return matched_to_surrogates
    
    def dependencyUpdate(self, dependencies: dict[str, pd.DataFrame]) -> pd.DataFrame:
        retailer_site = dependencies['RETAILER_SITE'][['RETAILER_SITE_RETAILER_SITE_CODE', 'RETAILER_SITE_RETAILER_SITE_CODE_SK']]
        retailer_site.rename(columns={'RETAILER_SITE_RETAILER_SITE_CODE': 'RETAILER_SITE_CODE', 'RETAILER_SITE_RETAILER_SITE_CODE_SK': 'RETAILER_SITE_CODE_SK'}, inplace=True)

        retailer_contact = pd.read_sql(f"SELECT * FROM RETAILER_CONTACT WHERE RETAILER_SITE_CODE IN ({','.join(retailer_site['RETAILER_SITE_CODE'].unique())})", self.engine) # type: ignore

        return self.transform(retailer_contact, retailer_site)

    def transform(self, retailer_contact: pd.DataFrame, retailer_site: pd.DataFrame) -> pd.DataFrame:
        # Rename columns
        retailer_contact = retailer_contact.rename(columns={
            'RETAILER_CONTACT_RETAILER_CONTACT_CODE_SK': 'RETAILER_CONTACT_CODE_SK',
            'RETAILER_CONTACT_RETAILER_CONTACT_CODE': 'RETAILER_CONTACT_CODE',
            'RETAILER_CONTACT_RETAILER_SITE_CODE': 'RETAILER_SITE_CODE',
        })

        return self.matchRetailerSiteSurrogateKeys(retailer_contact, retailer_site)
    
    def matchRetailerSiteSurrogateKeys(self, retailer_contact: pd.DataFrame, retailer_site: pd.DataFrame) -> pd.DataFrame:
        surrogate_dict = retailer_site.set_index('RETAILER_SITE_CODE').to_dict()['RETAILER_SITE_CODE_SK'] # type: ignore
        retailer_contact['RETAILER_SITE_CODE_SK'] = retailer_contact['RETAILER_SITE_CODE'].astype(int).map(surrogate_dict) # type: ignore

        return retailer_contact