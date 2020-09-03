from urllib.parse import urlparse


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
                src = i.get_attribute('data-src').replace('{width}','820')
                if src[:4].lower() != 'http':
                    print(self.page_url)
                    print(src)
                    parsed_uri = urlparse(self.page_url)
                    result = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)[:-1]
                    src = (result + src)
                    print(src)
                img_list += [src]
        return img_list