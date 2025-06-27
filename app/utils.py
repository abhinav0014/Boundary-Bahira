import requests
from django.conf import settings

def post_to_facebook(message, link=None, image_urls=None, post_type="link"):
    """
    post_type: "link", "image_caption", "full" (article + images + link)
    """
    page_id = settings.FACEBOOK_PAGE_ID
    access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN

    if post_type == "link":
        # Post with just a link and message
        data = {
            "message": message,
            "link": link,
            "access_token": access_token,
        }
        url = f"https://graph.facebook.com/{page_id}/feed"
        return requests.post(url, data=data).json()

    elif post_type == "image_caption" and image_urls:
        # Post image(s) with title as caption
        attached_media = []
        for img_url in image_urls:
            img_res = requests.post(
                f"https://graph.facebook.com/{page_id}/photos",
                data={
                    "url": img_url,
                    "published": "false",
                    "access_token": access_token,
                }
            )
            img_id = img_res.json().get("id")
            if img_id:
                attached_media.append({"media_fbid": img_id})
        post_data = {
            "message": message,
            "attached_media": attached_media,
            "access_token": access_token,
        }
        url = f"https://graph.facebook.com/{page_id}/feed"
        return requests.post(url, data=post_data).json()

    elif post_type == "full" and image_urls:
        # Post article text, images, and link
        attached_media = []
        for img_url in image_urls:
            img_res = requests.post(
                f"https://graph.facebook.com/{page_id}/photos",
                data={
                    "url": img_url,
                    "published": "false",
                    "access_token": access_token,
                }
            )
            img_id = img_res.json().get("id")
            if img_id:
                attached_media.append({"media_fbid": img_id})
        post_data = {
            "message": f"{message}\n\nRead more: {link}",
            "attached_media": attached_media,
            "access_token": access_token,
        }
        url = f"https://graph.facebook.com/{page_id}/feed"
        return requests.post(url, data=post_data).json()

    else:
        # Fallback: just post the message
        data = {
            "message": message,
            "access_token": access_token,
        }
        url = f"https://graph.facebook.com/{page_id}/feed"
        return requests.post(url, data=data).json()