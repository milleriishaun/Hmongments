from urllib.parse import urlparse

# Get domain name (example.com)
def get_domain_name(url):
    try:
        # Split the list up to chunk up
        results = get_sub_domain_name(url).split('.')
        # get second to last item, and the last item
        return results[-2] + '.' + results[-1]
    except:
        return ''


# Get subdomain name only (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc #network location is returned
    except:
        return '' #have to return something