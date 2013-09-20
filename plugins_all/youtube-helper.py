from message_plugin import MessagePlugin

from urllib2 import urlopen
from urlparse import urlparse, parse_qs
import datetime
import re
import xml.etree.ElementTree as ET


class YoutubeHelper(MessagePlugin):

    def message_received(self, msg, nick=""):
        if msg['type'] == 'groupchat':
            # Get urls in message
            urls = re.findall(r'(https?://[^\s]+)', msg['body'])

            new_msg = ""
            for url in urls:
                # Check if link is from Youtube
                if url.find("youtube.com") > -1:
                    # Find video ID from query parameters
                    qps = parse_qs(urlparse(url).query, keep_blank_values=True)
                    if 'v' in qps.keys():
                        # Get video details
                        fh = urlopen("http://gdata.youtube.com/feeds/api/videos/%s" % (qps['v'][0]))
                        xml_data = fh.read()
                        root = ET.fromstring(xml_data)
                        video_title = ""
                        video_duration = ""
                        for k in range(0, len(root) - 1):
                            if root[k].tag.endswith("title"):
                                video_title = root[k].text
                            if root[k].tag.endswith("group"):
                                for child in root[k].getchildren():
                                    if child.tag.endswith("duration"):
                                        video_duration = child.attrib['seconds']
                        new_msg += "Video: %s (%s)" % (video_title, str(datetime.timedelta(seconds=int(video_duration))))
                        fh.close()
            msg.reply(new_msg).send()
