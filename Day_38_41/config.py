
import os
import argparse

def get_access(args):
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-2' # change to your own region
    os.environ["AWS_ACCESS_KEY_ID"] = args['key'] #'*********AHZ4IVO******'
    os.environ["AWS_SECRET_ACCESS_KEY"] = args['passkey'] #'****4W4*******QW1W*****************'

if __name__=='__main__':
  
    parser = argparse.ArgumentParser()

    # Create another group for authentication
    auth_group = parser.add_argument_group('Authentication', 'Login credentials')

    auth_group.add_argument("-k", "--key", help="Username to connect to a database server")
    auth_group.add_argument("-s", "--passkey", help="Password to connect to a database server")

    args = parser.parse_args()

    args = vars(args)
    print(args)
#     get_access(args)
