from bs4 import BeautifulSoup as BS
from halo import Halo
from icecream import ic
import json
import requests


def extract_recipe_content(recipe):
    try:
        soup = BS(get_(recipe), 'html.parser')
        title = soup.title.text.split("recipe")[0].strip()
        content = soup.find(class_="recipe-and-additional-content")
        ingredients = [x.text.strip() for x in
                       content.find(class_="ingredient-group").find_all("li")]
        steps = [x.text.strip() for x in
                 content.find(class_="preparation-steps").find_all("li")]
        tags = [x.text.strip() for x in
                content.find(class_="menus-tags content").find_all("dt")]
        return {
            "title": title,
            "source": recipe,
            "ingredients": ingredients,
            "steps": steps,
            "tags": tags
        }
    except Exception:  # as e:
        pass


def extract_recipe_urls(url_list):
    url_base = "https://www.epicurious.com"
    recipe_urls = []
    for url in url_list:
        soup = BS(get_(url), 'html.parser')
        try:
            content_list = soup.find(id='sitemapItems').find_all('li')
            for item in content_list:
                href = item.a.attrs.get('href')
                recipe_url = url_base + href
                recipe_urls.append(recipe_url)
        except Exception:  # as e:
            pass
    return recipe_urls


def generate_urls(kind, start_year, end_year):
    url_base = "https://www.epicurious.com/services/sitemap/recipes/"
    date_range = range(start_year, end_year + 1)
    url_base = url_base + kind + "/"
    return [url_base + str(x) for x in date_range]


def get_(url):
    return requests.get(url).text


def main():
    spinner = Halo(
        text="Generating Editorial recipe base URLs", spinner="dots")
    spinner.start()
    editorial_start_urls = generate_urls("editorial", 1998, 1998)
    spinner.succeed()

    spinner = Halo(
        text="Gathering list of all Editorial recipe URLs", spinner="dots")
    spinner.start()
    editorial_recipe_urls = extract_recipe_urls(editorial_start_urls)
    spinner.succeed()

    spinner = Halo(text="Extracting Editorial recipe contents", spinner="dots")
    spinner.start()
    editorial_recipes = [extract_recipe_content(x)
                         for x in editorial_recipe_urls]
    spinner.succeed()

    spinner = Halo(text="Saving editorial recipes to disk", spinner="dots")
    spinner.start()
    filename = "editorial_recipes.json"
    with open(filename, "w+") as f:
        json.dump(editorial_recipes, f)
    spinner.succeed()

    spinner = Halo(text="Generating Member recipe base URLs", spinner="dots")
    spinner.start()
    member_start_urls = generate_urls("member", 2005, 2021)
    spinner.succeed()

    spinner = Halo(
        text="Gathering list of all Member recipe URLs", spinner="dots")
    spinner.start()
    member_recipe_urls = extract_recipe_urls(member_start_urls)
    spinner.succeed()

    spinner = Halo(
        text="Extracting Member recipe contents", spinner="dots")
    spinner.start()
    """
    member_recipes = [extract_recipe_content(x) for x in
                      member_recipe_urls]
    """
    member_recipes = extract_recipe_content(member_recipe_urls[0])
    spinner.succeed()

    spinner = Halo(text="Saving member recipes to disk", spinner="dots")
    spinner.start()
    filename = "member_recipes.json"
    with open(filename, "w+") as f:
        json.dump(member_recipes, f)
    spinner.succeed()


if __name__ == "__main__":
    main()
