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


def render_follower(follower, follower_template_file="template/follower.html"):
    with open(follower_template_file) as f:
        follower_template = Template(f.read())

    follower_readme = follower_template.safe_substitute(
        follower_name=follower.name,
        follower_screen_name=follower.screen_name,
        follower_description=follower.description,
        follower_profile_image_url_https=follower.profile_image_url_https,
    )

    return follower_readme


def render_readme(
    api,
    template_file="template/follower.svg",
    follower_template="template/follower.html",
):
    """Render readme with twitter follower."""

    latest_followers = "".join(
        [render_follower(follower) for follower in api.followers(count=3)]
    )

    me = api.get_user("_waylonwalker")

    with open(template_file) as f:
        template = Template(f.read())

    readme = template.safe_substitute(
        me_followers_count=me.followers_count, latest_followers=latest_followers
    )

    return readme


if __name__ == "__main__":
    api = get_api()
    readme = render_readme(api)
    with open("follower.svg", "w+") as f:
        f.write(readme)
