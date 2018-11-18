
if __name__ == '__main__':

    from pickle import dump, HIGHEST_PROTOCOL

    from pyenvdiff.version import __version__ as v

    from .bottle.bottle import route, run, response, request, template
    from .environment import Environment, EnvironmentDiff
    from .import_macros import import_json
    from .version import __version__ as v

    from datetime import datetime

    try:
        import ghdiff
        GHDIFF_MSG = ""
    except:
        GHDIFF_MSG = "PyEnvDiff is dependency free, but the diffs are easier to read if you manually install ghdiff from pypi.  <code>pip install ghdiff</code> does it."

    DEVELOP_MODE = False

    title = "PyEnvDiff Environment Diff Tool Hub v" + v
    header = "<h1>Welcome to " + title + " for M2M & H2M Environment Information & Difference Server!</h1>For more information see the <a href='http://pyenvdiff.com'>home page</a> or checkout the <a href='http://github.com/jnmclarty/pyenvdiff-lib'>github</a>"

    env_info_store = ['The first entry in this list is never used, the rest of the elements are a tuple of the form (environment info, timestamp)']

    HOME_TEMPLATE = """<html><h1>""" + title + """</h1>
                       <p>View Environment Information for the hub at <a href=/environment_info>/environment_info</a>
                       
                       % for i, (posted_data, ts) in enumerate(stored_envs):
                         <p>View Environment Information for <a href=/environment_info/{{i+1}}>Env #{{i+1}}</a> from {{ts}}
                       % end
                       
                       % for a, b, hub in options:
                         <p>Compare <a href=/environment_diff_view/{{a}}/{{b}}>Env #{{a}} {{hub}} and Env #{{b}}</a>
                       % end
                                       
                       </html>"""
    @route('/')
    def index():


        options = []
        for i in range(len(env_info_store)):
            for j in range(i, len(env_info_store)):
                if i != j:
                    if i == 0:
                        hub = "(hub)"
                    else:
                        hub = ""
                    options.append((i, j, hub))

        return template(HOME_TEMPLATE, stored_envs=env_info_store[1:], options=options)


    ENV_TEMPLATE = """<html><title>""" + title + """</title><body>
                                <h1>""" + title + """</h1><hr>
 
                                <h1>Environment #{{env_number}} as of {{ts}}</h1>
 
                                 <ul>
                                % for collector in env.keys():
                                  <li> <a href=#{{collector}}>{{collector}}</a>
                                  </li>
                                % end
                                </ul>

                                <hr>

 
                                % for collector in env.keys():
                                    <a name={{collector}}></a>
                                    <h1>{{collector}}</h1>
                                    <p><b>{{env[collector]['english']}}</b></p>
                                    <p>{{!env[collector]['info']}}</p>
                                % end
                          </body></html>"""

    @route('/environment_info', method='POST')
    def environment_info_write():
        """Recieves Environment Info from another node."""

        global env_info_store

        json = import_json()

        urlparts = request.urlparts

        postdata = request.body.read()

        ts = datetime.now().isoformat()

        postdata = json.loads(postdata)
        postdata['environment'] = Environment.from_dict(postdata['environment'])

        env_info_store.append((postdata, ts))
        env_info_number = len(env_info_store) - 1

        out = {'timestamp': ts,
               'environment_number': env_info_number,
               'response_type': 'environment_info_write',
               'read_url': urlparts.scheme + "://" + urlparts.netloc + "/environment_info/" + str(env_info_number),
               'diff_url': urlparts.scheme + "://" + urlparts.netloc + "/environment_diff_view/0/" + str(env_info_number)}

        out = json.dumps(out)
        out = out.encode('utf-8')

        response.content_type = 'application/json'

        return out

    @route('/environment_info', method='GET')
    @route('/environment_info/<env_info_key>', method='GET')
    def environment_info_read(env_info_key=0):
        """Recieves Environment Info"""

        global env_info_store

        env_info_key = int(env_info_key)

        if env_info_key == 0:
            environment = Environment()
            ts = datetime.now().isoformat()
        else:
            postdata, ts = env_info_store[env_info_key]
            environment = postdata['environment']

        env_info = environment.for_web()

        response.content_type = 'text/html'

        return template(ENV_TEMPLATE, env=env_info, env_number=env_info_key, ts=ts)

    def parse_input_do_diff(env_1_info_key, env_2_info_key):

        def get_env(key):
            global env_info_store
            if key == 0:
                e = Environment()
                ts = datetime.now().isoformat()
            else:
                postdata, ts = env_info_store[key]
                e = postdata['environment']
            return e, ts

        e1, ts1 = get_env(env_1_info_key)
        e2, ts2 = get_env(env_2_info_key)

        return EnvironmentDiff(e1, e2), ts1, ts2


    @route('/environment_diff/<env_1_info_key>', method='GET')
    @route('/environment_diff/<env_1_info_key>/<env_2_info_key>', method='GET')
    def environment_diff(env_1_info_key, env_2_info_key=0):

        env_1_info_key = int(env_1_info_key)
        env_2_info_key = int(env_2_info_key)

        json = import_json()

        ed, ts1, ts2 = parse_input_do_diff(env_1_info_key, env_2_info_key)

        ed = ed.for_json()

        out = json.dumps(ed)
        out = out.encode('utf-8')

        response.content_type = 'application/json'

        return out

    DIFF_TEMPLATE = """<html><title>""" + title + """</title><body>
                                <h1>""" + title + """</h1>
                                """ + GHDIFF_MSG + """
                                <hr>
                                
                                
                                <h1>Environment #{{e1}} ({{ts1}}) vs #{{e2}} ({{ts2}})</h1>
                                
                                % if e1 == 0 or e2 == 0:
                                   Note: Environment #0 is the environment the PyEnvDiff hub is running from.
                                % end
                                
                                <ul>
                                % for collector in diff.keys():
                                  <li> <a href=#{{collector}}>{{collector}}</a>
                                  % if not diff[collector]['matching']:
                                     - Differences Detected!
                                  % end
                                  </li>
                                % end
                                </ul>

                                <hr>
                                
                                % for env_cls in diff.keys():
                                    <a name={{env_cls}}></a>
                                    <h1>{{env_cls}}</h1>
                                    <p><b>{{diff[env_cls]['english']}}</b></p>
                                    % if diff[env_cls]['matching']:
                                        <h2><font color="blue">Matching!</font></h2>
                                        {{!diff[env_cls]['left']}}
                                    % end
                                    
                                    % if not diff[env_cls]['matching']:
                                        <h2><font color="blue">Differences Detected!</font></h2>
                                        <h3>Comparison</h3>
                                        {{!diff[env_cls]['comparison']}}
                                        <h3>Left</h3>
                                        {{!diff[env_cls]['left']}}
                                        <h3>Right</h3>
                                        {{!diff[env_cls]['right']}}
                                    % end
                                % end
                          </body></html>"""

    @route('/environment_diff_view/<env_1_info_key>', method='GET')
    @route('/environment_diff_view/<env_1_info_key>/<env_2_info_key>', method='GET')
    def environment_diff_view(env_1_info_key, env_2_info_key=0):

        env_1_info_key = int(env_1_info_key)
        env_2_info_key = int(env_2_info_key)

        diff, ts1, ts2 = parse_input_do_diff(env_1_info_key, env_2_info_key)
        diff = diff.for_web()

        if DEVELOP_MODE:
            with open("diff.pickle", "wb+") as f:
                dump(diff, f, protocol=HIGHEST_PROTOCOL)

        response.content_type = 'text/html'

        return template(DIFF_TEMPLATE, diff=diff, e1=env_1_info_key, e2=env_2_info_key, ts1=ts1, ts2=ts2)

    if DEVELOP_MODE:
        @route('/sample_diff')
        def sample_diff():

            from pickle import load

            with open("diff.pickle", "rb+") as f:
                diff = load(f)

            response.content_type = 'text/html'


            print(diff['SysPath'])

            return template(DIFF_TEMPLATE, diff=diff)



    SERVER = '0.0.0.0'

    from sys import argv

    try:
        # If we get an integer, use it, else...
        PORT = str(int(argv[-1]))
    except:
        PORT = '8080'

    print("Starting up " + title + " running on:")
    print()
    print("   http://" + SERVER + ":" + PORT + "/")
    print()
    print("You can view environment information at")
    print()
    print("   http://" + SERVER + ":" + PORT + "/environment_info")
    print()
    print("If you run the following command from other environments:")
    print(">>>python -m pyenvdiff.post_to_hub http://" + SERVER + ":" + PORT)
    print("...")
    print("You will be able to view it, or compare it, at the following URLs:")
    print("   http://" + SERVER + ":" + PORT + "/environment_info/N where N is the number of environment, shown in the response after posting.")
    print("   http://" + SERVER + ":" + PORT + "/environment_diff_view/N/M where N & M are two different environment numbers.  Use 0 for the hub's environment.")

    run(host=SERVER, port=PORT, quiet=True)
