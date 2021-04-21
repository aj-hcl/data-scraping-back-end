import requests
from flask_restful import Resource, reqparse
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

class Scraper(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('url',
        type = str,
        required = True,
        help = "this field cannot be left blank"
    )

    def post(self):
        args = Scraper.parser.parse_args()

        options = Options()
        options.headless = True
        try:
            #the chromedriver executable should be installed in the src folder
            driver = webdriver.Chrome('./chromedriver', chrome_options=options)

        except:
            return {"message":"Error getting chrome driver, is it installed?"}
        try:
            driver.get(args['url'])
        except:
            return {"message":"Invalid URL"}



        time.sleep(5)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        #try nhl standings
        tags = []
        try:
            for i in soup.findAll('div', {'class': 'responsive-datatable__pinned'}):
                nhl_table = i.find("tbody")
                for t in nhl_table.findAll("tr"):
                    team_name = t.find('span', {'class':'team--name'}).text
                    tag = {}
                    tag['games_played'] = t.find('td', attrs={'data-col':'1'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['wins'] = t.find('td', attrs={'data-col':'2'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['losses'] = t.find('td', attrs={'data-col':'3'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['OT_losses'] = t.find('td', attrs={'data-col':'4'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['points'] = t.find('td', attrs={'data-col':'5'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['points_percentage'] = t.find('td', attrs={'data-col':'6'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['regulation_wins'] = t.find('td', attrs={'data-col':'7'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['regulation_and_OT_wins'] = t.find('td', attrs={'data-col':'8'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['goals_for'] = t.find('td', attrs={'data-col':'9'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['goals_against'] = t.find('td', attrs={'data-col':'10'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['goal_differential'] = t.find('td', attrs={'data-col':'11'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['home'] = t.find('td', attrs={'data-col':'12'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['away'] = t.find('td', attrs={'data-col':'13'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['shoot_out'] = t.find('td', attrs={'data-col':'14'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['last10'] = t.find('td', attrs={'data-col':'15'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)
                    tag = {}
                    tag['streak'] = t.find('td', attrs={'data-col':'16'}).find('span').text
                    tag['tag_key'] = team_name
                    tags.append(tag)

            if tags: #if teams is not empty, else try a different site
                return tags
        except:
            pass
        
        tags = []
        try:
            head = soup.find('thead')
            labels = []
            for c in head.findAll('th'):
                labels.append(c.text.strip())
            body = soup.find('tbody')
            for i in body.findAll('tr'):
                colIndex = 0
                name = ''
                
                for j in i.findAll('td'):
                    tag = {}
                    if colIndex == 0:
                        name_tag = j.find('div',{'class': 'd3-o-club-fullname'})
                        if not name_tag:
                            name_tag = j.find('a',{'class': 'd3-o-player-fullname nfl-o-cta--link'})
                        name = name_tag.text.strip()
                        colIndex += 1
                        continue
                    tag[labels[colIndex]] = j.text.strip()
                    tag['tag_key'] = name
                    tags.append(tag)
                    colIndex += 1
                

            if tags: #if teams is not empty, else try a different site
                return tags
        except Exception as e:
            pass



        return{"message":"Could not scrape data from URL"}

        divs = soup.find_all("div")

        tables = soup.find_all("table")

        return {"div_tags:" : [str(d) for d in divs], "table_tags:": [str(t) for t in tables]}
