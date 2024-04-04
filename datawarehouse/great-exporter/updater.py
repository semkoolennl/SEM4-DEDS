from loaderManager import LoaderManager
from exporters import RetailerContactTable
import pandas as pd

lm     = LoaderManager()
engine = lm.container.engine


retailer_contact = pd.read_sql("SELECT * FROM RETAILER_CONTACT WHERE RETAILER_CONTACT_JOB_POSITION_EN = 'District Manager - edited'", engine) # type: ignore
retailer_contact.to_html('retailer_contact-updated.html')

# if isinstance(lm.loaders['RetailerContactTable'], RetailerContactTable):
#     loader: RetailerContactTable = lm.loaders['RetailerContactTable']
#     result = loader.updateLoad(retailer_contact)
#     result.to_sql('RETAILER_CONTACT', engine, if_exists='append', index=False)

# print(pd.read_sql("SELECT * FROM RETAILER_CONTACT WHERE RETAILER_CONTACT_JOB_POSITION_EN = 'District Manager - edited'", engine))

