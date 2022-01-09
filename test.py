import sys
from pprint import pprint
import nessus_file_reader as nfr
import csv
import requests
import xml.etree.ElementTree as etree
import os


import socket
import pandas as pd


nessus_scan_file = 'sensor001.nessus'
report_host_name = ''


root = nfr.file.nessus_scan_file_root_element(nessus_scan_file)
#
# for child_of_root in root.iter('ReportItem'):
#     print('%s\tnText:', child_of_root.items())

ip = []
service = []
port = 0
port_value = []
host_os = []

test = [1,2,3,4,5]




for report_host in nfr.scan.report_hosts(root):
    report_host_name = nfr.host.report_host_name(report_host)
    ip.append(report_host_name)

    print(report_host_name)
    for keys in root.iter('ReportItem'):
        port = keys.get('svc_name')
   # print(port_value)

    # print(port)
        port_value.append(keys.get('svc_name'))






    #list_port = '|'.join(map(str, port))
# print(port_value)

#port_value.append(port)
#print(port_value)
#port_value = ([port for reportItem in root.iter('ReportItem')])
#

host = {


    'ex': {
        'port': ip,
        'serv': str(port_value)
    }
}

#         keyList = ["ip"]
#
#         # initialize dictionary
#         d = {}
#
#     # iterating through the elements of list
#         for i in keyList:
#             d[i] = ip
    #






# df = pd.DataFrame(host['ex'])
# df.to_csv('test.csv', header=True, index=False)


    # port_value.append(int(port))






    # for reportItem in root.iter('ReportItem'):
    #     port = int(reportItem.get('port'))
    #     port_value.append(int(port))

    # try:
    #     sockets = socket.getservbyport(port, 'tcp')
    #
    #     service.append(sockets)
    # except OSError:
    #         continue
#
# listKeys = ["Paras", "Jain", "Cyware"]
#
# # using zip() function to create a dictionary
# # with keys and same length None value
#
# StudentDict = dict.fromkeys(listKeys, ip)
#
# # print dict
# print(StudentDict)
#
#
#

#

#
#         protocols=reportItem.get('protocol')
#         protocol.append(protocols)
#
#         # print(ports,protocols)
#         #print(port,protocol)
#
#
#
# for i in port:
#     try:
#             sockets = socket.getservbyport(i, 'tcp')
#             soc.append(sockets)
#
#             #print(sockets)
#
#     except OSError:
#         continue




# print(socket)
#print("Name of the service running at port number %d : %s" % (port, protocol))



    #print(test)

# report_items_per_host = nfr.host.report_items(report_host)
# for report_item in report_items_per_host:
#     plugin_id = int(nfr.plugin.report_item_value(report_item, 'pluginID'))
#     risk_factor = nfr.plugin.report_item_value(report_item, 'risk_factor')
#     plugin_name = nfr.plugin.report_item_value(report_item, 'pluginName')
#     print('\t', plugin_id, '  \t\t\t', risk_factor, '  \t\t\t', plugin_name)



# for report_host in nfr.scan.report_hosts(root):
#
#     host_os = []
#     host_dns = []
#     domains = []
#     report_host_name = nfr.host.report_host_name(report_host)
#     report_host_os = nfr.host.detected_os(report_host)
#
#     url = 'https://www.robtex.com/ip-lookup/' + report_host_name
#     # url = 'https://www.robtex.com/ip-lookup/193.29.204.67'
#     print(url)
#     print(host_os)
#     page = requests.get(url)
#     # print(page)
#     soup = BeautifulSoup(page.text, 'lxml')
#     try:
#         table1 = soup.find('div', attrs={'class': 'infobox'}).find('ul', attrs={'class': 'scrollist'}).find('li').find(
#             'a').text
#
#         domains.append(table1)
#
#         list_domains = '|'.join(map(str, domains))
#
#         if (table1 == None):
#             continue
#     except AttributeError:
#         continue
#
#     report_host_os = report_host_os.splitlines()
#
#     list_os = '|'.join(map(str, report_host_os))
#
#     if (report_host_os == None):
#         report_host_os = "Unknown"
#         host_os.append(report_host_os)
#     else:
#         host_os.append(report_host_os)
#
#     hosts[str(report_host_name)] = {
#
#         "dns": list_domains,
#         "os": list_os
#     }
#     print(list_domains)
#
# header = ['ip', 'os', 'dns']
#
# with open('report.csv', 'w') as f:
#     # create the csv writer
#     writer = csv.DictWriter(f, header)
#     # writer.writerow(header)
#     writer.writeheader()
#     # write a row to the csv file
#
#     for k in hosts:
#         writer.writerow({field: hosts[k].get(field) or k for field in header})

    # for ip in hosts:
    #     print(ip,type(ip))
    #     writer.writerow(ip)
    #     for attr in hosts[ip]:
    #         print(hosts[ip][attr])
    #         #writer.writerow(hosts[ip].values())

    # print(type(report_host_name))
    # print(report_host_name,hosts[report_host_name]['os'])

# for ip in hosts:
#     print(ip)
#     for attr in hosts[ip]:
#         print(hosts[ip][attr])

# pprint.pprint("{0}, {1}, {2}".format(hosts.keys(), hosts[report_host_name]['dns'], hosts[report_host_name]['os']))


# csv_file.close()
# print(f'host name: {report_host_name}')
# print(f'OS: {report_host_os}')

# IP_OS["IP"].append(report_host_name)

# IP_OS["OS"].append(report_host)

# print(IP_OS)
