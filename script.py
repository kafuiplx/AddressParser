__author__ = 'kafuinutakor'
from AddressParser.AddressParser import AddressParser

a = AddressParser()

a.Parse('350 Fifth Avenue New York, New York, 10118')

a.Parse('713 Central Avenue, Fort Dodge,  IA 50501, United States')

a.Parse('6401 West Clearwater Avenue, Kennewick,  WA 99336, United States')

a.Parse('1111 Western Dr Hartford, 53027-2722 United States')

a.Parse('7120 Homestead Rd Fort Wayne, 46814 United States')

# sample output
['zipcode', 'city', 'state_code', 'lat', 'lon', 'street']