import requests
import os
import logging
from django.conf import settings
from django.contrib.sites.models import Site

logger = logging.getLogger(__name__)

def post_to_facebook(post, post_type='full', include_title=True, include_excerpt=True, 
                    include_image=True, include_link=True, image=None):
    """
    Post a NewsPost to Facebook with configurable options
    
    Args:
        post: NewsPost instance to be shared
        post_type: 'full', 'image', or 'link'
        include_title: Whether to include the title in the post
        include_excerpt: Whether to include content excerpt
        include_image: Whether to include image(s)
        include_link: Whether to include link back to the site
        image: Specific NewsPostImage instance to use (optional)
    
    Returns:
        dict: Response from the Facebook API
        bool: True if successful, False otherwise
    """
    try:
        # Get Facebook credentials from settings
        page_token = settings.FACEBOOK_PAGE_ACCESS_TOKEN
        page_id = settings.FACEBOOK_PAGE_ID
        
        if not page_token or not page_id:
            logger.error("Facebook API credentials not configured")
            return False, {"error": "API credentials missing"}
            
        # Build post message components
        message_parts = []
        
        # Add title if requested
        if include_title and post_type != 'image':
            message_parts.append(post.title)
        
        # Add content excerpt if requested
        if include_excerpt and post_type != 'image' and post_type != 'link':
            # Create a readable excerpt (about 2-3 sentences)
            content = post.content
            excerpt_length = min(280, len(content))
            excerpt = content[:excerpt_length]
            if len(content) > excerpt_length:
                # Try to end at a sentence or period
                last_period = excerpt.rfind('.')
                if last_period > excerpt_length * 0.6:  # At least 60% of the excerpt
                    excerpt = excerpt[:last_period+1]
                else:
                    excerpt = excerpt + '...'
            message_parts.append(excerpt)
        
        # Build the site URL
        try:
            current_site = Site.objects.get_current()
            base_url = f"https://{current_site.domain}"
        except:
            # Fallback if Sites framework isn't properly configured
            base_url = "https://boundarybahira.com"  # Replace with your actual domain
            
        post_url = f"{base_url}/news/{post.id}/"
        
        if include_link and post_type != 'image':
            # For link type posts, we'll use the link property
            # For full posts, append to the message
            if post_type == 'link':
                link = post_url
            else:
                message_parts.append(f"Read more: {post_url}")
                link = None
        else:
            link = None
        
        # Join message parts with double newlines for readability
        message = "\n\n".join(message_parts) if message_parts else ""
        
        # Handle different post types
        if post_type == 'image' or (include_image and (image or post.images.exists())):
            # Determine which image to use
            if image:
                img_instance = image
            else:
                # Use the first image attached to the post
                img_instance = post.images.first() if post.images.exists() else None
                
            if img_instance:
                # Image posting with optional caption
                try:
                    # Check if the file exists and is accessible
                    img_path = img_instance.image.path
                    if not os.path.exists(img_path):
                        logger.error(f"Image file not found: {img_path}")
                        # Fall back to posting without image
                        return post_feed_content(page_id, page_token, message, link)
                        
                    # Prepare for photo upload with caption
                    api_url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
                    
                    data = {
                        'access_token': page_token,
                    }
                    
                    # For photo posts, use caption instead of message
                    if message:
                        data['caption'] = message
                        
                    # Upload the photo
                    with open(img_path, 'rb') as img_file:
                        files = {'source': img_file}
                        response = requests.post(api_url, data=data, files=files)
                        
                    # Check response and handle result
                    if response.status_code == 200:
                        result = response.json()
                        logger.info(f"Successfully posted image to Facebook: {result.get('id', 'unknown ID')}")
                        return True, result
                    else:
                        logger.error(f"Failed to post image: {response.status_code} - {response.text}")
                        # Fall back to posting without image
                        return post_feed_content(page_id, page_token, message, link)
                        
                except Exception as e:
                    logger.exception(f"Error posting image to Facebook: {str(e)}")
                    # Fall back to posting without image
                    return post_feed_content(page_id, page_token, message, link)
            else:
                # No image available, fall back to regular post
                return post_feed_content(page_id, page_token, message, link)
        else:
            # Regular post without image
            return post_feed_content(page_id, page_token, message, link)
            
    except Exception as e:
        logger.exception(f"Unexpected error posting to Facebook: {str(e)}")
        return False, {"error": str(e)}

def post_feed_content(page_id, page_token, message, link=None):
    """
    Helper function to post content to the Facebook feed
    """
    api_url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
    
    data = {
        'access_token': page_token,
    }
    
    if message:
        data['message'] = message
        
    if link:
        data['link'] = link
        
    try:
        response = requests.post(api_url, data=data)
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Successfully posted to Facebook feed: {result.get('id', 'unknown ID')}")
            return True, result
        else:
            logger.error(f"Failed to post to feed: {response.status_code} - {response.text}")
            return False, response.json() if response.content else {"error": f"Status code: {response.status_code}"}
    except Exception as e:
        logger.exception(f"Error posting to Facebook feed: {str(e)}")
        return False, {"error": str(e)}