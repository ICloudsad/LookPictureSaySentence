
import requests
from lxml import etree
import time
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.action_chains import ActionChains

import openpyxl
from selenium import webdriver


class Spider:

    def __init__(self):
        self.chrome = webdriver.Chrome()
        self.headers = {
            "Cookie": "JSESSIONID=ABAAAECAAEBABII8E8694F8E7B19D5E2D83D3A810983276; WEBTJ-ID=20220403123440-17fedb4257c66a-0dcf3cabf66607-56171958-1049088-17fedb4257d679; RECOMMEND_TIP=true; user_trace_token=20220403123441-709cd056-8e0c-4afc-8c23-63063cadbd46; LGUID=20220403123441-bdbd32d7-8dbd-4e6f-9ef9-bff6deb95739; _ga=GA1.2.1398676597.1648960481; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1648960481; LGSID=20220403123441-0843c81f-dc92-4b55-8db9-1021e9e124e5; privacyPolicyPopup=false; _gid=GA1.2.61558583.1648960482; sajssdk_2015_cross_new_user=1; sensorsdata2015session=%7B%7D; index_location_city=%E5%85%A8%E5%9B%BD; X_MIDDLE_TOKEN=6786a16ea0188c64d011ed80cd2e3d00; __lg_stoken__=80b62e480840e7252c140fb7066572a4f740881a13a925a4cb1813b0b150b288430ed5804256e9c929b6a2454b6a856c1faa87ae5db571040c9f4b7f6ddf00bdf1d6745f193b; TG-TRACK-CODE=search_code; SEARCH_ID=3fae8b76ae6e410a8720643063f21956; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1648961673; LGRID=20220403125434-6dfcfc26-9962-42fd-b863-aeef267035ca; X_HTTP_TOKEN=c9578984678b768a28026984610f7cbaf3c23c2ecf; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217fedb429e38db-0dd0783f16eb0f-56171958-1049088-17fedb429e4767%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2299.0.4844.74%22%7D%2C%22%24device_id%22%3A%2217fedb429e38db-0dd0783f16eb0f-56171958-1049088-17fedb429e4767%22%7D",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"
        }

    def run(self):
        url_lst = self.get_url_lst()
        job_infos = []
        for url in url_lst:
            job_url_lst,company_info =  self.get_job_url(url)
            if job_url_lst == []:
                continue

            for ind in job_url_lst:
                job_info = self.get_job_info(job_url_lst[ind])
                job_infos.append(job_info+company_info[ind])
        
        self.save(job_infos)
    
    def get_url_lst(self):
        url_lsts = []
        self.chrome.get("https://www.lagou.com/gongsi/2-0-100107,100109-0")
        if WebDriverWait(self.chrome,60).until(lambda x:x.find_element_by_xpath("//h3[@class='company-name wordCut']/a")):



            html = self.chrome.page_source
            e = etree.HTML(html)
            url_lst = e.xpath("//a[@class='bottom-item bottom-2 fl']/@href")
            # url_lst = self.chrome.find_element_by_xpath("//h3[@class='company-name wordCut']/a").get_attribute("href")
            url_lsts += url_lst
            # print(len(url_lst))
            # print(url_lst[-1])

            self.chrome.find_element_by_xpath('//div[@id="company_list"]/div/div/span[3]').click()
            time.sleep(3)
            html = self.chrome.page_source
            e = etree.HTML(html)
            url_lst = e.xpath("//a[@class='bottom-item bottom-2 fl']/@href")
            # url_lst = self.chrome.find_element_by_xpath("//h3[@class='company-name wordCut']/a").get_attribute("href")
            url_lsts += url_lst
            # print(len(url_lst))
            # print(url_lst[-1])

            #url_lsts += url_lst
        return url_lsts
    
    def get_job_url(self,url):
        self.chrome.get(url)
        url_lst = []
        company_info = []
        if WebDriverWait(self.chrome,60).until(lambda x:x.find_element_by_xpath("//div[@class='item_title_date_name']/a")):
            html = self.chrome.page_source
            e = etree.HTML(html)
            
            job_nums = e.xpath('//div[@id="company_navs"]/div/ul/li[2]/a/text()')[0]
            job_nums = int(job_nums.split("（")[-1].split("）")[0].strip())

            if job_nums == 0:
                return [],[]

            url_lst += e.xpath("//div[@class='item_title_date_name']/a/@href")
            field = e.xpath('//div[@id="basic_container"]/div[2]/ul/li[1]/span')[0]
            development_stage = e.xpath('//div[@id="basic_container"]/div[2]/ul/li[2]/span')[0]
            development_scale = e.xpath('//div[@id="basic_container"]/div[2]/ul/li[3]/span')[0]
            city = e.xpath('//div[@id="basic_container"]/div[2]/ul/li[4]/span')[0]
            company_label = []
            label = e.xpath("//ul[@class='item_con_ul clearfix']/li/text()")
            for l in label:
                company_label.append(l.strip())
            company_label = "|".join(company_label)

            for _ in range(len(url_lst)):
                company_info.append([field,development_stage,development_scale,city,company_label])

            if job_nums <= 10:
                return url_lst,company_info

            for i in range(2):
                s = f'//div[@id="posfilterlist_container"]/div/div[2]/div[3]/span[{4+i}]'
                print(s)
                actions = ActionChains(self.chrome)
                tag = self.chrome.find_element_by_css_selector(f"#posfilterlist_container > div > div.item_con_list_container > div.pages > span:nth-child({4+i})")
                actions.move_to_element(tag)
                actions.click()
                #self.chrome.find_element_by_xpath(f'//div[@id="posfilterlist_container"]/div/div[2]/div[3]/span[{4+i}]/').click()
                time.sleep(3)
                html = self.chrome.page_source
                e = etree.HTML(html)
                lst = e.xpath("//div[@class='item_title_date_name']/a/@href")
                url_lst += lst
                for _ in range(len(lst)):
                    company_info.append([field,development_stage,development_scale,city,company_label])
        return url_lst,company_info

    
    def get_job_info(self,url):
        resp = requests.get(url,headers=self.headers)
        e = etree.HTML(resp.text)
        job_name = e.xpath("//span[@class='position-head-wrap-position-name']/text()")[0]
        job_salary = e.xpath("//span[@class='salary']/text()")[0]
        job_detail = e.xpath("//div[@class='job-detail']/text()")
        job_detail = "".join(job_detail).strip().replace("\n","")
        job_addr = e.xpath("//div[@class='work_addr']/a/text()")[:-1]
        a = e.xapth("//div[@class='work_addr']/span/text()")
        job_addr = "-".join(job_addr + a)
        return [job_name,job_salary,job_detail,job_addr]


    def save(self,job_infos):
        #创建工作簿对象
        wb = openpyxl.Workbook()
        #获取工作表sheet
        sheet = wb.active
        for i in job_infos:
            sheet.append(i)

        #保存
        wb.save("job_info.xlsx")


if __name__ == '__main__':
    s = Spider()
    s.run()

