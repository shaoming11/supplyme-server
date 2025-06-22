import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

companies = []

finalCompanyData = []
finalSupplierData = []

# def getCompanyPage(companyName):
#     driver = webdriver.Firefox()
#     driver.get(f"https://www.importyeti.com/search?q={companyName}")
#     time.sleep(5)
#     elem = driver.find_element(By.ID, "headlessui-tabs-panel-«Rq9tpdpdb»")
#     elem2 = driver.find_elements(By.TAG_NAME, "a")
#     # print(elem)
#     # print(elem2)

#     print(elem2[5].text)
#     print(len(elem2))

#     for element in elem2:
#         print(element.text)

#     # elem.clear()
#     # elem.send_keys("pycon")
#     # elem.send_keys(Keys.RETURN)
#     driver.close()

def getCompanyPage(companyName):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    url = f"https://www.importyeti.com/search?q={companyName}"
    driver.get(url)
    # time.sleep(10)

    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CLASS_NAME, "-rotate-45"))
        )
    except:
        driver.quit()

    links = driver.find_elements(By.TAG_NAME, "a")
    # print(elem)
    # print(elem2)

    print(links[9].text)
    print(len(links))

    # for link in links:
    #     print(link.text)

    driver.quit()


# def getSuppliers(companyPage):
    # page = requests.get(companyPage)

getCompanyPage("microsoft")

# soup = BeautifulSoup("<p>Some<b>bad<i>HTML", "html.parser")
# results = soup.find(id="ResultsContainer")
# suppliers = results.find_all("div", class_="card-content")
# # text-yeti-abominable-10 hover:underline fill-blue-700 font-bold text-sm

# req = urllib.request.Request('https://www.importyeti.com/company/apple')
# req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:139.0) Gecko/20100101 Firefox/139.0')
# req.add_header('Referer', 'https://www.importyeti.com/search?q=apple&page=1')

# print(urllib.request.urlopen(req).read().decode('utf-8'))

# async def main():
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://www.importyeti.com/company/apple') as resp:
#             print(resp.status)
#             print(await resp.text())

# asyncio.run(main())