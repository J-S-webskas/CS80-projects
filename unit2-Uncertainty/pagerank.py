import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

"""
Feedback:

Pretty good job! Nice use of comprehensions to build dicts.
In iterate_pagerank, invoking max() on all the diffs requires iterating over all the ranks 
but if you find a single diff above threshold you could break early ('short-circuit'). 
There's also no need to make a copy of the new ranks
"""

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}
    if not corpus[page]:  # If page does not link to any page, all key have value 1/N
        return {key: 1/len(corpus) for key in corpus}     
    for key in corpus:
        distribution[key] = (1 - damping_factor) / len(corpus)  # All pages add
        if key in corpus[page]:
            distribution[key] += damping_factor/len(corpus[page])  # Only pages linked to p add
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page = random.choice(list(corpus.keys()))
    visited = {key: 0 for key in corpus}  # Initialize
    visited[page] += 1
    for _ in range(n-1):
        distribution = transition_model(corpus, page, damping_factor)  # Probability distribution
        page = random.choices(list(distribution.keys()), list(distribution.values()), k = 1)[0]  # Weighted random page
        visited[page] += 1
    return {key : value/n for key, value in visited.items()}  # All value/n adds up to 1

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # duplicate links on the same page are treated as a single link, and links from a page to itself are ignored as well
    prev_rank = {key: 1/len(corpus) for key in corpus.keys()}
    new_rank = {}
    while True:
        for p in corpus:
            const = 0
            for i, valuei in corpus.items():
                if p in valuei:  # If i links to page p
                    const += prev_rank[i]/len(valuei)
                if len(valuei) == 0:  # if page i does not link to any
                    const +=  prev_rank[i]/len(corpus)  # Links to all pages
            new_rank[p] = (1 - damping_factor)/ len(corpus) + damping_factor * const  # Formula
            if abs(prev_rank[p] - new_rank[p]) > 0.001:
                prev_rank = new_rank  # No need to copy because new_rnak is rebuilt with every iteration
                break  # No need to check other pages


if __name__ == "__main__":
    main()
