import requests

BASE_URL = "https://dacs-prd.utshare.utsystem.edu/psc/DACSPRD/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_COMPONENT_FL.GBL"
COOKIE = "COOKIE_HERE"

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': COOKIE,  # Replace 'YOUR_COOKIE_HERE' with the actual cookie value
    'DNT': '1',
    'Origin': 'https://dacs-prd.utshare.utsystem.edu',
    'Referer': 'https://dacs-prd.utshare.utsystem.edu/psc/DACSPRD/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID%3aPTPPNAVCOL&scname=ADMN_MANAGE_CLASSES&PTPPB_GROUPLET_ID=UTD_SR_MANAGE_CLASSES&CRefName=ADMN_NAVCOLL_22',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': 'Android'
}

DATA = {
    'ICAJAX': '1',
    'ICNAVTYPEDROPDOWN': '0',
    'DERIVED_SSR_FL_SSR_VW_CLSCHD_OPT$81$': 'D'
}

class Requests:

    @classmethod
    def get_response_text(cls) -> str:
        """
        Sends request to UT API and returns response text
        :return str: Response text if successful else empty string
        """
        response: requests.Response = requests.post(BASE_URL, headers=HEADERS, data=DATA)
        response_code: int = response.status_code
        if response_code != 200:
            print(f"Unable to get response. Status code: {response_code}")
            return ""
        
        return response.text