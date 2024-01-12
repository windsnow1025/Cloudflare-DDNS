# Cloudflare DDNS

## Usage

### Requirements

Recommended: Windows 11 x64

### Basic

Global API Key: [https://dash.cloudflare.com/profile/api-tokens](https://dash.cloudflare.com/profile/api-tokens)

### Advanced

IPv4 and IPv6 Address Checking API changeable in `ddns.py` - `fetch_current_ip()`.

DNS Record update interval changeable in `main.py` - `main()`.

## Development

### Requirements

Recommended: Python 3.12

### Build

```bash
pip install -r requirements.txt
```

```bash
pyinstaller --onefile main.py
```


