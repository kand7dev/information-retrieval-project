import requests
from bs4 import BeautifulSoup
from random_word import RandomWords

from . import json_save


def crawler(num_of_words=5):
    random = RandomWords()
    json_object_list = list()
    id = 1

    for i in range(num_of_words):
        word = random.get_random_word()
        url = url = (
            "https://arxiv.org/search/?query="
            + str(word)
            + "&searchtype=all&source=header"
        )
        html_respone = requests.get(url)

        if html_respone.ok:
            try:
                soup = BeautifulSoup(html_respone.content, "html.parser")

                html_titles = soup.find_all("p", class_="title is-5 mathjax")
                html_authors = soup.find_all("p", class_="authors")
                html_submissions = soup.select("p.is-size-7:not(.comments)")
                html_abstracts = soup.find_all(
                    "span", class_="abstract-full has-text-grey-dark mathjax"
                )

                authors_list = (
                    list()
                )  # is used to store all authors, gets re-initialized in each iteration

                for i in range(len(html_titles)):
                    title = html_titles[i].text.strip()

                    for author in html_authors[i].find_all("a"):
                        authors_list.append(author.text)

                    submission = (
                        html_submissions[i]
                        .find(
                            "span", class_="has-text-black-bis has-text-weight-semibold"
                        )
                        .nextSibling.text.strip()
                        .removesuffix(";")
                    )
                    abstract = (
                        html_abstracts[i].text.strip().replace("△ Less", "").strip()
                    )

                    paper_dict = dict(
                        paper_id=id,
                        paper_title=title,
                        paper_authors=authors_list.copy(),
                        paper_abstract=abstract,
                        paper_submission_date=submission,
                    )
                    json_object_list.append(paper_dict)
                    id += 1

                    authors_list.clear()
                    del paper_dict

            except AttributeError:
                continue

    if json_object_list:
        json_save.save("data/data.json", json_object_list)

        return 1

    else:
        return 0
