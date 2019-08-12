# Instagram-page-posts-scrapper


Get Instagram posts/profile/hashtag data without using Instagram API. 
This crawler could fail due to updates on instagram’s website. If you encounter any problems, please contact me.

Install
Make sure you have Chrome browser installed.
Download chromedriver and put it into bin folder: ../chromedriver
Install Selenium: pip install -r requirements.txt
cp inscrawler/secret.py.dist inscrawler/secret.py
Crawler
Usage
positional arguments:
  mode
    options: [posts, posts_full, profile, hashtag]

optional arguments:
  -n NUMBER, --number NUMBER
                        number of returned posts
  -u USERNAME, --username USERNAME
                        instagram's username
  -t TAG, --tag TAG     instagram's tag name
  -o OUTPUT, --output OUTPUT
                        output file name(json format)

  --debug               see how the program automates the browser

  --fetch_comments      fetch comments
  # Turning on the flag might take forever to fetch data if there are too many commnets.

  --fetch_likes_plays   fetch like/play number

  --fetch_likers        fetch all likers
  # Instagram might have rate limit for fetching likers. Turning on the flag might take forever to fetch data if there are too many likes.

  --fetch_mentions      fetch users who are mentioned in the caption/comments (startwith @)

  --fetch_hashtags      fetch hashtags in the caption/comments (startwith #)






Usage
