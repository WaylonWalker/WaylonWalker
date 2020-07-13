"""Add latest follower to readme."""
import os
from string import Template
import tweepy


def get_api():
    """Get tweepy api.
    
    uses environment variables to load twitter access keys
    """
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    print("consumer_key", len(consumer_key))
    print("consumer_secret", len(consumer_secret))
    print("access_token", len(access_token))
    print("access_token_secret", len(access_token_secret))

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api


def render_readme(api, template_file="template/README.md"):
    """Render readme with twitter follower."""

    latest = api.followers(count=1)[0]
    me = api.get_user("_waylonwalker")

    with open(template_file) as f:
        template = Template(f.read())

    readme = template.safe_substitute(
        me_followers_count=me.followers_count,
        latest_name=latest.name,
        latest_screen_name=latest.screen_name,
        latest_description=latest.description,
        latest_profile_image_url_https=latest.profile_image_url_https,
    )

    return readme


if __name__ == "__main__":
    api = get_api()
    readme = render_readme(api)
    with open("README.md", "w+") as f:
        f.write(readme)
