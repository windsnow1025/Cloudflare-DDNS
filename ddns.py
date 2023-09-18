import os
import requests
import json
import time


class DDNS:
    def __init__(self, email, global_api_key, domain_name, dns_record_name):
        self.email = email
        self.global_api_key = global_api_key
        self.headers = {
            "X-Auth-Email": self.email,
            "X-Auth-Key": self.global_api_key,
            "Content-Type": "application/json"
        }
        self.domain_name = domain_name
        self.domain_name_id = None
        self.dns_record_name = dns_record_name
        self.dns_record_id = None
        self.ip = None

    def get_domain_id(self):
        url = "https://api.cloudflare.com/client/v4/zones"
        response = requests.get(url, headers=self.headers)
        for domain in response.json()["result"]:
            if domain["name"] == self.domain_name:
                self.domain_name_id = domain["id"]
                break

    def get_dns_record_id(self):
        url = "https://api.cloudflare.com/client/v4/zones/{}/dns_records".format(self.domain_name_id)
        response = requests.get(url, headers=self.headers)
        for dns_record in response.json()["result"]:
            if dns_record["name"] == self.dns_record_name:
                self.dns_record_id = dns_record["id"]
                break

    def update_dns_record(self):
        url = "https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(self.domain_name_id, self.dns_record_id)
        data = {
            "type": "A",
            "name": self.dns_record_name,
            "content": self.ip,
            "ttl": 1,
            "proxied": False
        }
        response = requests.put(url, headers=self.headers, data=json.dumps(data))
        print(response.json())

    def get_ip(self, url="http://whatismyip.akamai.com"):
        response = requests.get(url)
        self.ip = response.text


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
    ddns.get_ip()
    while True:
        ddns.get_ip()
        ddns.update_dns_record()
        time.sleep(60)


if __name__ == '__main__':
    main()
