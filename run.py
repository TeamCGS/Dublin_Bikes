import os
from Dublin_Bikes import create_app

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    #app.run(host ='0.0.0.0',ssl_context='adhoc',debug='True')
    app.run(host ='0.0.0.0',ssl_context=('cert.pem', 'key.pem'))
