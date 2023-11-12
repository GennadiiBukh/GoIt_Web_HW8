from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

@cache
def find_by_tag(tag: str) -> list[str | None]:    
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

@cache
def find_by_author(author: str) -> list[list[Any]]:    
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result

if __name__ == '__main__':

    while True:
        command_input = input("Enter command: ")
        if not command_input or command_input.lower() == "exit":
            break 
        parts = command_input.split(":")        
        if len(parts) == 2:
            command = parts[0].lower().strip()
            value = parts[1].strip()
            match command:
                case "name":
                    print(f"Find by name: {value}")
                    print(find_by_author(value))                    
                case "tag":
                    print(f"Find by tag: {value}")
                    print(find_by_tag(value))
                case "tags":
                    values = value.split(",")                  
                    try:
                        tag1 = values[0]
                        tag2 = values[1]
                        print(f"Find by tags: {tag1},{tag2}")
                        result_1 = find_by_tag(tag1)
                        result_2 = find_by_tag(tag2)
                        result = list(set(result_1 + result_2))
                        print(result)
                    except:
                        print("Enter two tags")
                case _:
                    print("Unknown command")
        else:
            print("Incorrect command format")


