import socket
import sys
import pprint
import nessus_file_reader as nfr
import csv
import glob, os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from ip2geotools.databases.noncommercial import DbIpCity
import progressbar
import time


#get nessus file
nessus_extension = '.nessus'

csv_extension = '.csv'

name_of_file = 'sensor001'

nessus_scan_file = name_of_file + nessus_extension

#get ip ans os from nessus files

file_for_pars = ""

# root = nfr.file.nessus_scan_file_root_element(file_for_pars)
# output_file = file_for_pars + csv_extension

def main():

    host_ip = []
    host_os = []
    domains = []
    city_name = []
    county = []
    latitude = []
    longitude = []
    nt_host = []

    for report_host in nfr.scan.report_hosts(root):
        #Get IP
        report_host_name = nfr.host.report_host_name(report_host)
        host_ip.append(report_host_name)
        #Get OS
        report_host_os = nfr.host.detected_os(report_host)
        if (report_host_os == None):
            report_host_os = "Unknown"
            host_os.append(report_host_os)
        else:
            report_host_os = report_host_os.splitlines()
            list_os = '|'.join(map(str, report_host_os))
            host_os.append(list_os)
        #Get url
        url = 'https://www.robtex.com/ip-lookup/' + report_host_name
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')
        try:
            table1 = soup.find('div', attrs={'class': 'infobox'}).find('ul', attrs={'class': 'scrollist'}).find('li').find('a').text
            domains.append(table1)
        except AttributeError:
            try:
                table1 = socket.gethostbyaddr(report_host_name)[0]
                domains.append(table1)
            except socket.herror:
                table1 = "Unknown"
                domains.append(table1)
      

        #Get info by ip
        response = DbIpCity.get(report_host_name, api_key='free')
        city_name.append(response.city)
        county.append(response.country)
        latitude.append(response.latitude)
        longitude.append(response.longitude)

        try:
            host = socket.gethostbyaddr(report_host_name)[0]
            nt_host.append(host)

        except socket.herror:
            host="Unknown"
            nt_host.append(host)
            continue

    host = {
        'ip': host_ip,
        'mac': '',
        'nt_host': '',
        'os': host_os,
        'dns': domains,
        'owner': '',
        'priority': '',
        'lat': latitude,
        'long': longitude,
        'city': city_name,
        'country': county,
        'bunit': '',
        'category': '',
        'pci_domain': '',
        'is_expected': '',
        'should_timesync': '',
        'should_update': '',
        'requires_av': '',
        'cim_entity_zone': '',
    }

    df = pd.DataFrame(host)
    df.to_csv(output_file, header=True, index=False)

os.chdir('../nesus_scan/')

for file_for_pars in glob.glob("*.nessus"):

    root = nfr.file.nessus_scan_file_root_element(file_for_pars)


    file_without_ext = os.path.splitext(file_for_pars)[0]


    output_file = file_without_ext + "_by_IP" + csv_extension


    print("Pars ", file_for_pars)
    main()


