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
    prob_distribution = {}
    num_pages = len(corpus)
    links = corpus[page]
    
    if links:
        # Links exist from the current page
        for linked_page in links:
            prob_distribution[linked_page] = damping_factor / len(links)
        
        # Probability of choosing any page at random
        for p in corpus:
            if p in prob_distribution:
                prob_distribution[p] += (1 - damping_factor) / num_pages
            else:
                prob_distribution[p] = (1 - damping_factor) / num_pages
    else:
        # No links exist from the current page (randomly choose any page)
        for p in corpus:
            prob_distribution[p] = 1 / num_pages
    
    return prob_distribution



def sample_pagerank(corpus, damping_factor, n):
    page_rank = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))
    
    for _ in range(n):
        page_rank[current_page] += 1
        transition_probs = transition_model(corpus, current_page, damping_factor)
        next_page = random.choices(list(transition_probs.keys()), weights=transition_probs.values(), k=1)[0]
        current_page = next_page
    
    # Normalize the counts to get probabilities
    for page in page_rank:
        page_rank[page] /= n
    
    return page_rank



def iterate_pagerank(corpus, damping_factor):
    num_pages = len(corpus)
    page_rank = {page: 1 / num_pages for page in corpus}
    new_page_rank = page_rank.copy()
    threshold = 0.001
    
    while True:
        for page in corpus:
            rank_sum = 0
            for linking_page in corpus:
                if page in corpus[linking_page]:
                    rank_sum += page_rank[linking_page] / len(corpus[linking_page])
                if not corpus[linking_page]:
                    rank_sum += page_rank[linking_page] / num_pages
            new_page_rank[page] = (1 - damping_factor) / num_pages + damping_factor * rank_sum
        
        # Check for convergence
        if all(abs(new_page_rank[page] - page_rank[page]) < threshold for page in page_rank):
            break
        page_rank = new_page_rank.copy()
    
    return new_page_rank



if __name__ == "__main__":
    main()
