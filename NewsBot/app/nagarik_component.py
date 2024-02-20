from RPA.Browser.Selenium import Selenium, By
from qrlib.QRComponent import QRComponent
from qrlib.QRUtils import display
from excelfile import Englishkeywords, Nepalikeywords
import time, datetime

from selenium.webdriver.common.keys import Keys
import nepali_datetime

data = []
keywords = Nepalikeywords()


# keywords = ['सांसदको']
class Nagarik(QRComponent):
    def __init__(self):
        super().__init__()
        self.browser = Selenium()
        self.newsdict = {}

    def convertoenglish(self, date):
        nepali_months_mapping = {
            "वैशाख": "01",
            "जेठ": "02",
            "असार": "03",
            "साउन": "04",
            "भदौ": "05",
            "असोज": "06",
            "कात्तिक": "07",
            "कार्तिक": "07",
            "मंसिर": "08",
            "पुष": "09",
            "पुस": "09",
            "माघ": 10,
            "फागुन": 11,
            "फाल्गुन": 11,
            "चैत": 12,
        }
        swords = date.split(" ")
        extracted_date = swords[0:3]
        if len(extracted_date[0]) == 1:
            extracted_date[0] = "0" + str(int(extracted_date[0]))
        lstnew = [
            str(int(extracted_date[2])),
            str(nepali_months_mapping[extracted_date[1]]),
            extracted_date[0],
        ]
        formatteddate = "-".join(lstnew)
        return formatteddate

    # def open_broser(self):

    #     try:
    #         se`alf.browser.open_available_browser('https://nagariknews.nagariknetwork.com/search')
    #         self.browser.maximize_browser_window()

    #     except:
    #         print("Error while opening browser")

    def scrape(self):
        display("----------------------[scraping Nagarik]--------------")

        try:
            self.browser.open_available_browser(
                "https://nagariknews.nagariknetwork.com/search", headless=True
            )
            self.browser.maximize_browser_window()

        except:
            print("Error while opening browser")

        allinks = []
        for keyword in keywords:
            display(f"searching for {keyword}")
            input_field = self.browser.find_element('//input[@id="txtSearch"]')
            input_field.clear()
            input_field.send_keys(keyword + " ")
            input_field.send_keys(Keys.RETURN)
            time.sleep(1)
            articles = self.browser.find_elements(
                '//article[contains(@class,"list-group-item")]/div[@class="text"]'
            )
            for div in articles:
                try:
                    pt = div.find_element(By.TAG_NAME, "time")
                    nepalidate = self.convertoenglish(pt.text)

                    if nepalidate == str(nepali_datetime.date.today()):
                        h1tag = div.find_element(By.TAG_NAME, "h1")
                        a_tag = h1tag.find_element(By.TAG_NAME, "a")
                        href_value = a_tag.get_attribute("href")
                        title = a_tag.text
                        href_value = a_tag.get_attribute("href")
                        content = (div.find_element(By.TAG_NAME, "p")).text
                        if href_value not in allinks:
                            self.newsdict = {
                                "title": title,
                                "date_ad": datetime.datetime.now().strftime("%Y-%m-%d"),
                                "date_bs": nepalidate,
                                "content": content,
                                "keyword": keyword,
                                "newspaper": "नागरिक दैनिक",
                                "link": href_value,
                            }
                            # display(self.newsdict)
                        else:
                            print("same link")
                    else:
                        print("no further data")
                        break
                except BaseException as e:
                    print(e)
                    print("no time found")

        data.append(self.newsdict)
        print(data)
        return data
