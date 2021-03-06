#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24
extended by Norbert Stueken on 2015 may 20 (v1.1)
updated by Norbert Stueken after feedback from Helmuth Breitenfellner on 2015
may 26 (v1.2)

"""

# built-in modules
import webapp2
# third-party modules
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import memcache
# own modules
from conference import ConferenceApi
from models import Session
from models import Speaker

# authorship information
__authors__ = "Wesley Chun, Norbert Stueken"
__copyright__ = "Copyright 2015"
__credits__ = ["Wesley Chun, Norbert Stueken, Helmuth Breitenfellner at \
Udacity"]
__license__ = "GPL"
__version__ = "1.2"
__maintainer__ = "Norbert Stueken"
__email__ = "wesc+api@google.com (Wesley Chun), norbert.stueken@gmail.com \
(Norbert Stueken)"
__status__ = "Development"


class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        # use _cacheAnnouncement() to set announcement in Memcache
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )


class CheckSpeakers(webapp2.RequestHandler):
    def post(self):
        """Check if there are more conference sessions by the Speakers."""
        # convert the urlsafe key string to the conference key
        c_key = ndb.Key(urlsafe=self.request.get('c_key_str'))
        # get all sessions of the conference
        confSessions = Session.query(ancestor=c_key)
        # get all speakers
        speakers = Speaker.query()
        # sort all speakers by name
        speakers = speakers.order(Speaker.name)
        # create empty list of featured speakers
        feat_spk_keys = []
        # check for every speaker
        for spk in speakers:
            count = 0
            # in how many sessions he speaks at the conference
            for session in confSessions:
                for cs_spk_key in session.speakers:
                    if spk.key == cs_spk_key:
                        count += 1
                        # if he is in more than one session, feature him
                        if count == 2:
                            # attach the speaker key to the list of
                            # featured speakers
                            feat_spk_keys.append(cs_spk_key)
        # set memcache key to the urlsafe key of the conference. Adding prefix
        # "FEATURED:", so new functionality to be put into memcache won't
        # collide with existing key.
        MEMCACHE_CONFERENCE_KEY = "FEATURED:%s" % c_key.urlsafe()
        # If there are featured speakers at the conference,
        # format featured speakers announcement and set it in memcache
        if feat_spk_keys:
            count = 0
            featured = "FEATURED SPEAKERS & SESSIONS ON THIS CONFERENCE -- "
            for spk_key in feat_spk_keys:
                count += 1
                featured += " FEATURED %s: %s SESSIONS: " % (
                    count, spk_key.get().name)
                sessionsOfFeatured = confSessions.filter(
                    Session.speakers == spk_key)
                featured += ", ".join(sess.name for sess in sessionsOfFeatured)
            memcache.set(MEMCACHE_CONFERENCE_KEY, featured)
        else:
            # If there are no featured speakers at the conference,
            # delete the memcache announcements entry
            featured = ""
            memcache.delete(MEMCACHE_CONFERENCE_KEY)

app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/check_speakers', CheckSpeakers)
], debug=True)
