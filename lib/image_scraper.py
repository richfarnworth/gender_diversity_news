
class image_scraper:
    def __init__(self,page_url,driver):
        self.page_url = page_url
        self.driver = driver
    def image_list(self):
        print("Listing images for " + self.page_url)
        self.driver.get(self.page_url)
        elements = self.driver.find_elements_by_xpath("//img")
        img_list = []
        for i in elements:
            src = i.get_attribute('src')
            if src != '' and src[:4] != 'data':
                img_list += [src]
            else:
                img_list += [i.get_attribute('data-src').replace('{width}','820')]
        return img_list