import argparse
import string
import sys
import time

from twitter import scraper as tscraper

DEFAULT_NUMBER = 2500
DEFAULT_PER_NODE_LIMIT = 100
DEFAULT_FOLLOWER_LIMIT = 10

"""
parser.add_argument('-nl','--node_limit',metavar="Per-Node-Limit",
    type=int,dest='limit_per_node',default=DEFAULT_PER_NODE_LIMIT,
    help="The number of posts/images to extract per node before moving to neighbor. Note: Decreasing "
            " this number increases the time it takes to run, due to twitter rate limits.")
parser.add_argument('-fl','--follower_limit',metavar="Followers-Per-Node",
    type=int,dest='limit_followers_per_node',default=DEFAULT_FOLLOWER_LIMIT,
    help="For snowball sampling, the number of neigbors to visit per node. Visit all neighbors if not listed.")
args = parser.parse_args()
"""

def argument_parsing():
    """
    Parse the arguments

    Returns args
    """

    parser = argparse.ArgumentParser(description="Scrape data from social media")
    parser.add_argument('website', choices=['twitter', 'instagram'],
                        help='The website to crawl for data')
    parser.add_argument('-n', '--number', type=int, default=DEFAULT_NUMBER,
                        dest='number', metavar='Number',
                        help="If data type is images, the number of images to "
                        + "scrape. Else the number of posts to scrape.")
    parser.add_argument('-t', '--tracking', dest='tracking_file', metavar='Tracking File',
                        default='metadata/tracking.txt',
                        help="(Twitter) A file containing a list of phrases, one per line, to track." +
                        " see https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters.html")
    return parser.parse_args()

def main():
    args = argument_parsing()

    if args.website == 'twitter':
        start_time = time.time()
        tscraper.stream_scrape(args.tracking_file,args.number)
        #tscraper.snowball_scrape('@johnalberse', number=1000, limit_per_user=-1, limit_neighbors_per_node=20)
        elapsed_time = time.time() - start_time
        print("Time elapsed: " + str(elapsed_time))

if __name__ == "__main__":
    main()
