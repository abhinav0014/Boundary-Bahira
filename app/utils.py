# import requests
# from django.conf import settings

# def post_to_facebook(message, link=None):
#     url = f"https://graph.facebook.com/{settings.FACEBOOK_PAGE_ID}/feed"
#     data = {
#         "message": message,
#         "access_token": settings.FACEBOOK_PAGE_ACCESS_TOKEN,
#     }
#     if link:
#         data["link"] = link
#     response = requests.post(url, data=data)
#     return response.json()

# def create_facebook_post(news_post):
#     access_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
#     page_id = settings.FACEBOOK_PAGE_ID
#     message = news_post.title + "\n\n" + news_post.content

#     image_urls = [img.image.url for img in news_post.images.all()]
#     if image_urls:
#         # Upload images first and collect their Facebook IDs
#         attached_media = []
#         for url in image_urls:
#             img_res = requests.post(
#                 f'https://graph.facebook.com/{page_id}/photos',
#                 data={
#                     'url': url,
#                     'published': 'false',
#                     'access_token': access_token
#                 }
#             )
#             img_id = img_res.json().get('id')
#             if img_id:
#                 attached_media.append({'media_fbid': img_id})

#         # Create post with attached images
#         post_data = {
#             'message': message,
#             'attached_media': attached_media,
#             'access_token': access_token
#         }
#         res = requests.post(
#             f'https://graph.facebook.com/{page_id}/feed',
#             data=post_data
#         )
#     else:
#         # Create post without images
#         res = requests.post(
#             f'https://graph.facebook.com/{page_id}/feed',
#             data={
#                 'message': message,
#                 'access_token': access_token
#             }
#         )
#     return res.json()

def post_to_facebook(message, link):
    pass