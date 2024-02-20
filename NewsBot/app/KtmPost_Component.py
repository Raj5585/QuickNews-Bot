from qrlib.QRComponent import QRComponent
from RPA.Browser.Selenium import Selenium
import time
import re
from datetime import datetime, timedelta
from excelfile import Englishkeywords


keywords = Englishkeywords()


URL = "www.kathmandupost.com"

current_datetime = datetime.now()
twenty_four_hours_ago = current_datetime - timedelta(hours=24)


class KtmPost(QRComponent):
    def __init__(self):
        super().__init__()
        self.browser = Selenium()

    def search_keyword(self):
        try:
            self.browser.open_available_browser(URL, headless=True)
            self.browser.maximize_browser_window()
            time.sleep(2)

        except:
            print("Error while opening browser")

        try:
            for keyword in keywords:
                search_button = '//div[@class="blocktop blocktop-search block--search"]'
                self.browser.click_element_when_clickable(search_button)

                search_box = '//input[@name="search"]'
                time.sleep(2)

                self.browser.input_text(search_box, keyword)
                self.browser.press_keys(None, "RETURN")
                time.sleep(2)

        except Exception as e:
            print("Unable to search, ", e)

        # sort news bsed on date
            
        try:
            sort_menu = '//div[@class="gsc-option-menu-container gsc-inline-block"]'
            sort_option = '//div[@class="gsc-option"][text()="Date"]'

            self.browser.click_element_when_clickable(sort_menu)
            self.browser.click_element_when_visible(sort_option)
            time.sleep(2)
        
        except Exception as e:
            print("Cannot sort results, ", e)

        # Check Article links 

        article_link_elements = '//a[@class="gs-title"][@href]'
        time_elements = '//div[@class="gs-bidi-start-align gs-snippet"]'

        article_links = set()
        article_found = False

        time_elements_list = self.browser.find_elements(time_elements)
        article_link_elements_list = self.browser.find_elements(article_link_elements)

        for i, time_element in enumerate(time_elements_list):
            try:
                element_text = time_element.text
                relative_time_match = re.search(r"(\d+) (seconds?|minutes?|hours?) ago", element_text)
                
                if relative_time_match:
                    j = 2 * i
                    article_link = article_link_elements_list[j].get_attribute('href')
                    if len(article_link) < 40:

                        article_link = None
                    if article_link:
                        # print(f"found article_link {article_link}")
                        article_found = True
                        article_links.add(article_link)

            except Exception as e:
                print(f"Error processing time element {i}: {str(e)}")

        
        updated_time_elements = '//div[@class="updated-time"]'
        title_element = '//h1[@style]'
        story_section_element = '//section[@class="story-section"]'

        final_results = []

        try:
            for article_link in article_links:
                paragraph_flag = 0
                print(f"visiting link {article_link}")
                self.browser.go_to(article_link)
                time.sleep(2)

                try:
                    updated_time = self.browser.find_elements(updated_time_elements)

                    for updated_at in updated_time:
                        updated_time_text = updated_at.text.strip()

                        if 'Updated at' in updated_time_text:
                            published_date_str = updated_time_text.split(':', 1)[-1].strip()

                            published_date = datetime.strptime(published_date_str, "%B %d, %Y %H:%M")
                            if twenty_four_hours_ago <= published_date <= current_datetime:
                                title = self.browser.find_element(title_element)

                                story_section = self.browser.find_element(story_section_element)
                                if story_section:
                                    story_section_paragraphs = self.browser.find_elements('//section[@class="story-section"]/p')
                                    paragraph_elements = []
                                    for paragraph in story_section_paragraphs:
                                        paragraph_elements.append(paragraph.text)
                                    for paragraph in paragraph_elements:
                                        if paragraph_flag == 1:
                                            break
                                        if keyword in paragraph:
                                            paragraph_flag = 1
                                            print(f"found {keyword} in paragraph text")

                                            if title_element:
                                                article_title = title.text
                                            else:
                                                article_title = paragraph_elements.split('.')[0].strip() if paragraph_elements else "Title Not Available"

                                            results = {
                                                "keyword": keyword,
                                                "title": article_title,
                                                "link": article_link,
                                                "content": paragraph_elements[0].strip()
                                            }
                                            print("added to final results")
                                            final_results.append(results)

                except Exception as e:
                    print("Caught exception : ", e)
                    
                # time.sleep(2)
                self.browser.go_back()
                self.click_outside()
                # time.sleep(2)

        except Exception as e:
            print("Caught exception : ", e)

        return final_results

    def click_outside(self):
        search_box = '//input[@name="search"]'
        self.browser.click_element_at_coordinates(search_box, 5, 5)
        # time.sleep(2)