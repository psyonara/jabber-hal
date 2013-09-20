from message_plugin import MessagePlugin

from urllib2 import urlopen, HTTPError
from urlparse import urlparse, parse_qs
import datetime
import re
import xml.etree.ElementTree as ET


class YoutubeHelper(MessagePlugin):

    def get_video_id(self, url):
        if url.find("youtube.com") > -1:
            qps = parse_qs(urlparse(url).query, keep_blank_values=True)
            if 'v' in qps.keys():
                return qps['v'][0]
            else:
                return None
        elif url.find("youtu.be") > -1:
            path_elements = filter(None, urlparse(url).path.split("/"))
            if len(path_elements) > 0:
                return path_elements[0]
            else:
                return None
        else:
            return None

    def get_video_info(self, video_id):
        try:
            fh = urlopen("http://gdata.youtube.com/feeds/api/videos/%s" % (video_id))
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
            fh.close()
            return video_title, video_duration
        except HTTPError:
            return None, None

    def message_received(self, msg, nick=""):
        if msg['type'] == 'groupchat':
            urls = re.findall(r'(https?://[^\s]+)', msg['body'])

            for url in urls:
                video_id = self.get_video_id(url)
                if video_id:
                    title, duration = self.get_video_info(video_id)
                    if title:
                        new_msg = "Video: %s (%s)" % (title, str(datetime.timedelta(seconds=int(duration))))
                        msg.reply(new_msg).send()
