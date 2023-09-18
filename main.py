import os
import json
import time
from ddns import DDNS


def main():
    if not os.path.exists('config.json'):
        email = input("Enter your email: ")
        global_api_key = input("Enter your global API key: ")
        domain_name = input("Enter your domain name: ")
        dns_record_name = input("Enter your DNS record name: ")
        config = {
            "email": email,
            "global_api_key": global_api_key,
            "domain_name": domain_name,
            "dns_record_name": dns_record_name
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)
    else:
        with open('config.json') as f:
            config = json.load(f)

    ddns = DDNS(config["email"], config["global_api_key"], config["domain_name"], config["dns_record_name"])
    ddns.get_domain_id()
    ddns.get_dns_record_id()
    while True:
        ddns.get_dns_record()
        try:
            ddns.get_ip()
            if ddns.ip != ddns.dns_record_content:
                ddns.update_dns_record()
        except Exception as e:
            print(e)
        time.sleep(10)


if __name__ == '__main__':
    main()
