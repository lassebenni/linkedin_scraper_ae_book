import os
from typing import List
import requests
import json

from models.linkedin_post import LinkedinPost
from models.linkedin_response import IncludedElement, LinkedInResponse

session = requests.Session()

url = "https://www.linkedin.com/voyager/api/graphql?variables=(start:0,origin:CLUSTER_EXPANSION,query:(keywords:fundamentals%20of%20analytics%20engineering,flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:resultType,value:List(CONTENT)),(key:searchId,value:List(15a49aba-1ed3-463a-b535-130735ab04e4)))),count:50)&queryId=voyagerSearchDashClusters.09f1c85c0e383740672f698538438a2b"

payload = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "application/vnd.linkedin.normalized+json+2.1",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "x-li-lang": "nl_NL",
    "x-li-track": '{"clientVersion":"1.13.19075","mpVersion":"1.13.19075","osName":"web","timezoneOffset":2,"timezone":"Europe/Amsterdam","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":2,"displayWidth":3840,"displayHeight":2160}',
    "x-li-page-instance": "urn:li:page:d_flagship3_search_srp_content;oX0Tee1uTwiUKIIgsZvdnA==",
    "csrf-token": "ajax:1797525637115598100",
    "x-restli-protocol-version": "2.0.0",
    "x-li-pem-metadata": "Voyager - Content SRP=search-results",
    "Connection": "keep-alive",
    "Referer": "https://www.linkedin.com/search/results/content/?keywords=fundamentals%20of%20analytics%20engineering&origin=CLUSTER_EXPANSION&searchId=15a49aba-1ed3-463a-b535-130735ab04e4&sid=yVK",
    "Cookie": os.getenv("LINKEDIN_COOKIE"),
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "DNT": "1",
    "Sec-GPC": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}


def crawl() -> dict:
    response = session.get(url, headers=headers, data=payload)
    return response.json()


def load_existing_posts(file_path):
    """Load existing posts from a JSON file."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def find_new_posts(existing_posts, new_posts):
    """Find and return posts that are new."""
    existing_posts_set = {json.dumps(post, sort_keys=True) for post in existing_posts}
    new_posts_list = [post.dict() for post in new_posts]
    new_posts_set = {json.dumps(post, sort_keys=True) for post in new_posts_list}
    return [json.loads(post) for post in new_posts_set - existing_posts_set]


def extract_posts_from_response(
    linkedin_response: LinkedInResponse,
) -> List[LinkedinPost]:
    """
    Extracts posts from the LinkedIn response and returns them as a list of dictionaries.

    :param linkedin_response: The LinkedInResponse object containing the response data.
    :return: A list of dictionaries, each representing a post.
    """
    posts: List[LinkedinPost] = []
    for included_element in linkedin_response.included:
        # Only include posts that have 'fundamentals' in the text
        if "fundamentals of analytics engineering" in included_element.summary.text.lower():
            post: LinkedinPost = LinkedinPost(
                author=included_element.title.text,
                bio=included_element.primary_subtitle.text,
                author_url=str(included_element.actor_navigation_url),
                text=included_element.summary.text,
                post_url=str(included_element.navigation_url),
            )
            posts.append(post)

    return posts


if __name__ == "__main__":
    res = crawl()
    # print(res)
    linkedin_response: LinkedInResponse = LinkedInResponse(**res)

    posts: List[LinkedinPost] = extract_posts_from_response(linkedin_response)

    # Load existing posts
    existing_posts = load_existing_posts("data/posts.json")
    print(f"Found {len(existing_posts)} existing posts:")

    # Find new posts
    new_posts = find_new_posts(existing_posts, posts)
    print(f"Found {len(new_posts)} new posts:")

    # Optionally, update the JSON file with the new combined list of posts
    combined_posts = existing_posts + [
        post.dict() for post in posts if post.dict() not in existing_posts
    ]
    with open("data/posts.json", "w") as f:
        json.dump(combined_posts, f, indent=2)
