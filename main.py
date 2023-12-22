import simple_crawler, indexing


def main():
    
    if simple_crawler.crawler():
        
        index = indexing.inverted_index()
        for key, value in index.items():
            print(f" '{key}' found in Documents {value}")


if __name__ == "__main__":
    main()