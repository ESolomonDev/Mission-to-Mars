#!/usr/bin/env python
# coding: utf-8

# In[164]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#import pandas to read html
import pandas as pd


# In[165]:


executable_path = {'executable_path': ChromeDriverManager(version="98.0.4758.102").install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[166]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[167]:


#set up HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[168]:


slide_elem


# In[169]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[170]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[171]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[172]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1] #indexing changed to click second button
full_image_elem.click()


# In[173]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[174]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[175]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Scraping an HTML table

# In[176]:


#read_html function returns a list of tables found in the HTML, index 0 pulls first table it incounters
df = pd.read_html('https://galaxyfacts-mars.com')[0]
#set up the dataframe
df.columns=['description', 'Mars', 'Earth']
#change the description column into the DF index
df.set_index('description', inplace=True)
df


# In[177]:


#convert the DF back to html
df.to_html()


# ## D1: Scraope High-Resolution Mars' Hemisphere Images and Titles

# ### Hemispheres

# In[178]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[179]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html =  browser.html
soup = soup(html, "html.parser")
#hemisphere_image_urls = soup.find_all("a", class_='itemLink product-item')
div_items = soup.find_all("div", class_ = 'item')
len(div_items)


# In[180]:


div_items[0].a.get("href")


# In[181]:


#loop through array of each div_items hemisphere 
for div_item in div_items:
    #kept haveing to reimport soup in testing
    from bs4 import BeautifulSoup as soup
    
    #empty dic to store scrape
    hemisphere = {'img_url':'','title':''}
    #print relative link
    #print(div_item.a.get("href"))
    #append the relative link onto url
    img_url = url + div_item.a.get("href")
    #print(img_url)
    #tell splinter to visit each url
    browser.visit(img_url)
    html_sub = browser.html
    soup = soup(html_sub, "html.parser")
    relative_jpeg_url = soup.find("li").a.get("href")
    jpeg_url = url + relative_jpeg_url
    #print(jpeg_url)
    
    hemisphere['img_url']=(jpeg_url)
    
    title = soup.find("h2", class_="title").text #.split(" | ")
    #print(title)
    
    hemisphere['title']=(title)
    #print(hemisphere)
    
    hemisphere_image_urls.append(hemisphere)
    #print("-----------")

#test prints
#import pprint
#pprint.pprint(hemisphere_image_urls)


# In[182]:


#print(hemisphere_image_urls[0].find('img')["src"])


# In[183]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[184]:


#end the splinter browser
browser.quit()


# In[ ]:




