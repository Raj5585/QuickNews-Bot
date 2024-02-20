from RPA.Browser.Selenium import Selenium, By
from qrlib.QRComponent import QRComponent
from qrlib.QRUtils import display
import date_utils
import datetime
import nepali_datetime
import time

from excelfile import Nepalikeywords


class Ekantipur(QRComponent):
    def __init__(self):
        super().__init__()
        self.browser = Selenium()
        self.keywords = Nepalikeywords()
        self.alllinks = []

    def open_browser(self):
        pass

    def scrape(self):

        display("----------------------[scraping eKantipur]--------------")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        url = f"https://ekantipur.com/search/2003/?txtSearch=&year=2024&date-from={today}&date-to={today}"

        try:
            self.browser.open_available_browser(url, headless=True)
            self.browser.maximize_browser_window()
            time.sleep(2)
        except:
            print("Error while opening browser")

        results = []
        for keyword in self.keywords:
            display(f"searching for {keyword}")
            try:
                self.browser.input_text_when_element_is_visible(
                    "xpath=//input[@id='txtSearch']", keyword
                )
                self.browser.click_button_when_visible(
                    "xpath=//input[@class='commentBtnText default-btn']"
                )
            except Exception as e:
                print(e)

            articles_list = self.browser.find_elements("xpath=//article[@class]")
            for _ in articles_list:

                title = self.browser.find_element(
                    "xpath=//div[@class='teaser offset']/h2"
                ).text
                link = self.browser.find_element(
                    "xpath=//div[@class='teaser offset']/h2/a"
                ).get_attribute("href")
                content = self.browser.find_element(
                    "xpath=//div[@class='teaser offset']/p"
                ).text

                date = self.browser.find_element(
                    "xpath=//div[@class='teaser offset']/time"
                ).text
                conv_day, conv_month, conv_year = date_utils.get_eng_date(date.split())

                date = nepali_datetime.date(conv_year, conv_month, conv_day)

                date_bs = date.strftime("%Y-%m-%d")
                date_ad = date.to_datetime_date().strftime("%Y-%m-%d")
                # display(
                #     f"""
                # -------------------------------------[news found]------------------------------------------
                # Link      : {link}
                # Title     : {title}
                # Keyword   : {keyword}
                # Newspaper : eKantipur
                # Date AD   : {date_ad}
                # Date BS   : {date_bs}
                # -------------------------------------------------------------------------------------------
                # """
                # )

                if link not in self.alllinks:
                    self.alllinks.append(link)
                    results.append(
                        {
                            "newspaper": "eKantipur",
                            "keyword": keyword,
                            "title": title,
                            "content": content,
                            "link": link,
                            "date_ad": date_ad,
                            "date_bs": date_bs,
                        }
                    )
        return results
