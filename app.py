#!/usr/bin/env python

import urllib
import json
import os
from math import sqrt

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    # baseurl = "https://query.yahooapis.com/v1/public/yql?"
    data = makeYqlQuery(req)
    # if yql_query is None:
    #     return {}
    # yql_url = baseurl + urllib.urlencode({'q': yql_query}) + "&format=json"
    # print(yql_url)
    #
    # result = urllib.urlopen(yql_url).read()
    # print("yql result: ")
    # print(result)
    #
    # data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    d = parameters.get("unit-length").get("amount")
    v = parameters.get("unit-speed").get("amount")
    #a = parameters.get("unit-accel")
    # if city is None:
    #     return None
    #
    # return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"
    return sqrt(d/v)


def makeWebhookResult(data):
    # query = data.get('query')
    # if query is None:
    #     return {}
    #
    # result = query.get('results')
    # if result is None:
    #     return {}
    #
    # channel = result.get('channel')
    # if channel is None:
    #     return {}
    #
    # item = channel.get('item')
    # location = channel.get('location')
    # units = channel.get('units')
    # if (location is None) or (item is None) or (units is None):
    #     return {}
    #
    # condition = item.get('condition')
    # if condition is None:
    #     return {}
    #
    # # print(json.dumps(item, indent=4))

    speech = data

    print("Response:")
    print(speech)

    slack_message = {
        "text": speech,
        "attachments": [
            {
                "title": "title",
                "title_link": "title_link",
                "color": "#36a64f",

                "fields": [
                    {
                        "title": "Condition",
                        "value": "val",
                        "short": "false"
                    },
                    {
                        "title": "Wind",
                        "value": "val",
                        "short": "true"
                    },
                    {
                        "title": "Atmosphere",
                        "value": "val",
                        "short": "true"
                    }
                ],

                "thumb_url": "url"
            }
        ]
    }

    facebook_message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "title",
                        "image_url": "image",
                        "subtitle": speech,
                        "buttons": [
                            {
                                "type": "web_url",
                                "url": "url",
                                "title": "View Details"
                            }
                        ]
                    }
                ]
            }
        }
    }

    print(json.dumps(slack_message))

    return {
        "speech": speech,
        "displayText": speech,
        "data": {"slack": slack_message, "facebook": facebook_message},
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    #print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
