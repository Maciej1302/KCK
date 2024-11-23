from bs4 import BeautifulSoup
import requests



def scrap_page(url: str) -> str:
    page = requests.get(url)
    return page.text


def scrap_cars_links(url: str) :
    cars_links=[]
    soup = BeautifulSoup(scrap_page(url), "html.parser")
    for div in soup.find_all('div', class_='offer-card__body'):
        a_tag = div.find('a', href=True)
        cars_links.append(f"https://www.autotrader.pl{a_tag['href']}")
    return cars_links



def get_car_attributes(url: str) -> dict[str] | None:
    car_attributes = {}
    soup = BeautifulSoup(scrap_page(url), "html.parser")
    car_attributes["price"] = soup.find('h3', class_='basic-info-heading__price').text.replace("zł", "").replace(" ","")

    for li in soup.find_all('div', class_='details-technical__body'):
        spans = li.find_all('span')
        ps = li.find_all('p')

        for attribute_name, attribute_value in zip(spans, ps):
            car_attributes[attribute_name.text] = attribute_value.text
    return car_attributes




def scrapper() :
    url= "https://www.autotrader.pl/szukaj/osobowe"
    links=scrap_cars_links(url)
    cars_list=[]
    i=1
    for link in links:
        #print(f"Samochód nr{i} {get_car_attributes(link)}")
        i+=1
        cars_list.append(get_car_attributes(link))
    return cars_list


