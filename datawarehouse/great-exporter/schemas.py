from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.sql import func

meta = MetaData()

retailer = Table('RETAILER', meta,
    Column('RETAILER_SITE_RETAILER_SITE_CODE_SK', Integer, primary_key=True, autoincrement=True),
    Column('RETAILER_SITE_RETAILER_SITE_CODE', Integer, nullable=False),
    Column('RETAILER_SITE_ADDRESS1', String(255)),
    Column('RETAILER_SITE_ADDRESS2', String(255)),
    Column('RETAILER_SITE_CITY', String(255)),
    Column('RETAILER_SITE_REGION', String(255)),
    Column('RETAILER_SITE_POSTAL_ZONE', String(255)),
    Column('RETAILER_SITE_ACTIVE_INDICATOR', Integer),

    Column('RETAILER_RETAILER_CODE', Integer, nullable=False),
    Column('RETAILER_RETAILER_CODEMR', Integer),
    Column('RETAILER_COMPANY_NAME', String(255)),

    Column('SALES_TERRITORY_SALES_TERRITORY_CODE', Integer),
    Column('SALES_TERRITORY_TERRITORY_NAME_EN', String(255)),

    Column('RETAILER_COUNTRY_COUNTRY_CODE', Integer, nullable=False),
    Column('RETAILER_COUNTRY_COUNTRY_EN', String(255)),
    Column('RETAILER_COUNTRY_FLAG_IMAGE', String(255)),
    Column('RETAILER_TYPE_RETAILER_TYPE_CODE', Integer),
    Column('RETAILER_TYPE_RETAILER_TYPE_EN', String(255)),

    Column('UPDATED_AT', DateTime, server_default=func.now(), nullable=False),
)

retailer_contact = Table('RETAILER_CONTACT', meta, 
    Column('RETAILER_CONTACT_CODE_SK', Integer, primary_key=True, autoincrement=True),
    Column('RETAILER_CONTACT_CODE', Integer, nullable=False),

    Column('RETAILER_CONTACT_FIRST_NAME', String(255)),
    Column('RETAILER_CONTACT_LAST_NAME', String(255)),
    Column('RETAILER_CONTACT_JOB_POSITION_EN', String(255)),
    Column('RETAILER_CONTACT_EXTENSION', String(255)),
    Column('RETAILER_CONTACT_FAX', String(255)),
    Column('RETAILER_CONTACT_E_MAIL', String(255)),
    Column('RETAILER_CONTACT_GENDER', String(255)),

    Column('RETAILER_SITE_CODE', Integer, nullable=False),
    Column('RETAILER_SITE_CODE_SK', Integer, ForeignKey(retailer.c.RETAILER_SITE_RETAILER_SITE_CODE_SK, ondelete='cascade'), nullable=False),

    Column('UPDATED_AT', DateTime, server_default=func.now(), nullable=False),
)

sales_branch = Table('SALES_BRANCH', meta,
    Column('SALES_STAFF_CODE', Integer),
    Column('SALES_STAFF_FIRST_NAME', String),
    Column('SALES_STAFF_LAST_NAME', String),
    Column('SALES_STAFF_POSITION_EN', String),
    Column('SALES_STAFF_WORK_PHONE', String),
    Column('SALES_STAFF_EXTENSION', String),
    Column('SALES_STAFF_FAX', String),
    Column('SALES_STAFF_EMAIL', String),
    Column('SALES_STAFF_DATE_HIRED', Date),

    Column('SALES_BRANCH_CODE', Integer),
    Column('SALES_BRANCH_ADDRESS1', String),
    Column('SALES_BRANCH_ADDRESS2', String),
    Column('SALES_BRANCH_CITY', String),
    Column('SALES_BRANCH_REGION', String),
    Column('SALES_BRANCH_POSTAL_ZONE', String),

    Column('COUNTRY_COUNTRY_CODE', Integer),
    Column('COUNTRY_COUNTRY', String),
    Column('COUNTRY_LANGUAGE', String),
    Column('COUNTRY_CURRENCY_NAME', String),
)



def getSchemas() -> dict[str, Table]:
    return {
        'RETAILER': retailer,
        'RETAILER_CONTACT': retailer_contact,
        'SALES_BRANCH': sales_branch
    }

def getMeta()-> MetaData:
    return meta