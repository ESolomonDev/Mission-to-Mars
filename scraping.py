
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt
#import pandas to read html
import pandas as pd

def scrape_all():
    #set up splinter
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager(version="99.0.4844.51").install()}
    #set headless to false to see splinter in action
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        #hemipheres data 
        "hemisphere": scrape_hemispheres(browser),
    }

    # Stop webdriver and return data
    browser.quit()
    return data

#pass the browser obj into func for scope
def mars_news(browser):
    # Visit the mars nasa news site
    # Convert the browser html to a soup object and then quit the browser
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #set up HTML parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #try block for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    #if attribute error is thrown return nothing insted of other return statement
    except AttributeError:
        return None , None    

    #return scraped data
    return news_title, news_p

# Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1] #indexing changed to click second button
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        #img_url_rel
    #AttributeError occures when script refers to invalid attribute
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    #return the absolute URL
    return img_url

# Scraping an HTML table / Mars Facts 

def mars_facts():
    try:    
        #read_html function returns a list of tables found in the HTML, index 0 pulls first table it incounters
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    #baseException is used to catch multiple errors ie general error thrown... thrown might be a JAVA spesific term
    except BaseException:
        return None

    #set up the dataframe
    df.columns=['description', 'Mars', 'Earth']
    #change the description column into the DF index
    df.set_index('description', inplace=True)
    
    #return the converted the DF back to html
    return df.to_html(classes="table table-striped")

#scrape hemispheres
def scrape_hemispheres(browser):

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    #Create a list to hold the images and titles.
    hemisphere_image_urls = []
    html = browser.html

    #reimport soup for some reasons
    from bs4 import BeautifulSoup as soup

    soup = soup(html, "html.parser")

    #try except block for error handling
    try:
        div_items = soup.find_all("div", class_ = "item")
        for div_item in div_items:
            #empty dictionary for each hemisphere div
            hemisphere = {'img_url':'','title':''}
            #append relative url onto url to get img url
            img_url = url + div_item.a.get("href")
            #visit url in splinter
            browser.visit(img_url)
            #parse the html data
            html_sub = browser.html
            soup = soup(html_sub, "html.parser")
            #get the jpeg relative url 
            relative_jpeg_url = soup.find("li").a.get("href")
            #append the jpeg url onto url
            jpeg_url = url + relative_jpeg_url
            #pass jpeg url into hemisphere dictionary
            hemisphere['img_url']=(jpeg_url)
            #find the title text
            title = soup.find("h2", class_="title").text
            #pass the title text into the hemishpere dictionary
            hemisphere['title']=(title)
            #append the hemisphere dictionary into hemi img url list
            hemisphere_image_urls.append(hemisphere)
    except AttributeError:
        return None

    #return hemi img url list
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())