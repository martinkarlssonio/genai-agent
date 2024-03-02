"""
This tool allows the AI Agent to perform nslookup on a domain.
"""

def nsLookup(domain: str) -> dict:
    #import subprocess
    import requests

    try:
        import socket

        ip_list = []
        ais = socket.getaddrinfo(domain,0,0,0,0)
        for result in ais:
            ip_list.append(result[-1][0])
            ip_list = list(set(ip_list))
        return {"ip": ip_list}
    except Exception as e:
        return f"Error occurred while performing nslookup: {e.output}"