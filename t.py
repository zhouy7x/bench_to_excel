import json

data1 = {
    'platform': {
        'hardware': {
            'BB_number': 'BB37949',
            'cpu_model': 'N4100',
            'memory': '4g',
            'device_type': 'chromebook'
        },
        'software': {
            'OS': 'ChromeOS 122260.0.0',
            'firmware': 'Google_Bobba.11297.4.0',
            'browser': 'chrome 77.0.3818.0',
            'v8': '7.7.27',
            'optimization': 'baseline'
        }
    },
    'benchmark': {
        'name': 'Speedometer2.0',
        'score': {
            'overall': 44.86,
            'subcase': '{"VanillaJS-TodoMVC":224.18,"Vanilla-ES2015-TodoMVC":182.34,"Vanilla-ES2015-Babel-Webpack-TodoMVC":179.4,"React-TodoMVC":121.24,"React-Redux-TodoMVC":62.06,"EmberJS-TodoMVC":73.39,"EmberJS-Debug-TodoMVC":24.81,"BackboneJS-TodoMVC":264.86,"AngularJS-TodoMVC":64.3,"Angular2-TypeScript-TodoMVC":267.17,"VueJS-TodoMVC":482.64,"jQuery-TodoMVC":36.34,"Preact-TodoMVC":737.19,"Inferno-TodoMVC":118.83,"Elm-TodoMVC":89.31,"Flight-TodoMVC":190.65}'
        }
    },
    'info': {
        'tester': 'yangx.a.zhou@intel.com',
        'requester': 'shiyu.zhang@intel.com',
        'driver': {
            'name': 'Petra',
            'org': 'CCG'
        },
        'reason': 'weekly trunk1'
    }
}

data2 = {
    'platform': {
        'hardware': {
            'BB_number': 'BB37949',
            'cpu_model': 'N4100',
            'memory': '4g',
            'device_type': 'chromebook'
        },
        'software': {
            'OS': 'ChromeOS 122260.0.0',
            'firmware': 'Google_Bobba.11297.4.0',
            'browser': 'chrome 77.0.3818.0',
            'v8': '7.7.27',
            'optimization': 'baseline'
        }
    },
    'benchmark': {
        'name': 'Speedometer2.0',
        'score': {
            'overall': 44.86,
            'subcase': '{"VanillaJS-TodoMVC":224.18,"Vanilla-ES2015-TodoMVC":182.34,"Vanilla-ES2015-Babel-Webpack-TodoMVC":179.4,"React-TodoMVC":121.24,"React-Redux-TodoMVC":62.06,"EmberJS-TodoMVC":73.39,"EmberJS-Debug-TodoMVC":24.81,"BackboneJS-TodoMVC":264.86,"AngularJS-TodoMVC":64.3,"Angular2-TypeScript-TodoMVC":267.17,"VueJS-TodoMVC":482.64,"jQuery-TodoMVC":36.34,"Preact-TodoMVC":737.19,"Inferno-TodoMVC":118.83,"Elm-TodoMVC":89.31,"Flight-TodoMVC":190.65}'
        }
    },
    'info': {
        'tester': 'yangx.a.zhou@intel.com',
        'requester': 'shiyu.zhang@intel.com',
        'driver': {
            'name': 'Petra',
            'org': 'CCG'
        },
        'reason': 'weekly trunk2'
    }
}
data3 = {
    'platform': {
        'hardware': {
            'BB_number': 'BB37949',
            'cpu_model': 'N4100',
            'memory': '4g',
            'device_type': 'chromebook'
        },
        'software': {
            'OS': 'ChromeOS 122260.0.0',
            'firmware': 'Google_Bobba.11297.4.0',
            'browser': 'chrome 77.0.3818.0',
            'v8': '7.7.27',
            'optimization': 'baseline'
        }
    },
    'benchmark': {
        'name': 'Speedometer2.0',
        'score': {
            'overall': 44.86,
            'subcase': '{"VanillaJS-TodoMVC":224.18,"Vanilla-ES2015-TodoMVC":182.34,"Vanilla-ES2015-Babel-Webpack-TodoMVC":179.4,"React-TodoMVC":121.24,"React-Redux-TodoMVC":62.06,"EmberJS-TodoMVC":73.39,"EmberJS-Debug-TodoMVC":24.81,"BackboneJS-TodoMVC":264.86,"AngularJS-TodoMVC":64.3,"Angular2-TypeScript-TodoMVC":267.17,"VueJS-TodoMVC":482.64,"jQuery-TodoMVC":36.34,"Preact-TodoMVC":737.19,"Inferno-TodoMVC":118.83,"Elm-TodoMVC":89.31,"Flight-TodoMVC":190.65}'
        }
    },
    'info': {
        'tester': 'yangx.a.zhou@intel.com',
        'requester': 'shiyu.zhang@intel.com',
        'driver': {
            'name': 'Petra',
            'org': 'CCG'
        },
        'reason': 'weekly trunk3'
    }
}

data = [data1, data2, data3]
data_json = json.dumps(data)
# with open('data.json', 'w') as f:
#     f.write(data_json)

string = "mongodb://jstc_db_usr:jstcDB123@" +\
	"p1fm1mon125.amr.corp.intel.com:7919," +\
	"p2fm1mon125.amr.corp.intel.com:7919," +\
	"p3fm1mon125.amr.corp.intel.com:7919" +\
	"/JSTC_Performance_DB?ssl=true&replicaSet=mongo7919"

print(string)