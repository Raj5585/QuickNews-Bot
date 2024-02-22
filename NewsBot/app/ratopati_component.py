from RPA.Browser.Selenium import Selenium, By
from qrlib.QRProcess import QRProcess
from qrlib.QRComponent import QRComponent
from qrlib.QRUtils import display
from excelfile import Englishkeywords
import datetime

data = []
alllinks = []
keywords = Englishkeywords()


class Ratopati(QRComponent):
    def __init__(self):
        super().__init__()
        self.browser = Selenium()

    def open_broser(self, url):
        try:
            self.browser.open_available_browser(url, headless=True)
            self.browser.maximize_browser_window()
        except:
            print("Error while opening browser")

    def scrape(self):
        display("----------------------[scraping Ratopati]--------------")
        for keyword in keywords:
            display(
                f"***************Searching for {keyword} in Ratopati*****************"
            )

        for keyword in keywords:
            display(f"searching for {keyword}")
            URL = f"https://english.ratopati.com/search?query={keyword}"
            self.open_broser(URL)
            # try:
               # maindivs = self.browser.find_elements('//div[contains(@class,"post-card__more-secondary-story")]')
            for div in self.browser.find_elements('//div[contains(@class,"post-card__more-secondary-story")]'):
                a_tag = div.find_element(By.TAG_NAME, "a")
                Posttime = div.find_element(By.TAG_NAME, "time")
                link = a_tag.get_attribute("href")
                title = a_tag.text
                getTime = (Posttime.text).split(" ")
                content, time = self.insideLink(link)

                if (getTime[1] == "Minutes" or getTime[1] == "Minute" or getTime[1] == "Seconds"  or getTime[1] == "Hour"or getTime[1] == "Hours"):
                    print(link)
                    if(keyword  in content or keyword  in title):
                        if (link not in alllinks):
                            alllinks.append(link)
                            newsData = {
                                "title": title,
                                "date_bs": "",
                                "date_ad": datetime.datetime.now().strftime("%Y-%m-%d"),
                                "content": content[:1200],
                                "keyword": keyword,
                                "newspaper": "Ratopati",
                                "link": link,
                            }
                        else:
                            display('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx[duplicate link]xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx]')
                    else:
                        display('xxxxxxxxx [Wrong News] xxxxxxxxxxxxxx')
                else:
                    display("no recent news ")
                    break
                display(newsData)
                data.append(newsData)
            # except BaseException as e:
            #     display("main div not found")
            #     print(e)
        return data

    def insideLink(self, link):
        print(link)
        self.browser.open_available_browser(link, headless=True)
        self.browser.maximize_browser_window()
        content = self.browser.find_element('//div[@class="content-area"]').text
        print(content)
        time = self.browser.find_element('//div[@class="author-img flex"]/div').text

        return (content, time)
