import requests
import logging


class DDNS:
    def __init__(self, email, global_api_key, dns_record_name):
        self.__headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": global_api_key,
            "Content-Type": "application/json"
        }
        self.dns_record_name = dns_record_name
        self.domain_id = None
        self.dns_record_id = None
        self.dns_record_type = None
        self.__init_dns_record()

    def __init_dns_record(self):
        self.domain_id = self.__fetch_domain_id(self.__headers, self.__get_domain_name(self.dns_record_name))
        self.dns_record_id, self.dns_record_type, _ = self.__fetch_dns_record(self.__headers, self.domain_id, self.dns_record_name)

    def update_dns_record(self, new_ip):
        url = f"https://api.cloudflare.com/client/v4/zones/{self.domain_id}/dns_records/{self.dns_record_id}"
        data = {
            "type": self.dns_record_type,
            "name": self.dns_record_name,
            "content": new_ip,
            "ttl": 1,
            "proxied": False
        }
        try:
            response = requests.put(url, headers=self.__headers, json=data)
            response.raise_for_status()
            logging.info(f"DNS record updated successfully: {response.json()}")
        except requests.RequestException as e:
            logging.error(f"Failed to update DNS record: {e}")

    def get_record_content(self):
        return self.__fetch_dns_record(self.__headers, self.domain_id, self.dns_record_name)[2]

    @staticmethod
    def __get_domain_name(dns_record_name):
        return ".".join(dns_record_name.split(".")[-2:])

    @staticmethod
    def __fetch_domain_id(headers, domain_name):
        url = "https://api.cloudflare.com/client/v4/zones"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            for domain in response.json()["result"]:
                if domain["name"] == domain_name:
                    return domain["id"]
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve domain ID: {e}")
        return None

    @staticmethod
    def __fetch_dns_record(headers, domain_name_id, dns_record_name):
        url = f"https://api.cloudflare.com/client/v4/zones/{domain_name_id}/dns_records"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            for record in response.json()["result"]:
                if record["name"] == dns_record_name:
                    return record["id"], record["type"], record["content"]
        except requests.RequestException as e:
            logging.error(f"Failed to retrieve DNS record: {e}")
        return None, None, None

    @staticmethod
    def fetch_current_ip(dns_record_type):
        if dns_record_type == "A":
            url = "https://ip.3322.net/"
        elif dns_record_type == "AAAA":
            url = "https://6.ipw.cn"
        else:
            raise ValueError("Unsupported DNS record type.")
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text.strip()
        except requests.RequestException as e:
            logging.error(f"Failed to get IP address: {e}")
            return None
