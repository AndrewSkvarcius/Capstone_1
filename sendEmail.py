from __future__ import print_function
import clicksend_client
from clicksend_client.rest import ApiException
from clicksend_client import EmailRecipient
from clicksend_client import EmailFrom
from clicksend_client import Attachment

# Configure HTTP basic authorization: BasicAuth
configuration = clicksend_client.Configuration()
configuration.username = 'andrewskvarcius@gmail.com'
configuration.password = '843F2488-18F6-978D-F072-CF6814380FE3'

# create an instance of the API class
api_instance = clicksend_client.TransactionalEmailApi(clicksend_client.ApiClient(configuration))
email_receipient=EmailRecipient(email='dungeondyesnyc@gmail.com',name='abc')
email_from=EmailFrom(email_address_id='27421',name='abc')
attachment=Attachment(content='ZmlsZSBjb250ZW50cw==',
                      type='text/plain',
                      filename='text.txt',
                      disposition='attachment',
                      content_id='text')
# Email | Email model
email = clicksend_client.Email(to=[email_receipient],
                              cc=[email_receipient],
                              bcc=[email_receipient],
                              _from=email_from,
                              subject="Test 123",
                              body="send EMAIL TEST MESSAGE",
                              attachments=[attachment],
                              schedule=14785562325) 

try:
    # Send transactional email
    api_response = api_instance.email_send_post(email)
    print(api_response)
except ApiException as e:
    print("Exception when calling TransactionalEmailApi->email_send_post: %s\n" % e)