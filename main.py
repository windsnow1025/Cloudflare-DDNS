import json
import logging
import os
import time

import schedule

from ddns import DDNS


def load_config():
    if not os.path.exists('config.json'):
        config = {
            "email": input("Enter your email: "),
            "global_api_key": input("Enter your global API key: "),
            "dns_record_name": input("Enter your DNS record name (xxx.yyy.zzz): ")
        }
        with open('config.json', 'w') as f:
            json.dump(config, f)
    else:
        with open('config.json') as f:
            config = json.load(f)
    return config


def update_dns_record(ddns):
    try:
        record_content = ddns.get_record_content()
        current_ip = ddns.fetch_current_ip(ddns.dns_record_type)
        if current_ip != record_content:
            logging.info(f"Current IP {current_ip} is different from DNS record {record_content}. Updating...")
            ddns.update_dns_record(current_ip)
        else:
            logging.info("No update needed. IP address unchanged.")
    except Exception as e:
        logging.error(f"Error updating DNS record: {e}")


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    config = load_config()
    ddns = DDNS(config["email"], config["global_api_key"], config["dns_record_name"])

    schedule.every(10).seconds.do(update_dns_record, ddns=ddns)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
