import re
import requests
import numpy as np
import urllib, base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans
from skimage.color import rgb2lab, deltaE_cie76
from selenium.webdriver.common.keys import Keys

def search_website_url(driver, company_name):

    # searching company name on google
    google_search_url = 'https://www.google.com/search?q='
    driver.get(google_search_url + company_name)
    company_name = re.sub('[^\w]','',company_name)

    # searching website url from obtained results
    search_results = driver.find_elements_by_class_name('g')
    website_url = ''
    for search_result in search_results:
        try:
            url = search_result.find_element_by_class_name('iUh30').text
            url = url if url.find(' ')==-1 else url[:url.find(' ')]
            url_filtered = url.replace('-','')
            if company_name in str(url_filtered):
                website_url = url
                break
        except NoSuchElementException:
            continue

    if website_url == '':
        return {
            'body' : 'website_url',
            'status' : 404
        }
    
    return {
        'body' : website_url,
        'status' : 200
    }

def get_logo(driver, website_url):

    # checking if favicon is directly accessible
    path_to_favicon = '/favicon.ico'
    response = requests.get(website_url + path_to_favicon, stream=True)
    logo = ''

    if response.status_code != 200:
        # traversing website to find logo
        try:
            driver.get(website_url)
            logo_url = driver.find_element_by_css_selector('img').get_attribute('src')
            # if image path is relative path
            if logo_url[0] == '/':
                logo_url = website_url + logo_url
            response = requests.get(logo_url, stream=True)
        except:
            return {
                'body' : 'logo',
                'status' : 404
            }
    
    logo = Image.open(BytesIO(response.content))
    logo = np.array(logo)
    return {
        'body' : logo,
        'status' : 200
    }

def detect_colours(img, number_of_colors):

    # detecting clusters in image using k-means
    modified_img = img.reshape(img.shape[0]*img.shape[1], 4)
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_img)

    # counting occurence of different colours
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    
    # removing transparent color(s)
    length = len(counts.keys())
    colors_to_remove = []

    for i in range(length):
        if int(center_colors[i][3] == 0):
            counts.pop(i)
            colors_to_remove.append(i)
       
    center_colors = np.delete(center_colors, colors_to_remove, axis=0)

    # getting hex value of colours
    hex_colors = [RGBA2HEX(center_colors[i]) for i in range(len(center_colors))]

    # plotting a pie-chart
    plt.figure(figsize = (8, 6))
    plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
    fig = plt.gcf()
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = 'data:image/png;base64,' + urllib.parse.quote(string)
    
    # mapping counts' keys to center_colors' indices
    counts = dict(sorted(counts.items(), reverse=True))
    counts_new = {}
    for i in range(len(center_colors)):
        counts_new.__setitem__(i, counts.popitem()[1])
    
    # sorting in descending order of % colour occurence
    counts_new = dict(sorted(counts_new.items(), key=lambda item:item[1], reverse=True))
    counts_new = list(counts_new.items())
    
    return {
        'pie_chart_uri': uri,
        'center_colors': center_colors.tolist(),
        'counts_new': counts_new
    }

def RGBA2HEX(color):
    return "#{:02x}{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]), int(color[3]))