import requests
import urllib.parse, urllib.error
import urllib.request, json

def icr_run(image_url):
    print("image_url", image_url)
    image_url_changed = str(image_url).replace("?","myIail@258")
    url = "https://iassistlabs.com/icr_image_url"
    print("image_url_changed", image_url_changed)
    payload={'image_url': str(image_url_changed)}
    files=[
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    return response.json()
    
def rc_api_run(vech_nu):
    print("vech_nu", vech_nu)
    url = "https://iassistlabs.com/icr_image_url"

    payload={'reg_no': str(vech_nu).lower()}
    files=[

    ]
    headers = {}
    try:
        response = requests.request("GET", url, headers=headers, data=payload, files=files,timeout = 8)
        return response.json()
    except:
        return {'error': 1,}
        
    