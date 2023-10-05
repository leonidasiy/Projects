import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
    probDistribution = dict()
    defaultProb = 1 / len(corpus) * (1 - damping_factor)
    if not corpus[page]:
        for nextPage in corpus:
            probDistribution[nextPage] = 1 / len(corpus)
    else:
        for nextPage in corpus:
            if nextPage in corpus[page]:
                probDistribution[nextPage] = 1 / len(corpus[page]) * damping_factor + defaultProb
            else:
                probDistribution[nextPage] = defaultProb
    return probDistribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    start = random.choice(list(corpus.keys()))
    sampleCount = {start: 1}
    currentPage = start
    for i in range(n-1):
        probDistribution = transition_model(corpus, currentPage, damping_factor)
        nextPage = random.choices(list(probDistribution.keys()), weights=list(probDistribution.values()), k=1)[0]
        if nextPage in sampleCount:
            sampleCount[nextPage] += 1
        else:
            sampleCount[nextPage] = 1
        currentPage = nextPage    
    return {key: value/n for key, value in sampleCount.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = dict.fromkeys(list(corpus.keys()), 1/len(corpus))
    convergence = False
    while not convergence:
        currentPagerank = dict(pagerank)
        for page in pagerank:
            pagerankSum = 0
            for possiblePage in corpus:
                if page in corpus[possiblePage]:
                    pagerankSum += pagerank[possiblePage] / len(corpus[possiblePage])
                elif not corpus[possiblePage]:
                    pagerankSum += pagerank[possiblePage] / len(corpus)
            pagerank[page] = (1 - damping_factor) / len(corpus) + damping_factor * pagerankSum
        convergence = True
        for page in pagerank:
            if abs(pagerank[page] - currentPagerank[page]) > 0.001:
                convergence = False
    return pagerank


if __name__ == "__main__":
    main()
