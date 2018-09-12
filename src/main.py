import collections
import wikipediaapi
import concurrent.futures
import sys


def get_title(name):
    return (name.split("/"))[-1]


def count_single(name):
    wiki_wiki = wikipediaapi.Wikipedia(
        language="en", extract_format=wikipediaapi.ExtractFormat.WIKI
    )

    wiki = wiki_wiki.page(get_title(name))
    counter = collections.Counter(wiki.text.split())
    return counter


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(count_single, page.strip()) for page in sys.stdin]

        main_count = collections.Counter()
        for future in concurrent.futures.as_completed(futures):
            main_count += future.result()

        print(main_count.most_common(10))
