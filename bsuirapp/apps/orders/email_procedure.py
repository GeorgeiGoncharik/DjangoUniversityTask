def render_template(template, **kwargs):
    # check if template exists
    import os, sys
    if not os.path.exists(template):
        print('No template file present: %s' % template)
        sys.exit()

    import jinja2
    templateLoader = jinja2.FileSystemLoader(searchpath="/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)
    return templ.render(**kwargs)


def send_email(to, sender='georgii.goncharik@gmail.com', cc=None, bcc=None, subject=None, body=None):
    import logging
    import smtplib
    # Import the email modules
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.header import Header
    from email.utils import formataddr

    # convert TO into list if string
    if type(to) is not list:
        to = to.split()

    to_list = to + [cc] + [bcc]
    to_list = filter(None, to_list)  # remove null emails

    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['Subject'] = subject
    msg['To'] = ','.join(to)
    msg['Cc'] = cc
    msg['Bcc'] = bcc
    msg.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com')  # or your smtp server

    # This retrieves a Python logging instance (or creates it)
    log = logging.getLogger(__name__)
    try:
        log.info('sending email xxx')
        server.sendmail(sender, to_list, msg.as_string())
    except Exception as e:
        log.error('Error sending email')
        log.exception(str(e))
    finally:
        server.quit()