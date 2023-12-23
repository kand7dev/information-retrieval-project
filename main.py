import simple_crawler, indexing


def main():
    
    if simple_crawler.crawler():
        
        record_level_index = indexing.record_level_inverted_index()
        for key, value in record_level_index.items():
            print(f" '{key}' found in Documents {value}")
            

        word_level_index = indexing.word_level_inverted_index()
        
        for key, value in word_level_index.items():
            coordinates, times = value
            print(f"Key -> {key} , Found At -> {coordinates} , Total Times -> {times}")
           
            
        # Verbose Output (uncomment to see)

        # for key, value in word_level_index.items():
        #     my_tuple, times = value
        #     for t in my_tuple:
        #        print(f"Key -> {key} : Found In Document -> {t[0]} : Found At Index -> {t[1]}")
        #     print(f"Total Times -> {times}")


if __name__ == "__main__":
    main()