from bs4 import BeautifulSoup

def get_email_body(message):
    """ Retorna o texto do corpo do email.
    """
    if message.is_multipart():
            for part in message.walk():
                partType = part.get_content_type()
                ## Get Body ##
                if partType == "text/plain" and "attachment" not in part:
                    html_body = part.get_payload()
    else:
        html_body = message.get_payload(decode=True).decode('utf-8')
    
    # Analisa o html do corpo e extrai o texto
    soup = BeautifulSoup(html_body, 'html.parser')
    try:
        body = soup.body.text
    except AttributeError:
        body = soup.text

    return body
