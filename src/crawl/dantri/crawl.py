from tqdm import tqdm
from utils.crawl import web_utils


def get_topics(root_url: str = web_utils.ROOT_URL):
    soup = web_utils.get_soup(root_url)
    topics = soup.find_all("li", class_="has-child")
    result = []
    for topic in topics:
        topic_name = topic.find("a").text
        topic_info = {"name": topic_name, "link": []}
        submenu = topic.find("ol", class_="submenu")
        for a in submenu.find_all("a", href=True):
            path = a["href"]
            if web_utils.is_path(path) & web_utils.is_valid_url(path):
                topic_info["link"].append(path)
        result.append(topic_info)

    return result


def get_posts_link_each_topic(topic_url: str = None, num_of_pagination: int = 10):
    if web_utils.is_path(topic_url):
        topic_url = web_utils.join_with_root(topic_url)
    links = []
    soup = web_utils.get_soup(topic_url)
    for i in tqdm(range(num_of_pagination)):
        articles = soup.find_all("article", class_="article-item")
        links += [
            article["data-content-target"]
            for article in articles
            if "data-content-target" in article.attrs
        ]
        hasNext = soup.find("a", class_="page-item next", href=True)
        if not hasNext:
            break
        next_link = hasNext["href"]
        soup = web_utils.get_soup(web_utils.join_with_root(next_link))
    return links


def parse_post(post_url: str = None, main_topic: str = None):
    title = None
    content = ""
    post = {"title": title, "content": content, "category": main_topic}
    if web_utils.is_path(post_url):
        post_url = web_utils.join_with_root(post_url)
    soup = web_utils.get_soup(post_url)
    article = soup.find("article")
    if article is None:
        return None
    article_type = article["class"]
    p_tags = []

    if "d-magazine" in article_type:
        h1 = article.find("h1")
        img_cover = h1.find("img")
        if img_cover is not None:
            title = img_cover["alt"]
        else:
            title = h1.text
        div = article.find("div", class_="e-magazine__body")
        p_tags = div.find_all("p")
    elif "singular-container" in article_type:
        title = article.find("h1", class_="title-page detail").text
        div = article.find("div", class_="singular-content")
        p_tags = div.find_all("p")
    elif "photo-story" in article_type:
        title = article.find("h1", class_="e-magazine__title").text
        div = article.find("div", class_="e-magazine__body")
        p_tags = div.find_all("p")
    elif "infographic" in article_type:
        title = article.find("h1", class_="e-magazine__title").text
        content = article.find("h2", class_="e-magazine__sapo").text
    elif "blog" in article_type:
        title = article.find("h1", class_="e-magazine__title").text
        div = article.find("div", class_="e-magazine__body")
        p_tags = div.find_all("p")
    elif "dbiz" in article_type:
        title = soup.find("h1", class_="special-news__title").text
        div = article.find("div", class_="e-magazine__body")
        p_tags = div.find_all("p")
    else:
        print(f"{post_url} Cannot be scraped")
        return None

    for p in p_tags:
        content += p.text + " "

    if content == "":
        return None

    post["title"] = title
    post["content"] = content
    return post


def walk_topic(
    main_topic: str = None, topic_url: str = None, num_of_pagination: int = 10
):
    if web_utils.is_path(topic_url):
        topic_url = web_utils.join_with_root(topic_url)
    print(f"Scraping {topic_url} in {main_topic}")
    posts = []
    links = get_posts_link_each_topic(topic_url, num_of_pagination)
    for link in tqdm(links):
        post = parse_post(link, main_topic)
        if post:
            posts.append(post)
    print(f"Successfully scrape {len(posts)} posts")
    return posts
