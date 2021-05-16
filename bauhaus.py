from bs4 import BeautifulSoup
import requests
import pandas as pd

# Get the ids of the products to search them in a web page.
df = pd.read_excel("Refs to parse.xlsx")
list_of_ids = df['Ref'].to_list()
list_of_ids = [str(x) for x in list_of_ids]


# Search on the web and save the results in a list
final_titles = []
final_urls = []
for num in list_of_ids[:100]:
    search_url = "https://www.bauhaus.es/buscar/productos?text=" + num
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    prod_tags = soup.select('h3.product-list-tile__info__name')

    titles = [tag.text for tag in prod_tags]
    urls = [link.a.get("href") for link in prod_tags]
    final_titles.append("".join(titles))
    final_urls.append("".join(urls))


print('Finish')

#Delete empty spaces that can affect the url and add the domain
final_titles = [x.strip() for x in final_titles]
final_urls = [y.strip() for y in final_urls]
final_urls = ['https://www.bauhaus.es' + y for y in final_urls]


#Save it to a new excel
df2 = pd.DataFrame(list(zip(final_titles, final_urls)), columns =['Product name', 'urls'])
df2.to_excel('Products list.xlsx', encoding="utf_8_sig", index=False)