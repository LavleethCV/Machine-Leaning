import pandas as pd
from apartment_buliding import apbul_apartments
from apartment_complex import apcom_apartments
from commercial_apartments import comm_apartments
from condominium_complex import cc_apartments
from residential_apartments import resap_apartments
from gated_community import gc_apartments

data1 = apbul_apartments()
data2 = apcom_apartments()
data3 = comm_apartments()
data4 = cc_apartments()
data5 = resap_apartments()
data6 = gc_apartments()

apartments = pd.concat([data1, data2, data3, data4, data5, data6], axis=0)
print(apartments)
apartments.to_excel('apartments.xlsx')
