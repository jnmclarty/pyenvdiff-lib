from .version import __version__
from .import_macros import import_os, import_json, import_urllib_x

os = import_os()
json = import_json()
Request, urlopen, HTTPError = import_urllib_x()

PUBLIC_SERVER = 'https://osa.pyenvdiff.com'
FREE_API_KEY = 'qcjODGX4iw3cEPIQR7Jn77uTKSuQOvwS4Q4z7AwR'

class Client(object):

    DEFAULT_SERVER = None # FEEL FREE TO PATCH THIS CODE HERE WITH A HARDCODED SERVER Eg. 'https://osa.pyenvdiff.com'
    LOCAL_SERVER = r'http://localhost:8080'
    DEFAULT_API_KEY = FREE_API_KEY
    SUBMISSION_ENDPOINT = r'/submit'

    def __init__(self, server=None, api_key=None):

        server = server or os.environ.get('PYENVDIFF_SERVER', self.DEFAULT_SERVER)

        if server is not None:
            if server.upper() == 'DEFAULT':
                server = self.DEFAULT_SERVER

        if server is not None:
            if server.upper() == 'LOCAL':
                server = self.LOCAL_SERVER

        api_key = api_key or os.environ.get('PYENVDIFF_API_KEY', self.DEFAULT_API_KEY) or FREE_API_KEY

        if api_key is not None:
            if api_key.upper() == 'DEFAULT':
                api_key = self.DEFAULT_API_KEY

        if server is None:
            raise Exception("Must specify a server.  Found None.")

        self.server = server
        self.api_key = api_key

    def send(self, environment,
             organization=None,
             group=None,
             subgroup=None,
             username=None,
             email=None,
             domain=None,
             application=None,
             version=None,
             tags=None):
        data = {'pyenvdiff_version': __version__}

        try:
            from datetime import datetime as dt # make an import macro for this
            date = dt.now().isoformat()
        except:
            date = None

        data['user_meta'] = {'organization': organization,
                             'group': group,
                             'subgroup': subgroup,
                             'username': username,
                             'email': email,
                             'domain': domain,
                             'application': application,
                             'version': version,
                             'tags': tags,
                             'date': date}

        data['environment'] = environment.info()

        data = json.dumps(data)
        data = data.encode('utf-8')
        clen = len(data)

        server = self.server
        api_key = self.api_key

        print("Posting environment information to " + server)

        if api_key == FREE_API_KEY:
            print("Attempting to use the demo API KEY.  It's throttled.  If this fails, consider requesting your own.")
            print("Once you have your own, set an environment variable PYENVDIFF_API_KEY to your API key.")
        elif api_key == 'NOT_REQUIRED':
            pass # Backwards compatibility
        else:
            print("Using API KEY: " + api_key[:6] + "...")


        req = Request(server + self.SUBMISSION_ENDPOINT, data, {'x-api-key': api_key,
                                                                      'Content-Type': 'application/json',
                                                                      'Content-Length': clen})

        try:
            f = urlopen(req)
        except HTTPError as e:
            if e.code == 429:
                print("You are getting throttled.  Try again later.")
                if api_key == FREE_API_KEY:
                    print("You are using the demo API KEY.  You can try again in a moment, or request your own API KEY.")
                elif api_key == 'NOT_REQUIRED':
                    pass # backwards compatibility
                else:
                    print("Even the personal API KEYs have limits.  What are you doing?  Let the maintainer know, he might boost your API limit.")
                return ""
            else:
                return "HTTPError: " + str(e.code) + ". Are you using the latest release? Yes? File a github issue if this keeps happening"

        response = f.read()

        response = json.loads(response.decode('utf-8'))

        f.close()

        response_type = response.get('response_type', None)

        if response_type == 'environment_info_write':
            return '''Environment #{environment_number} posted at {timestamp} can be viewed @\n{read_url}\n...or diffed with the server's environment @\n{diff_url}\n...or replace the 0 in the URL with any other Environment #.'''.format(**response)

        if response_type == 'environment_diff':
            print(response)


        if response.get('result', None) == 'OK':
            sha = response['sha']

            print("Successful POST, use SHA %s for reference or comparison." % sha)
            if 'pyenvdiff.com' in server:
                print("Eg. http://pyenvdiff.com/view.html?sha=%s" % sha)

        return response.get("message", "No response message provided. Something strange happened on the server.  This shouldn't happen. Please file a github issue. " + str(response))

class PublicClient(Client):

    DEFAULT_SERVER = 'https://osa.pyenvdiff.com'
    LOCAL_SERVER = 'http://localhost:8080'
    DEFAULT_API_KEY = FREE_API_KEY

class HubClient(Client):

    DEFAULT_SERVER = r'http://localhost:8080'
    LOCAL_SERVER = r'http://localhost:8080'
    SUBMISSION_ENDPOINT = r'/environment_info'

    def __init__(self, server=None):

        server = server or os.environ.get('PYENVDIFF_SERVER', self.DEFAULT_SERVER)

        if server is not None:
            if server.upper() == 'DEFAULT':
                server = self.DEFAULT_SERVER

        if server is not None:
            if server.upper() == 'LOCAL':
                server = self.LOCAL_SERVER

        if server is None:
            raise Exception("Must specify a server.  Found None.")

        self.server = server
        self.api_key = 'NOT_REQUIRED'
