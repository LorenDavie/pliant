""" 
Access to Box.com
"""

from boxsdk import JWTAuth, Client
from boxsdk.auth import DeveloperTokenAuth
from django.conf import settings
import markdown as md


# auth = JWTAuth(
#     client_id=settings.BOX_CLIENT_ID,
#     client_secret=settings.BOX_CLIENT_SECRET,
#     enterprise_id=settings.BOX_ENTERPRISE_ID,
#     jwt_key_id=settings.BOX_JWT_KEY_ID,
#     rsa_private_key_data=settings.BOX_RSA_PRIVATE_KEY_DATA,
#     rsa_private_key_passphrase=settings.BOX_PRIVATE_KEY_PASSPHRASE,
# )

class SettingsDevTokenAuth(DeveloperTokenAuth):
    """ 
    Specialization of DeveloperTokenAuth to get token from settings.
    """
    def _refresh_developer_token(self):
        return settings.BOX_DEV_TOKEN


auth = SettingsDevTokenAuth()

#access_token = auth.authenticate_instance()

client = Client(auth)

pub_folder = client.folder(settings.BOX_PUB_FOLDER_ID)

def get_blog_items():
    """ 
    Gets all of the items for the blog.
    """
    return [ContentRenderer(item) for item in pub_folder.get_items()]

def get_blog_entry(entry_id):
    """ 
    Gets and wraps a specific blog entry.
    """
    return ContentRenderer(client.file(entry_id))

def get_case_studies():
    """ 
    Gets published items that have case study metadata.
    """
    case_studies = []
    for entry in get_blog_items():
        for meta in entry.item.get_all_metadata():
            if meta.get('caseStudy', None) == 'True':
                case_studies.append(entry)
    
    return case_studies


class ContentRenderer(object):
    """ 
    Renders the content.
    """
    def __init__(self, item):
        self.item = item
    
    def rendered_content(self):
        """ 
        Converts Markdown to HTML and cleans up output string.
        """
        return md.markdown(self.item.content().decode('utf-8'))
