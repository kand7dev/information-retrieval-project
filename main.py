import os
import random
import time
from datetime import datetime

import numpy as np

from functions import algorithms, crawler, data_tokenizer, indexing, json_reader

if os.name == "posix":

    def clear():
        return os.system("clear")

elif os.name == "nt":

    def clear():
        return os.system("cls")


data = json_reader.reader("data/data.json")
tokenized_data = data_tokenizer.tokenizer(data)
inverted_index = indexing.record_level_inverted_index(tokenized_data)


print("*" * 8, "Starting Search Engine", "*" * 8)
print("\nWelcome to our Custom Search Engine!\n")

while 1:
    clear()
    print("You can use the previously scraped data or start fresh!")
    print("1) Use database data")
    print("2) Start scraping")
    print("3) Exit application\n")
    try:
        option = int(input("\nEnter an option : "))
        match option:
            case 1:
                clear()
                print("\n**** Select an Algorithm ****\n")
                print("1) Boolean Retrieval")
                print("2) Vector Space Model")
                print("3) OKAPI BM25")
                print("4) Previous Page\n")
                algo = 0
                while algo == 0:
                    try:
                        algo = int(input("\nEnter an option : "))
                        match algo:
                            case 1:
                                clear()
                                print("**** Enter your Boolean query ****")
                                print(
                                    "\nQuery must start with a word. Single word is accepted. In case of using multiple words, each word must be separated by a boolean operator (AND/OR/NOT)\n"
                                )
                                query = input("Query : ")
                                if query == "":
                                    clear()
                                    print(
                                        "Your given query is empty! Returning a random and interesting paper..."
                                    )
                                    time.sleep(2)
                                    clear()
                                    random_id = random.randint(0, len(data))
                                    random_paper = data[random_id]
                                    print("-" * 100)
                                    print(
                                        f"\nPaper Title: {random_paper['paper_title']}"
                                    )
                                    print(
                                        f"Paper Authors: {', '.join(random_paper['paper_authors'])}\n"
                                    )
                                    print(f"\n{random_paper['paper_abstract']}\n")
                                    print(
                                        f"\nSubmitted: {random_paper['paper_submission_date']}"
                                    )
                                    print(
                                        "-" * 100,
                                    )
                                    input("\n")
                                    break

                                result = algorithms.boolean_retrieval(
                                    query, tokenized_data, inverted_index
                                )
                                clear()
                                print("**** Filters ****\n")
                                print("1) Filter by authors names")
                                print("2) Filter by date")
                                print("3) No filter")
                                if not result:
                                    clear()
                                    input("No Result...")
                                    clear()
                                    break
                                filter = 0
                                while filter == 0:
                                    try:
                                        filter = int(input("\nEnter an option : "))
                                        match filter:
                                            case 1:
                                                authors_names = (
                                                    input(
                                                        "Enter authors names, seperated by a comma (,) : "
                                                    )
                                                    .strip()
                                                    .lower()
                                                    .split(sep=",")
                                                )
                                                final_result = list()
                                                paper_number = 0
                                                clear()
                                                if result:
                                                    for id in result:
                                                        paper = next(
                                                            item
                                                            for item in data
                                                            if item["paper_id"] == id
                                                        )
                                                        paper_authors = [
                                                            author.lower()
                                                            for author in paper[
                                                                "paper_authors"
                                                            ]
                                                        ]
                                                        if all(
                                                            authors in paper_authors
                                                            for authors in authors_names
                                                        ):
                                                            paper_number += 1
                                                            final_result.append(paper)
                                                        if final_result:
                                                            print(
                                                                "-" * 48,
                                                                f"{paper_number}",
                                                                "-" * 48,
                                                            )
                                                            print(
                                                                f"\n    Paper Title: {paper['paper_title']}"
                                                            )
                                                            print(
                                                                f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                            )
                                                            print(
                                                                f"\n{paper['paper_abstract']}\n"
                                                            )
                                                            print(
                                                                f"\nSubmitted: {paper['paper_submission_date']}"
                                                            )
                                                            print(
                                                                "-" * 100,
                                                            )
                                                            final_result.clear()
                                                            input("\n")

                                            case 2:
                                                clear()
                                                date_is_okay = False
                                                operations = ["n", "o"]
                                                while not date_is_okay:
                                                    date = input(
                                                        "Enter date (day/month/year) : "
                                                    )
                                                    operation = input(
                                                        "You want newer or older papers than the given date? ( n/o ) : "
                                                    )
                                                    try:
                                                        user_input_date = (
                                                            datetime.strptime(
                                                                date, "%d/%m/%Y"
                                                            )
                                                        )
                                                        if operation not in operations:
                                                            input(
                                                                "Wrong operation.\nPress any key to re-enter your data..."
                                                            )
                                                            clear()
                                                            continue
                                                        date_is_okay = True

                                                    except ValueError:
                                                        input(
                                                            "Wrong format.\nPress any key to re-enter you data..."
                                                        )
                                                        clear()
                                                        continue
                                                final_result = list()
                                                paper_number = 0
                                                clear()
                                                if result:
                                                    for id in result:
                                                        paper = next(
                                                            item
                                                            for item in data
                                                            if item["paper_id"] == id
                                                        )
                                                        paper_date = datetime.strptime(
                                                            paper[
                                                                "paper_submission_date"
                                                            ],
                                                            "%d %B, %Y",
                                                        )
                                                        if operation == "n":
                                                            if (
                                                                paper_date
                                                                > user_input_date
                                                            ):
                                                                paper_number += 1
                                                                final_result.append(
                                                                    paper
                                                                )
                                                        elif operation == "o":
                                                            if (
                                                                paper_date
                                                                < user_input_date
                                                            ):
                                                                paper_number += 1
                                                                final_result.append(
                                                                    paper
                                                                )
                                                        if final_result:
                                                            print(
                                                                "-" * 48,
                                                                f"{paper_number}",
                                                                "-" * 48,
                                                            )
                                                            print(
                                                                f"\n    Paper Title: {paper['paper_title']}"
                                                            )
                                                            print(
                                                                f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                            )
                                                            print(
                                                                f"\n{paper['paper_abstract']}\n"
                                                            )
                                                            print(
                                                                f"\nSubmitted: {paper['paper_submission_date']}"
                                                            )
                                                            print(
                                                                "-" * 100,
                                                            )
                                                            final_result.clear()
                                                            input("\n")

                                            case 3:
                                                clear()
                                                paper_number = 0
                                                for id in result:
                                                    paper = next(
                                                        item
                                                        for item in data
                                                        if item["paper_id"] == id
                                                    )
                                                    paper_number += 1
                                                    print(
                                                        "-" * 48,
                                                        f"{paper_number}",
                                                        "-" * 48,
                                                    )
                                                    print(
                                                        f"\n    Paper Title: {paper['paper_title']}"
                                                    )
                                                    print(
                                                        f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                    )
                                                    print(
                                                        f"\n{paper['paper_abstract']}\n"
                                                    )
                                                    print(
                                                        f"\n    Submitted: {paper['paper_submission_date']}"
                                                    )
                                                    print(
                                                        "-" * 100,
                                                    )
                                                    input("\n")

                                            case _:
                                                clear()
                                                print("**** Filters ****\n")
                                                print("1) Filter by authors names")
                                                print("2) Filter by date")
                                                print("3) No filter")
                                                filter = 0

                                    except ValueError:
                                        clear()
                                        print("**** Filters ****\n")
                                        print("1) Filter by authors names")
                                        print("2) Filter by date")
                                        print("3) No filter")
                                        filter = 0

                            case 2:
                                clear()
                                print("**** Enter your query ****")
                                print("\nA query can consist of any ammount of words\n")
                                query = input("Query : ")
                                if query == "":
                                    clear()
                                    print(
                                        "Your given query is empty! Returning a random and interesting paper..."
                                    )
                                    time.sleep(2)
                                    clear()
                                    random_id = random.randint(0, len(data))
                                    random_paper = data[random_id]
                                    print("-" * 100)
                                    print(
                                        f"\nPaper Title: {random_paper['paper_title']}"
                                    )
                                    print(
                                        f"Paper Authors: {', '.join(random_paper['paper_authors'])}\n"
                                    )
                                    print(f"\n{random_paper['paper_abstract']}\n")
                                    print(
                                        f"\nSubmitted: {random_paper['paper_submission_date']}"
                                    )
                                    print(
                                        "-" * 100,
                                    )
                                    input("\n")
                                    break
                                results = sorted(
                                    algorithms.vector_space_model(
                                        query, tokenized_data, data
                                    ),
                                    key=lambda tup: tup[1],
                                    reverse=True,
                                )
                                scores = [
                                    score[1] for score in results if score[1] != 0
                                ]
                                if not scores:
                                    clear()
                                    input("No Result...")
                                    clear()
                                    break
                                clear()
                                print("**** Filters *****\n")
                                print("1) Filter by authors names")
                                print("2) Filter by date")
                                print("3) No filter")
                                filter = 0
                                while filter == 0:
                                    try:
                                        filter = int(input("\nEnter an option : "))
                                        match filter:
                                            case 1:
                                                authors_names = (
                                                    input(
                                                        "Enter authors names, seperated by a comma (,) : "
                                                    )
                                                    .strip()
                                                    .lower()
                                                    .split(sep=",")
                                                )
                                                final_result = list()
                                                paper_number = 0
                                                clear()
                                                if results[0][1]:
                                                    for result in results:
                                                        if (result[1]) != 0:
                                                            paper = next(
                                                                item
                                                                for item in data
                                                                if item["paper_id"]
                                                                == result[0]
                                                            )
                                                            paper_authors = [
                                                                author.lower()
                                                                for author in paper[
                                                                    "paper_authors"
                                                                ]
                                                            ]
                                                            if all(
                                                                authors in paper_authors
                                                                for authors in authors_names
                                                            ):
                                                                paper_number += 1
                                                                final_result.append(
                                                                    paper
                                                                )
                                                            if final_result:
                                                                for (
                                                                    paper
                                                                ) in final_result:
                                                                    print(
                                                                        "-" * 48,
                                                                        f"{paper_number}",
                                                                        "-" * 48,
                                                                    )
                                                                    print(
                                                                        f"\n    Similarity {result[1]:.3f}\n"
                                                                    )
                                                                    print(
                                                                        f"\n    Paper Title: {paper['paper_title']}"
                                                                    )
                                                                    print(
                                                                        f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                                    )
                                                                    print(
                                                                        f"\n{paper['paper_abstract']}\n"
                                                                    )
                                                                    print(
                                                                        f"\nSubmitted: {paper['paper_submission_date']}"
                                                                    )
                                                                    print(
                                                                        "-" * 100,
                                                                    )
                                                                    final_result.clear()
                                                                    input("\n")
                                            case 2:
                                                clear()
                                                date_is_okay = False
                                                operations = ["n", "o"]
                                                while not date_is_okay:
                                                    date = input(
                                                        "Enter date (day/month/year) : "
                                                    )
                                                    operation = input(
                                                        "You want newer or older papers than the given date? ( n/o ) : "
                                                    )
                                                    try:
                                                        user_input_date = (
                                                            datetime.strptime(
                                                                date, "%d/%m/%Y"
                                                            )
                                                        )
                                                        if operation not in operations:
                                                            input(
                                                                "Wrong operation.\nPress any key to re-enter your data..."
                                                            )
                                                            clear()
                                                            continue
                                                        date_is_okay = True

                                                    except ValueError:
                                                        input(
                                                            "Wrong format.\nPress any key to re-enter you data..."
                                                        )
                                                        clear()
                                                        continue
                                                final_result = list()
                                                paper_number = 0
                                                clear()
                                                if results[0][1]:
                                                    for result in results:
                                                        if (result[1]) != 0:
                                                            paper = next(
                                                                item
                                                                for item in data
                                                                if item["paper_id"]
                                                                == result[0]
                                                            )
                                                            paper_authors = [
                                                                author.lower()
                                                                for author in paper[
                                                                    "paper_authors"
                                                                ]
                                                            ]
                                                            paper_date = datetime.strptime(
                                                                paper[
                                                                    "paper_submission_date"
                                                                ],
                                                                "%d %B, %Y",
                                                            )
                                                            if operation == "n":
                                                                if (
                                                                    paper_date
                                                                    > user_input_date
                                                                ):
                                                                    paper_number += 1
                                                                    final_result.append(
                                                                        paper
                                                                    )
                                                            elif operation == "o":
                                                                if (
                                                                    paper_date
                                                                    < user_input_date
                                                                ):
                                                                    paper_number += 1
                                                                    final_result.append(
                                                                        paper
                                                                    )
                                                            if final_result:
                                                                for (
                                                                    paper
                                                                ) in final_result:
                                                                    print(
                                                                        "-" * 48,
                                                                        f"{paper_number}",
                                                                        "-" * 48,
                                                                    )
                                                                    print(
                                                                        f"\n    Similarity {result[1]:.3f}\n"
                                                                    )
                                                                    print(
                                                                        f"\n    Paper Title: {paper['paper_title']}"
                                                                    )
                                                                    print(
                                                                        f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                                    )
                                                                    print(
                                                                        f"\n{paper['paper_abstract']}\n"
                                                                    )
                                                                    print(
                                                                        f"\nSubmitted: {paper['paper_submission_date']}"
                                                                    )
                                                                    print(
                                                                        "-" * 100,
                                                                    )
                                                                    final_result.clear()
                                                                    input("\n")
                                            case 3:
                                                clear()
                                                paper_number = 0
                                                for result in results:
                                                    if (result[1]) != 0:
                                                        paper_number += 1
                                                        paper = next(
                                                            item
                                                            for item in data
                                                            if item["paper_id"]
                                                            == result[0]
                                                        )
                                                        paper_authors = [
                                                            author.lower()
                                                            for author in paper[
                                                                "paper_authors"
                                                            ]
                                                        ]
                                                        print(
                                                            "-" * 48,
                                                            f"{paper_number}",
                                                            "-" * 48,
                                                        )
                                                        print(
                                                            f"\n    Similarity {result[1]:.3f}\n"
                                                        )
                                                        print(
                                                            f"\n    Paper Title: {paper['paper_title']}"
                                                        )
                                                        print(
                                                            f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                        )
                                                        print(
                                                            f"\n{paper['paper_abstract']}\n"
                                                        )
                                                        print(
                                                            f"\nSubmitted: {paper['paper_submission_date']}"
                                                        )
                                                        print(
                                                            "-" * 100,
                                                        )
                                                        input("\n")
                                            case _:
                                                clear()
                                                print("**** Filters ****\n")
                                                print("1) Filter by authors names")
                                                print("2) Filter by date")
                                                print("3) No filter")
                                                filter = 0

                                    except ValueError:
                                        clear()
                                        print("**** Filters ****")
                                        print("1) Filter by authors names")
                                        print("2) Filter by date")
                                        print("3) No filter")
                                        filter = 0

                            case 3:
                                clear()
                                print("**** Enter your query ****")
                                print("\nA query can consist of any ammount of words\n")
                                query = input("Query : ")
                                if query == "":
                                    clear()
                                    print(
                                        "Your given query is empty! Returning a random and interesting paper..."
                                    )
                                    time.sleep(2)
                                    clear()
                                    random_id = random.randint(0, len(data))
                                    random_paper = data[random_id]
                                    print("-" * 100)
                                    print(
                                        f"\nPaper Title: {random_paper['paper_title']}"
                                    )
                                    print(
                                        f"Paper Authors: {', '.join(random_paper['paper_authors'])}\n"
                                    )
                                    print(f"\n{random_paper['paper_abstract']}\n")
                                    print(
                                        f"\nSubmitted: {random_paper['paper_submission_date']}"
                                    )
                                    print(
                                        "-" * 100,
                                    )
                                    input("\n")
                                    break
                                results = algorithms.okapi_bm25(query, tokenized_data)
                                sorted_results = -np.sort(-results)
                                check_results = [
                                    int(item) for item in results if int(item) != 0
                                ]
                                if not check_results:
                                    clear()
                                    input("No Result...")
                                    clear()
                                    break
                                clear()
                                print("**** Filters ****\n")
                                print("1) Filter by authors names")
                                print("2) Filter by date")
                                print("3) No filter")
                                filter = 0
                                while filter == 0:
                                    try:
                                        filter = int(input("\nEnter an option : "))
                                        match filter:
                                            case 1:
                                                clear()
                                                authors_names = (
                                                    input(
                                                        "Enter authors names, seperated by a comma (,) : "
                                                    )
                                                    .strip()
                                                    .lower()
                                                    .split(sep=",")
                                                )
                                                final_result = list()
                                                paper_number = 0
                                                for index in range(len(sorted_results)):
                                                    if sorted_results[index] != 0:
                                                        paper = next(
                                                            item
                                                            for item in data
                                                            if item["paper_id"]
                                                            == index + 1
                                                        )
                                                        paper_authors = [
                                                            author.lower()
                                                            for author in paper[
                                                                "paper_authors"
                                                            ]
                                                        ]
                                                        if all(
                                                            authors in paper_authors
                                                            for authors in authors_names
                                                        ):
                                                            paper_number += 1
                                                            final_result.append(paper)
                                                        if final_result:
                                                            for paper in final_result:
                                                                print(
                                                                    "-" * 48,
                                                                    f"{paper_number}",
                                                                    "-" * 48,
                                                                )
                                                                print(
                                                                    f"\n    Similarity {sorted_results[index]:.3f}\n"
                                                                )
                                                                print(
                                                                    f"\n    Paper Title: {paper['paper_title']}"
                                                                )
                                                                print(
                                                                    f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                                )
                                                                print(
                                                                    f"\n{paper['paper_abstract']}\n"
                                                                )
                                                                print(
                                                                    f"\nSubmitted: {paper['paper_submission_date']}"
                                                                )
                                                                print(
                                                                    "-" * 100,
                                                                )
                                                                final_result.clear()
                                                                input("\n")
                                            case 2:
                                                clear()
                                                date_is_okay = False
                                                operations = ["n", "o"]
                                                while not date_is_okay:
                                                    date = input(
                                                        "Enter date (day/month/year) : "
                                                    )
                                                    operation = input(
                                                        "You want newer or older papers than the given date? ( n/o ) : "
                                                    )
                                                    try:
                                                        user_input_date = (
                                                            datetime.strptime(
                                                                date, "%d/%m/%Y"
                                                            )
                                                        )
                                                        if operation not in operations:
                                                            input(
                                                                "Wrong operation.\nPress any key to re-enter your data..."
                                                            )
                                                            clear()
                                                            continue
                                                        date_is_okay = True

                                                    except ValueError:
                                                        input(
                                                            "Wrong format.\nPress any key to re-enter you data..."
                                                        )
                                                        clear()
                                                        continue
                                                final_result = list()
                                                paper_number = 0
                                                for index in range(len(sorted_results)):
                                                    if sorted_results[index] != 0:
                                                        paper = next(
                                                            item
                                                            for item in data
                                                            if item["paper_id"]
                                                            == index + 1
                                                        )
                                                        paper_authors = [
                                                            author.lower()
                                                            for author in paper[
                                                                "paper_authors"
                                                            ]
                                                        ]
                                                        paper_date = datetime.strptime(
                                                            paper[
                                                                "paper_submission_date"
                                                            ],
                                                            "%d %B, %Y",
                                                        )
                                                        if operation == "n":
                                                            if (
                                                                paper_date
                                                                > user_input_date
                                                            ):
                                                                paper_number += 1
                                                                final_result.append(
                                                                    paper
                                                                )
                                                        elif operation == "o":
                                                            if (
                                                                paper_date
                                                                < user_input_date
                                                            ):
                                                                paper_number += 1
                                                                final_result.append(
                                                                    paper
                                                                )
                                                        if final_result:
                                                            for paper in final_result:
                                                                print(
                                                                    "-" * 48,
                                                                    f"{paper_number}",
                                                                    "-" * 48,
                                                                )
                                                                print(
                                                                    f"\n    Similarity {sorted_results[index]:.3f}\n"
                                                                )
                                                                print(
                                                                    f"\n    Paper Title: {paper['paper_title']}"
                                                                )
                                                                print(
                                                                    f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                                )
                                                                print(
                                                                    f"\n{paper['paper_abstract']}\n"
                                                                )
                                                                print(
                                                                    f"\nSubmitted: {paper['paper_submission_date']}"
                                                                )
                                                                print(
                                                                    "-" * 100,
                                                                )
                                                                final_result.clear()
                                                                input("\n")
                                            case 3:
                                                clear()
                                                paper_number = 0
                                                for index in range(len(sorted_results)):
                                                    if sorted_results[index] != 0:
                                                        paper_number += 1
                                                        paper = next(
                                                            item
                                                            for item in data
                                                            if item["paper_id"]
                                                            == index + 1
                                                        )
                                                        paper_authors = [
                                                            author.lower()
                                                            for author in paper[
                                                                "paper_authors"
                                                            ]
                                                        ]
                                                        print(
                                                            "-" * 48,
                                                            f"{paper_number}",
                                                            "-" * 48,
                                                        )
                                                        print(
                                                            f"\n    Similarity {sorted_results[index]:.3f}\n"
                                                        )
                                                        print(
                                                            f"\n    Paper Title: {paper['paper_title']}"
                                                        )
                                                        print(
                                                            f"    Paper Authors: {', '.join(paper['paper_authors'])}\n"
                                                        )
                                                        print(
                                                            f"\n{paper['paper_abstract']}\n"
                                                        )
                                                        print(
                                                            f"\nSubmitted: {paper['paper_submission_date']}"
                                                        )
                                                        print(
                                                            "-" * 100,
                                                        )
                                                        input("\n")
                                            case _:
                                                clear()
                                                print("**** Filters ****\n")
                                                print("1) Filter by authors names")
                                                print("2) Filter by date")
                                                print("3) No filter")
                                                filter = 0

                                    except ValueError:
                                        clear()
                                        print("**** Filters ****\n")
                                        print("1) Filter by authors names")
                                        print("2) Filter by date")
                                        print("3) No filter")
                                        filter = 0

                            case 4:
                                break

                            case _:
                                clear()
                                print("\n**** Select an Algorithm ****\n")
                                print("1) Boolean Retrieval")
                                print("2) Vector Space Model")
                                print("3) OKAPI BM25")
                                print("4) Previous Page\n")
                                algo = 0

                    except ValueError:
                        clear()
                        print("\n**** Select an Algorithm ****\n")
                        print("1) Boolean Retrieval")
                        print("2) Vector Space Model")
                        print("3) OKAPI BM25")
                        print("4) Previous Page\n")
                        algo = 0

            case 2:
                user_data = input("Enter you desired words (separated by a ',') : ")
                if not user_data:
                    print(
                        "User input is empty...\nWe're going to generate random words!"
                    )
                if crawler.crawler(user_data):
                    print("Rebuilding database\n")
                    data = json_reader.reader("data/data.json")
                    tokenized_data = data_tokenizer.tokenizer(data)
                    inverted_index = indexing.record_level_inverted_index(
                        tokenized_data
                    )
                    input("Finished!\nPress any key to continue...\n")
                    clear()
                else:
                    input("Data not Found.\nPress any key to continue...\n")
                    continue
            case 3:
                break

            case _:
                clear()
                continue

    except ValueError:
        clear()
