from functions import json_reader, crawler, data_tokenizer, indexing, algorithms
import os
import numpy as np

if (os.name == "posix"):
    clear = lambda: os.system('clear')
    
elif (os.name == "nt"):
    clear = lambda: os.system('cls')
    
print("*" * 8,"Starting Search Engine","*" * 8)
print("\nWelcome to our Custom Search Engine!\n")

while 1:
    
    print("You can use the previously scraped data or start fresh!")
    print("1) Use database data")
    print("2) Start scraping")
    print("3) Exit application\n")
    try: 
        
        option = int(input("Enter an option: "))
        match option:
            
            case 1:
                
                data = json_reader.reader('data/data.json')
                tokenized_data = data_tokenizer.tokenizer(data)
                clear()
                print("\n**** Select an Algorithm ****\n")
                print("1) Boolean Retrieval")
                print("2) Vector Space Model")
                print("3) OKAPI BM25")
                print("4) Previous Page\n")
                algo = 0
                while algo == 0:
                    try: 
                        algo = int(input("Enter an option: "))
                        match algo:
                            
                            case 1:
                                inverted_index = indexing.record_level_inverted_index(tokenized_data)
                                print("Enter your Boolean query")
                                print("Query must start with a word. Single word is accepted. In case of using multiple words, each word must be separated by a boolean operator (AND/OR/NOT)") 
                                query = input("Query : ")
                                result = algorithms.boolean_retrieval(query, tokenized_data, inverted_index)
                                clear()
                                if result:
                                    for id in result:
                                        paper=next(item for item in data if item['paper_id'] == id )
                                        print("*" * 25, f"Paper {id}", "*" * 25)
                                        print(f"\n{paper['paper_abstract']}")
                                        input("\nPress any key to continute...")
                                else:
                                    input("Nothing Found. Press any key to continute...")
                                clear()
                                        
                            case 2:
                                clear()
                                print("Enter your query")
                                print("A query can consist of any ammount of words")
                                query = input("Query : ")
                                results = sorted(algorithms.vector_space_model(query, tokenized_data, data), key=lambda tup : tup[1] ,reverse=True)
                                clear()
                                if results[0][1]:
                                    for result in results:
                                        if (result[1]) != 0:
                                            paper=next(item for item in data if item['paper_id'] == result[0] )
                                            print("*" * 25, f"Paper {result[0]}", "*" * 25)
                                            print("*" * 25, f"Similarity {result[1]:.3f}", "*" * 25)
                                            print(f"\n{paper['paper_abstract']}")
                                            input("\nPress a key to continute...")
                                else:
                                    input("Nothing Found. Press any key to continute...")
                                clear()
                                        
                            case 3:
                                print("Enter your query")
                                print("A query can consist of any ammount of words")
                                query = input("Query : ")
                                results = algorithms.okapi_bm25(query, tokenized_data)
                                sorted_results = -np.sort(-results)
                                clear()
                                for index in range(len(sorted_results)):
                                    if (sorted_results[index] != 0):
                                        paper=next(item for item in data if item['paper_id'] == index+1 )
                                        print("*" * 25, f"Paper {index+1}", "*" * 25)
                                        print("*" * 25, f"Similarity {sorted_results[index]:.3f}", "*" * 25)
                                        print(f"\n{paper['paper_abstract']}")
                                        input("\nPress a key to continute...")
                                clear()
                                
                            case 4:
                                break
                            case _:
                                print("Option Not Supported!!!")
                                algo = 0
                        
                    except ValueError:
                        print("Option Not Supported!!!")
                        algo = 0
            
            case 2:
                num_words = 0
                while num_words == 0:
                    try: 
                        num_words = int(input("Enter number of words to generate and search for in arXiv (integer) :  "))
                        print("Starting Scraping...\n")
                        if (crawler.crawler()):
                            print("Scraped successfully!\n")
                        else:
                            print("Data not Found. Retry")
                            num_words = 0
                            continue
                        
                    except ValueError:
                        clear()
                        print("Enter An Integer!")
                data = json_reader.reader('data/data.json')
                tokenized_data = data_tokenizer.tokenizer(data)
                print("Select an Algorith!")
                print("1) Boolean Retrieval")
                print("2) Vector Space Model")
                print("3) OKAPI BM25")
                print("4) Previous Page\n")
                algo = 0
                while algo == 0:
                    try: 
                        algo = int(input("Enter an option: "))
                        match algo:
                            
                            case 1:
                                inverted_index = indexing.record_level_inverted_index(tokenized_data)
                                print("Enter your Boolean query")
                                print("Query must start with a word. Single word is accepted. In case of using multiple words, each word must be separated by a boolean operator (AND/OR/NOT)") 
                                query = input("Query : ")
                                result = algorithms.boolean_retrieval(query, tokenized_data, inverted_index)
                                clear()
                                if result:
                                    for id in result:
                                        paper=next(item for item in data if item['paper_id'] == id )
                                        print("*" * 25, f"Paper {id}", "*" * 25)
                                        print(f"\n{paper['paper_abstract']}")
                                        input("\nPress a key to continute...")
                                clear()
                                        
                            case 2:
                                print("Enter your query")
                                print("A query can consist of any ammount of words")
                                query = input("Query : ")
                                results = sorted(algorithms.vector_space_model(query, tokenized_data, data), key=lambda tup : tup[1] ,reverse=True)
                                clear()
                                for result in results:
                                    if (result[1]) != 0:
                                        paper=next(item for item in data if item['paper_id'] == result[0] )
                                        print("*" * 25, f"Paper {result[0]}", "*" * 25)
                                        print("*" * 25, f"Similarity {result[1]:.3f}", "*" * 25)
                                        print(f"\n{paper['paper_abstract']}")
                                        input("\nPress a key to continute...")
                                clear()
                                        
                            case 3:
                                print("Enter your query")
                                print("A query can consist of any ammount of words")
                                query = input("Query : ")
                                results = algorithms.okapi_bm25(query, tokenized_data)
                                sorted_results = -np.sort(-results)
                                clear()
                                for index in range(len(sorted_results)):
                                    if (sorted_results[index] != 0):
                                        paper=next(item for item in data if item['paper_id'] == index+1 )
                                        print("*" * 25, f"Paper {index+1}", "*" * 25)
                                        print("*" * 25, f"Similarity {sorted_results[index]:.3f}", "*" * 25)
                                        print(f"\n{paper['paper_abstract']}")
                                        input("\nPress a key to continute...")
                                clear()
                                
                            case 4:
                                break
                            case _:
                                print("Option Not Supported!!!")
                                algo = 0
                        
                    except ValueError:
                        print("Option Not Supported!!!")
                        algo = 0
            
            case 3:
                break
            
            case _:
                clear()
                print("Option Not Supported!!!\n")
                continue
    
    except ValueError:
        clear()
        print("Option Not Supported!!!\n")
