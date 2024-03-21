from exporters import *

# This function returns a list of all the classes in the exporters module
# Only these classes will be used by the dependency manager
def get_exporter_classes():
    return [
        RetailerContactTable,
        RetailerTable,
        SalesBranchTable
    ]