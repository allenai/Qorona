import json
import random
import re
import requests
import numpy as np
import time
from tqdm import tqdm

corona_patterns = [
    "coronavirus",
    "covid",
    "virus"
]

number_may_space = re.compile(r'\d may ')
number_may_end = re.compile(r'\d may$')
space_may_numbers = re.compile(r' may \d\d')
begin_may_numbers = re.compile(r'^may \d\d')


def query_and_return(prefix):
    time.sleep(0.8)
    r = requests.get(f"http://google.com/complete/search?client=chrome&q={prefix}")
    if r.status_code == 200:
        # save it
        content = r.content.decode("utf-8", errors='replace')
        content = json.loads(content)
        return content[1]
    else:
        return []


def crawl_questions_continue():
    # then, augment the results
    all_results = []
    with open("data/queries.txt") as f:
        for l in f.readlines():
            all_results.append(l.replace("\n", ""))

    for idx in tqdm(range(0, 500)):
        random.shuffle(all_results)
        for result in all_results:
            idx_cut = 24 + idx * 5

            # find the index of the next space
            try:
                idx_cut = result.index(" ", idx_cut)
            except:
                idx_cut = len(result)

            # skip is it is of the form `d may`, `may dd`, etc.
            if number_may_space.search(result) is not None:
                print(f" ** skipping because it matches the patten: {number_may_space}")
                continue

            if number_may_end.search(result) is not None:
                print(f" ** skipping because it matches the patten: {number_may_end}")
                continue

            if begin_may_numbers.search(result) is not None:
                print(f" ** skipping because it matches the patten: {begin_may_numbers}")
                continue

            if space_may_numbers.search(result) is not None:
                print(f" ** skipping because it matches the patten: {space_may_numbers}")
                continue

            prefix = result[:idx_cut + 1]

            matching_patterns = [q for q in corona_patterns if q in f" {prefix.lower()} "]
            if len(matching_patterns) == 0:
                # print(f">>>> skipping: {l} before it does not have a `corona` prefix")
                continue
            else:
                print(f"matching_patterns: {matching_patterns}")

            for i in np.arange(ord('a'), 1 + ord('z')):
                prefix1 = prefix + chr(i)
                print(f" ** {prefix1}")
                output = query_and_return(prefix1)
                # all_results.extend(output)
                for out in output:
                    if len(out) < 15:
                        print(f" ----> {out}: X")
                        continue
                    if out not in all_results:
                        all_results.append(out)
                        print(f" ----> {out}: Y")
                    else:
                        print(f" ----> {out}: X2")
                print(len(all_results))
            all_results = list(set(all_results))
            all_results = sorted(all_results)
            f = open("data/queries.txt", "w")
            f.write("\n".join(all_results))
            f.close()


if __name__ == "__main__":
    crawl_questions_continue()
