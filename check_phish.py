import requests

API_BASE_URL = "https://developers.bolster.ai/api/neo"
API_KEY = "0bfo9suxioilwvoma309avijj5hxsi7iegif1mzyik44bk3v8i8yuexae8580wd6"

def submit_scan(url, scan_type):
    """Returns dictionary with jobID if successful"""
    try:
        response = requests.post(
            'https://developers.bolster.ai/api/neo/scan',
            json={
                'apiKey': API_KEY,
                'urlInfo': {'url': url},
                'scanType': scan_type
            }
        )
        return response.json()  # Should return {'jobID': '...', ...}
    except Exception as e:
        return {'error': str(e)}

def check_scan_status(job_id, insights):
    """Returns dictionary with disposition/verdict"""
    try:
        response = requests.post(
            'https://developers.bolster.ai/api/neo/scan/status',
            json={
                'apiKey': API_KEY,
                'jobID': job_id,
                'insights': insights
            }
        )
        return response.json()  # Should return {'disposition': '...', ...}
    except Exception as e:
        return {'error': str(e)}