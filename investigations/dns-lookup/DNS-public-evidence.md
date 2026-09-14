# DNS capture evidence for public sharing

This table transcribes selected observations from a guided Wireshark exercise. It is not an original packet capture or an unmodified screenshot. Device addresses and identifiers are omitted, and endpoints are represented by roles.

| Packet | Source | Destination | Observation |
| --- | --- | --- | --- |
| 502 | Lab computer | DNS server | A query requesting IPv4 addresses for example.com |
| 503 | DNS server | Lab computer | A response returning 104.20.23.154 and 172.66.147.243 |
| 504 | Lab computer | DNS server | AAAA query requesting IPv6 addresses for example.com |
| 505 | DNS server | Lab computer | AAAA response returning IPv6 addresses |

## Evidence limits
The table is based on the screenshots reviewed during the exercise. The original capture file is not attached. The DNS answers do not establish address ownership, website access, or website safety.

## Privacy treatment
Private IP addresses, MAC addresses, network-adapter identifiers and unrelated domain lookups from the screenshots are not reproduced. The original screenshots have not been edited and are not included in this public-sharing evidence file.

