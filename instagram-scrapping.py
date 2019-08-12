#!/usr/bin/env python
# coding: utf-8

import json
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
import time
import xlsxwriter


driver = webdriver.Chrome('../chromedriver')
page= "pageid"   #Enter your page id here
url = 'https://www.instagram.com/{}/'.format(page)
driver.get(url)
driver.maximize_window()
for scroll in range(20):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

page = BeautifulSoup(driver.page_source, 'lxml')
script = page.findAll('script')[8]

page_json = script.text.split(' = ', 1)[1].rstrip(';')
data = json.loads(page_json)
profile = {}
# # ############## Profile Data ###############
page_data = data['entry_data']['ProfilePage'][0]
user_details = page_data['graphql']['user']
followers = user_details['edge_followed_by']['count']
following = user_details['edge_follow']['count']
full_name = user_details['full_name']
bio = user_details['biography']
Website = user_details['external_url']
user_id = user_details['id']
username = user_details['username']
profile_pic = user_details['profile_pic_url']
profile_pic_hd = user_details['profile_pic_url_hd'] 
business_prifile = user_details['is_business_account']
business_name = user_details['business_category_name']
private_profile = user_details['is_private']
verified_profile = user_details['is_verified']
fb_page = user_details['connected_fb_page']
insta_channel = user_details['has_channel']
no_of_posts = user_details['edge_owner_to_timeline_media']['count']
print("!!!!!!!!Profile details scrapped!!!!!!!")

profile.update({"username":username})
profile.update({"full_name":full_name})
profile.update({"followers":followers})
profile.update({"following":following})
profile.update({"no_of_posts":no_of_posts})
profile.update({"profile_pic":profile_pic})
profile.update({"profile_pic_hd":profile_pic_hd})
profile.update({"bio":bio})
profile.update({"Website":Website})
print("**"*40)
profile.update({"business_prifile":business_prifile})
profile.update({"business_name":business_name})
profile.update({"private_profile":private_profile})
profile.update({"verified_profile":verified_profile})
profile.update({"fb_page":fb_page})
profile.update({"insta_channel":insta_channel})

# # ########### POSTS DETAILS ###############

post_data = page.findAll('div', attrs ={'class':'_bz0w'})
post_details = []
counting = 0
for post_link in post_data:
    posts = {}
    post_links = post_link.find('a')
    post_links = post_links['href']
    post_links = "https://www.instagram.com" + str(post_links)
#     post_urls.append(post_links)

    posts.update({"post_links":post_links})
    driver.get(post_links)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    try:
        author = soup.find('a', attrs = {'class':'FPmhX notranslate nJAzx'}).text
    except:
        author = ''
    posts.update({"author":author})
    try:
        location = soup.find('a', attrs = {'class':'O4GlU'}).text
    except:
        location = ''
    posts.update({"location":location})
    try:
        text = soup.find('div', attrs = {'class':'C7I1f X7jCj'}).findAll('span')[0].text
    except:
        text = ''
    try:
        tags = soup.find('div', attrs = {'class':'C7I1f X7jCj'}).findAll('span')[0].findAll('a').text
    except:
        tags = ''
    caption = text + tags
   
    posts.update({"caption":caption})
    
    post_media = soup.find('div', attrs = {'class':'ZyFrc'})
    try:
        media = post_media.find('video')['src']
        posts.update({"media_type":'Video'})
    except:
        media = post_media.find('div', attrs = {'class': 'KL4Bh'}).find('img')['src']
        posts.update({"media_type":"Image"})
    posts.update({"media":media})
    counting+=1
    
    post_details.append(posts)
print("{} posts scrapped ".format(counting))

#********* Writing Data ***********#
workbook = xlsxwriter.Workbook('Instagram.xlsx')
worksheet = workbook.add_worksheet() 
bold = workbook.add_format({'bold': True})
size = workbook.add_format()
size.set_font_size(30)
worksheet.write(0,1,'Instagram Details',size)
worksheet.write(2,1,'username',bold)
worksheet.write(3,1,'Full name',bold)
worksheet.write(4,1,'Followers',bold)
worksheet.write(5,1,'Following',bold)
worksheet.write(6,1,'Total Posts',bold)
worksheet.write(7,1,'Profile pic',bold)
worksheet.write(8,1,'Hd Profile pic',bold)
worksheet.write(9,1,'Bio',bold)
worksheet.write(10,1,'Website url',bold)
worksheet.write(11,1,'Business prifile',bold)
worksheet.write(12,1,'Business name',bold)
worksheet.write(13,1,'private_profile',bold)
worksheet.write(14,1,'verified_profile',bold)
worksheet.write(15,1,'fb_page',bold)
worksheet.write(16,1,'insta_channel"',bold)


worksheet.write(2,2,profile['username'])
worksheet.write(3,2,profile['full_name'])
worksheet.write(4,2,profile['followers'])
worksheet.write(5,2,profile['following'])
worksheet.write(6,2,profile['no_of_posts'])
worksheet.write(7,2,profile['profile_pic'])
worksheet.write(8,2,profile['profile_pic_hd'])
worksheet.write(9,2,profile['bio'])
worksheet.write(10,2,profile['Website'])
worksheet.write(11,2,profile['business_prifile'])
worksheet.write(12,2,profile['business_name'])
worksheet.write(13,2,profile['private_profile'])
worksheet.write(14,2,profile['verified_profile'])
worksheet.write(15,2,profile['fb_page'])
worksheet.write(16,2,profile['insta_channel'])

worksheet.write(18,1,"!!!!!!!!!!!!!!!  Post Details starts from here !!!!!!!!!!!",bold)

worksheet.write(19,0,'S.No',bold)
worksheet.write(19,1,'post_links',bold)
worksheet.write(19,2,'author',bold)
worksheet.write(19,3,'location',bold)
worksheet.write(19,4,'Caption',bold)
worksheet.write(19,5,'Media type',bold)
worksheet.write(19,6,'Media link',bold)


count = 0
for post in post_details:
    count+=1
    worksheet.write(count+19,0, count) 
    worksheet.write(count+19,1, post['post_links']) 
    worksheet.write(count+19,2, post['author']) 
    worksheet.write(count+19,3, post['location'])
    worksheet.write(count+19,4, post['caption'])
    worksheet.write(count+19,5, post['media_type'])
    worksheet.write(count+19,6, post['media'])
    

print("!!!!!!! Data written on sheet Successfully !!!!!!")
workbook.close()
    
driver.quit()
    







