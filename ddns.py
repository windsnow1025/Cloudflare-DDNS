import requests
import json


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
        self.dns_record_content = None
        self.dns_record_type = None
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

    def get_dns_record(self):
        url = "https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(self.domain_name_id, self.dns_record_id)
        response = requests.get(url, headers=self.headers)
        dns_record = response.json()["result"]
        self.dns_record_content = dns_record["content"]
        self.dns_record_type = dns_record["type"]

    def update_dns_record(self):
        url = "https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(self.domain_name_id, self.dns_record_id)
        data = {
            "type": self.dns_record_type,
            "name": self.dns_record_name,
            "content": self.ip,
            "ttl": 1,
            "proxied": False
        }
        response = requests.put(url, headers=self.headers, data=json.dumps(data))
        print(response.json())

    def get_ip(self):
        if self.dns_record_type == "A":
            url = "http://whatismyip.akamai.com"
        elif self.dns_record_type == "AAAA":
            url = "http://6.ipw.cn"
        else:
            raise Exception("Unsupported DNS record type.")
        try:
            response = requests.get(url)
        except Exception as e:
            raise Exception(f"Failed to get {self.dns_record_type} record. {e}")
        self.ip = response.text
