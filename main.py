import json
import logging
import os
import time
from ddns import DDNS


def load_config():
    if not os.path.exists('config.json'):
        configs = []
        while True:
            config = {
                "email": input("Enter your email: "),
                "global_api_key": input("Enter your global API key: "),
                "dns_record_name": input("Enter your DNS record name (e.g., sub.domain.com): ")
            }
            configs.append(config)

            another = input("Do you want to add another record? (y/n): ")
            if another.lower().startswith('n'):
                break

        with open('config.json', 'w') as f:
            json.dump(configs, f)
    else:
        with open('config.json') as f:
            configs = json.load(f)
    return configs


def update_dns_records(ddns_objects):
    for ddns in ddns_objects:
        try:
            record_content = ddns.get_record_content()
            current_ip = ddns.fetch_current_ip(ddns.dns_record_type)
            if current_ip != record_content and current_ip is not None:
                logging.info(f"{ddns.dns_record_name} - Current IP {current_ip} is different from DNS record {record_content}. Updating...")
                ddns.update_dns_record(current_ip)
            else:
                logging.info(f"{ddns.dns_record_name} - IP address unchanged.")
        except Exception as e:
            logging.error(f"Error updating DNS record: {e}")


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    configs = load_config()
    ddns_objects = [DDNS(config["email"], config["global_api_key"], config["dns_record_name"]) for config in configs]
    logging.info("DNS records initialized successfully.")

    while True:
        update_dns_records(ddns_objects)
        time.sleep(60)


if __name__ == '__main__':
    main()
