import socket
from ip2geotools.databases.noncommercial import DbIpCity

import requests
import xml.etree.ElementTree as etree
import os
from bs4 import BeautifulSoup
import glob
import pandas as pd
import numpy as np



def run_bidlocode():
    for report in root:

        ip = ''
        service = []
        os = []
        domains = []
        bunit = []
        owner = []
        asn = []
        latitude = ''
        longitude = ''
        city_name = ''
        county = ''
        host = {

        }

        email_from_file = {
            'sensor001': 'sprokopenko@ncscc.gov.ua',
            'sensor003': 'portalinfo@pfu.gov.ua|dpicpopfu@ukr.net|info@pfu.gov.ua',
            'sensor004': 'PravdivyOP@cvk.gov.ua|Striganov@cvk.gov.ua',
            'sensor005': 'tvuz10@dsszzi.gov.ua',
            'sensor006': '3tvuz@dsszzi.gov.ua',
            'sensor007': 'admin@vin.gov.ua',
            'sensor008': '00100@dn.gov.ua',
            'sensor009': 'adm@zoda.gov.ua|nav@zoda.gov.ua',
            'sensor010': 'info@loga.gov.ua',
            'sensor011': 'admin@mk.gov.ua',
            'sensor012': 'pasko@nads.gov.ua|neshchadym@nads.gov.ua',
            'sensor013': 'danilov@sm.gov.ua',
            'sensor014': 'obladm@kharkivoda.gov.ua|semeney@kh.gov.ua|sytnik@kharkivoda.gov.ua',
            'sensor015': 'v.smolienko@khoda.gov.ua',
            'sensor016': 'chernihiv@dsszzi.gov.ua|anton@regadm.gov.ua',
            'sensor017': 'aan@gp.gov.ua|ks@gp.gov.ua',
            'sensor018': 'ssh@sdfm.gov.ua|ssh@fiu.gov.ua|avpmail@fiu.gov.ua|vd@fiu.gov.ua',
            'sensor019': 'it_telecom@treasury.gov.ua|office@treasury.gov.ua',
            'sensor020': 'uz_di@mvs.gov.ua',
            'sensor021': 'vzi@dmsu.gov.ua|noc@uss.gov.ua',
            'sensor022': 'yu.panchenko@kbp.aero|t.khomenko@kbp.aero',
            'sensor023': 'plis@dsns.gov.ua',
            'sensor024': 'root@spfu.gov.ua',
            'sensor025': 'IT@dbr.gov.ua',
            'sensor027': 'anton.strevaliuk@kmda.gov.ua|sergiy.batyus@kmda.gov.ua',
            'sensor028': 'd.v.panchenko@msp.gov.ua',
            'sensor029': 'sergiy.lypnik@mev.gov.ua',
            'sensor030': 'it-security@mfa.gov.ua'
        }

        bunit_from_file = {
            'sensor001': '(rnbo) National Security and Defense Council of Ukraine',
            'sensor003': '(pfu) Pension Fund of Ukraine',
            'sensor004': '(cvk) Central Election Commission',
            'sensor005': 'ODA Miropil',
            'sensor006': 'ODA Mirgorod',
            'sensor007': 'ODA Vinnitsa',
            'sensor008': 'ODA Donetsk',
            'sensor009': 'ODA Zaporizha',
            'sensor010': 'ODA Lugansk',
            'sensor011': 'ODA Mikolaiv',
            'sensor012': '(nads) National Agency of Ukraine for Civil Service',
            'sensor013': 'ODA Sumy',
            'sensor014': 'ODA Kharkiv',
            'sensor015': 'ODA Kherson',
            'sensor016': 'ODA Chernigiv',
            'sensor017': '(gpu) Office of the Prosecutor General of Ukraine',
            'sensor018': '(fmu) Financial intelligence',
            'sensor019': '(dkzu) Treasury',
            'sensor020': '(mvs) Ministry of Internal Affairs',
            'sensor021': '(dmsu) State Migration Service',
            'sensor022': '(dpma boryspil) Boryspil International Airport',
            'sensor023': '(dsns) State Emergency Service of Ukraine',
            'sensor024': '(fdm) State Property Fund of Ukraine',
            'sensor025': '(dbr) State Bureau of Investigation',
            'sensor027': '(kmda) Kyiv City State Administration',
            'sensor028': '(mspu) Ministry of Social Policy of Ukraine',
            'sensor029': '(meu) Ministry of Energy',
            'sensor030': '(mzs) Ministry of Foreign Affairs'
        }

        for report_host in report:

            # GET IP
            if 'name' in report_host.attrib.keys():
                ip = report_host.attrib['name']

                service = []
                list_service = []
                list_os = []
                os = []
                for report_item in report_host:

                    # GET SERVICE
                    if 'svc_name' in report_item.attrib.keys():
                        service_name = report_item.attrib['svc_name']

                        if "?" in service_name:

                            list_service.append((service_name.rstrip(service_name[-1])))
                            service = np.unique(list_service)
                            service = '|'.join(map(str, service))
                        else:
                            list_service.append(service_name)
                            service = np.unique(list_service)
                            service = '|'.join(map(str, service))

                    # GET OS

                    for host_properties in report_item:

                        if 'os' in host_properties.attrib.values():
                            # print(host_properties.text)
                            operation_system = host_properties.text

                            list_os.append(operation_system)

                            os = '|'.join(map(str, list_os))

                #GET LOCATION


                response = DbIpCity.get(ip, api_key='free')
                city_name =response.city.split(' ')[0]
                county = response.country
                latitude = response.latitude
                longitude = response.longitude




                # GET DOMAIN AND BUNIT

                list_domains = []
                bunit_list = []
                asn_list = []

                url = 'https://www.robtex.com/ip-lookup/' + ip
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'lxml')


                # GET ASN
                try:
                    tablle_asn = soup.find('table', attrs={'class': 'l0'}).find_all('td')
                    asn_list.append(tablle_asn[14].text)

                    asn = '|'.join((map(str, asn_list)))

                except:
                    tablle_asn = "unknown"

                    asn = '|'.join(map(str, tablle_asn))


                #GET DOMAINS
                try:
                    tablle_dns = soup.find('div', attrs={'class': 'infobox'}).find('ul', attrs={'class': 'scrollist'}).find(
                        'li').find('a').text

                    # print(tablle_dns)
                    list_domains.append(tablle_dns)


                    domains = '|'.join(map(str, list_domains))
                except:

                    try:

                        tablle_dns = socket.gethostbyaddr(ip)[0]

                        list_domains.append(tablle_dns)

                        domains = '|'.join(map(str, list_domains))


                    except socket.herror:

                        tablle_dns = "unknown"

                        list_domains.append(tablle_dns)

                        domains = '|'.join(map(str, list_domains))

                # GET BUNIT
                bunit = ''
                owner = ''
            if file_without_ext in bunit_from_file.keys():
                bunit = bunit_from_file[file_without_ext]
                # GET EMAIL
            if file_without_ext in email_from_file.keys():
                owner = email_from_file[file_without_ext]



            host.update({
                ip: {
                    'mac': '',
                    'nt_host': '',
                    'os': os,
                    'dns': domains,
                    'owner': owner,
                    'priority': '',
                    'lat': latitude,
                    'long': longitude,
                    'city': city_name,
                    'country': county,
                    'bunit': bunit,
                    'category': service,
                    'pci_domain': '',
                    'is_expected': '',
                    'should_timesync': '',
                    'should_update': '',
                    'requires_av': '',
                    'cim_entity_zone': '',
                    'asn': asn,

                }
            })




    df = pd.DataFrame(host)

    df = df.transpose()
    df.index.name = 'ip'

    df.to_csv(output_file, header=True, index=True)


os.chdir('../nesus_scan')  # DIRECTORY WITH .nessus


# for file_for_pars in glob.glob("*.nessus"):

# file_for_pars = "sensor001.nessus"
#

file_for_pars = 'sensor022.nessus'
tree = etree.parse(file_for_pars)

root = tree.getroot()

csv_extension = '.csv'

file_without_ext = os.path.splitext(file_for_pars)[0]

output_file = file_without_ext + "_public_by_IP_assets_nessus" + csv_extension
# output_file = 'test.csv'

print("Pars ", file_for_pars)

run_bidlocode()