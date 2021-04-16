import os
import argparse
import requests
import json
from tqdm import tqdm

API_TO_GET_RECORDS = "https://api.cloudflare.com/client/v4/zones/{selected_zone}/dns_records" #can add filter '?type=A'
API_TO_SET_RECORD = "https://api.cloudflare.com/client/v4/zones/{selected_zone}/dns_records/{record_id}"

def load_janjak2411_configuration(janjak2411_path=None) -> dict:
    if janjak2411_path is None and 'JANJAK2411_ROOT' not in os.environ:
        raise EnvironmentError("can't load configuraion from janjak2411")

    path_to_janjak2411 = janjak2411_path or os.environ['JANJAK2411_ROOT']

    path_to_configuration = os.path.join(path_to_janjak2411, 'PythonLab', 'configuraion',
                                         'dns_cloudflare_yjacob.json')
    with open(path_to_configuration, 'r') as f:
        configuration_dict = json.load(f)
    return configuration_dict

def get_all_dns_records(configuration_dict:dict, zone_name:str):
    head_authentication = configuration_dict['head_authentication']
    zone = configuration_dict['zone_by_name'][zone_name]

    url_to_get_all_records = API_TO_GET_RECORDS.format(selected_zone=zone)

    r = requests.get(url_to_get_all_records, headers=head_authentication)
    dns_records = r.json()['result']
    return dns_records

def get_local_ip_address():
    ip = requests.get('https://api.ipify.org').text
    return ip

def update_dns_ip_address(configuration_dict:dict, dns_records, ip_address, just_print_status=False):
    head_authentication = configuration_dict['head_authentication']

    for record in tqdm(dns_records):
        if record['type'] is not 'A':
            tqdm.write(f"Expected type: A in '{record['name']}' got: {record['type']}")
        elif record['content'] == ip_address:
            tqdm.write(f"The record '{record['name']}' is already set dedicated server IP.")
        else:
            record_id = record['id']
            zone_id = record['zone_id']
            record['content'] = ip_address
            body = json.dumps(record)
            url_to_set = API_TO_SET_RECORD.format(selected_zone=zone_id, record_id=record_id)
            if not just_print_status:
                r = requests.patch(url_to_set, data=body, headers=head_authentication)
                tqdm.write(f"Updated '{record['name']}' to dedicated server IP.")
            else:
                tqdm.write(f"JUST PRINTING: '{record['name']}' to dedicated server IP.")

def init_argparse():
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('--ip_address', help='ip address to set all domain, default local ip')
    parser.add_argument('--janjak2411_path', help='root to private repo, default from environ variable')
    parser.add_argument('--zone_name', default='yjacob.net')
    parser.add_argument('--just_print_status', action='store_true')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = init_argparse()

    configuration_dict = load_janjak2411_configuration(args.janjak2411_path)
    dns_records = get_all_dns_records(configuration_dict, args.zone_name)
    ip_address = args.ip_address or get_local_ip_address()

    update_dns_ip_address(configuration_dict, dns_records, ip_address, args.just_print_status)


