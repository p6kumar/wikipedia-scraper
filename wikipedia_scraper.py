from bs4 import BeautifulSoup
import requests
import csv

def extract(body):
    """
    Extracts bodies of texts that are in bullet points and returns a list of the bullet points
    as well as a list of the relevant links within the bullet points
    """
    points_list = []
    points_links_list = []
    for points in body.ul.find_all("li"):
        points_list.append(points.text)
        for bolded in points.find_all("b"):
            featured_link = bolded.find("a")["href"]
            full_link = "https://en.wikipedia.org" + featured_link
            points_links_list.append(full_link)
    return points_list, points_links_list


def main():
    url = "https://en.wikipedia.org/wiki/Main_Page"
    HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    website = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(website.text, 'html.parser')
    csv_file = open("wiki_front_page.csv", "w")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Header", "Text", "Relevant Links"])
    headline_list = []
    body_list = []
    links_list = []
    
    for card in soup.find_all('div', class_ = "MainPageBG mp-box"):
        for headline in card.find_all('h2'):
            headline_list.append(headline.text)
        if card.get("id") == "mp-right":
            for body in card.find_all('div', class_ = "mp-contains-float"):
                points_list , points_links_list = extract(body)
                body_list.append(points_list)
                links_list.append(points_links_list)
        elif card.get("id") == "mp-lower":
            content =  card.p
            body_list.append(content.text)
            featured_link = content.b.find("a")["href"]
            full_link = "https://en.wikipedia.org" + featured_link
            links_list.append(full_link)
        else:            
            for body in card.find_all('div', class_ = "mp-contains-float"):
                try:
                    body_list.append(body.p.text)
                    featured_link = body.p.b.find("a")["href"]
                    full_link = "https://en.wikipedia.org" + featured_link
                    links_list.append(full_link)
                except:
                    points_list , points_links_list = extract(body)
                    body_list.append(points_list)
                    links_list.append(points_links_list)

    for i in range(len(headline_list)):
        csv_writer.writerow([headline_list[i], body_list[i], links_list[i]])

    csv_file.close()
    print("Created CSV file!")

if __name__ == "__main__":
    main()