import json
import time
import getpass
import urllib, base64
from io import BytesIO
from PIL import Image
import app.functions as functions
from selenium import webdriver
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


# Create your views here.
@csrf_exempt
def get_company_details(request):
    if request.method == 'OPTIONS':

        response = json.dumps('OK')
        return HttpResponse(response,
                            status = 200,
                            content_type = 'text/json',
                            headers = {
                                'Access-Control-Allow-Origin':'*',
                                'Access-Control-Allow-Headers':'*'
                            })

    if request.method == 'POST':

        payload = json.loads(request.body)
        company_name = payload['company-name']

        # starting chrome driver
        username = getpass.getuser()
        path_to_web_driver = '/home/'+username+'/Downloads/chromedriver_linux64/chromedriver'
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(path_to_web_driver, chrome_options=options)
        driver.get('chrome://newtab')
        
        # Searching company's website on google
        result = functions.search_website_url(driver, company_name)

        if result['status'] != 200:
            reponse = json.dumps(result['body'])
            return HttpResponse(response,
                                status = result['status'],
                                content_type='text/json',
                                headers = {
                                    'Access-Control-Allow-Origin':'*'
                                })

        website_url = result['body']
    
        # get the logo of website
        result = functions.get_logo(driver, website_url)

        if result['status'] != 200:
            response = json.dumps(result['body'])
            return HttpResponse(response,
                                status = result['status'],
                                content_type='text/json',
                                headers = {
                                    'Access-Control-Allow-Origin':'*'
                                })

        logo = result['body']

        # closing web driver
        driver.quit()

        # no of colours to detect in image
        no_of_colours = 10

        # detect colours
        result = functions.detect_colours(logo, no_of_colours)

        # converting logo to base64
        logo = Image.fromarray(logo)
        buf = BytesIO()
        buf.flush()
        logo.save(buf, format="png")
        buf.seek(0)
        string = base64.b64encode(buf.read())
        logo_uri = 'data:image/png;base64,' + urllib.parse.quote(string)

        # making response to be returned
        result['company_name'] = company_name
        result['website_url'] = website_url
        result['website_logo'] = logo_uri
        response = json.dumps(result)
    
    if response != None:
        return HttpResponse(response,
                            status=200,
                            content_type='text/json',
                            headers = {
                                'Access-Control-Allow-Origin':'*'
                            })
    response = json.dumps('Internal Server Error')
    return HttpResponse(
        response,
        status=500,
        content_type='text/json',
        headers = {
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Headers':'*'
        }
    )

# request = {
#     'method' : 'POST',
#     'body' : {
#         'company-name' : 'real favicon generator'
#     }
# }

# get_company_details(request)