#!/usr/bin/env python

"""models.py

Udacity conference server-side Python App Engine data & ProtoRPC models

$Id: models.py,v 1.1 2014/05/24 22:01:10 wesc Exp $

created/forked from conferences.py by wesc on 2014 may 24
extended by Norbert Stueken on 2015 may 20 (v1.1)
updated by Norbert Stueken after feedback from Helmuth Breitenfellner on 2015
may 26 (v1.2)
"""

# built-in modules
import httplib
# third-party modules
import endpoints
from protorpc import messages
from google.appengine.ext import ndb

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


class ConflictException(endpoints.ServiceException):
    """ConflictException -- exception mapped to HTTP 409 response"""
    http_status = httplib.CONFLICT


class Profile(ndb.Model):
    """Profile -- User profile object"""
    displayName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    teeShirtSize = ndb.StringProperty(default='NOT_SPECIFIED')
    conferenceKeysToAttend = ndb.StringProperty(repeated=True)
    sessionsKeysOnWishlist = ndb.StringProperty(repeated=True)


class ProfileMiniForm(messages.Message):
    """ProfileMiniForm -- update Profile form message"""
    displayName = messages.StringField(1)
    teeShirtSize = messages.EnumField('TeeShirtSize', 2)


class ProfileForm(messages.Message):
    """ProfileForm -- Profile outbound form message"""
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    teeShirtSize = messages.EnumField('TeeShirtSize', 3)
    conferenceKeysToAttend = messages.StringField(4, repeated=True)
    sessionsKeysOnWishlist = messages.StringField(5, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    data = messages.StringField(1, required=True)


class BooleanMessage(messages.Message):
    """BooleanMessage-- outbound Boolean value message"""
    data = messages.BooleanField(1)


class Conference(ndb.Model):
    """Conference -- Conference object"""
    name            = ndb.StringProperty(required=True)
    description     = ndb.StringProperty()
    organizerUserId = ndb.StringProperty()
    topics          = ndb.StringProperty(repeated=True)
    city            = ndb.StringProperty()
    startDate       = ndb.DateProperty()
    month           = ndb.IntegerProperty()
    maxAttendees    = ndb.IntegerProperty()
    seatsAvailable  = ndb.IntegerProperty()
    endDate         = ndb.DateProperty()


class ConferenceForm(messages.Message):
    """ConferenceForm -- Conference outbound form message"""
    name            = messages.StringField(1)
    description     = messages.StringField(2)
    organizerUserId = messages.StringField(3)
    topics          = messages.StringField(4, repeated=True)
    city            = messages.StringField(5)
    startDate       = messages.StringField(6)
    month           = messages.IntegerField(7)
    maxAttendees    = messages.IntegerField(8)
    seatsAvailable  = messages.IntegerField(9)
    endDate         = messages.StringField(10)
    websafeKey      = messages.StringField(11)
    organizerDisplayName = messages.StringField(12)


class ConferenceForms(messages.Message):
    """ConferenceForms -- multiple Conference outbound form message"""
    items = messages.MessageField(ConferenceForm, 1, repeated=True)


class Speaker(ndb.Model):
    """Speaker -- A Speaker can speak at multiple conferences."""
    name = ndb.StringProperty(required=True)


class SpeakerForm(messages.Message):
    """SpeakerForm -- Speaker form messages"""
    name = messages.StringField(1, required=True)


class Session(ndb.Model):
    """Session -- Session as part of a Conference."""
    name            = ndb.StringProperty(required=True)
    highlights      = ndb.StringProperty(repeated=True)
    # A session can have multiple speaker entities/kinds.
    speakers        = ndb.KeyProperty(kind=Speaker, repeated=True)
    duration        = ndb.TimeProperty()
    # Add typeOFSession as an enum property with by using the msgprop module.
    # To perform queries on this field, indexed must be set to True.
    # typeOfSession   = msgprop.EnumProperty(TypeOfSession, indexed=True)
    typeOfSession   = ndb.StringProperty()
    date            = ndb.DateProperty()
    startTime       = ndb.TimeProperty()
    location        = ndb.StringProperty()


class SessionForm(messages.Message):
    """SessionForm -- Session form messages"""
    name                    = messages.StringField(1)
    highlights              = messages.StringField(2, repeated=True)
    speakers                = messages.StringField(3, repeated=True)
    duration                = messages.StringField(4)
    typeOfSession           = messages.EnumField('TypeOfSession', 5)
    date                    = messages.StringField(6)
    startTime               = messages.StringField(7)
    location                = messages.StringField(8)
    # The websafeKey contains the info of the entity and the parent and can
    # be used to fully reconstitute the full id
    websafeKey    = messages.StringField(9)
    websafeConfKey = messages.StringField(10)


class SessionForms(messages.Message):
    """SessionForms -- multiple Session form messages"""
    items = messages.MessageField(SessionForm, 1, repeated=True)


class TeeShirtSize(messages.Enum):
    """TeeShirtSize -- t-shirt size enumeration value"""
    NOT_SPECIFIED = 1
    XS_M = 2
    XS_W = 3
    S_M = 4
    S_W = 5
    M_M = 6
    M_W = 7
    L_M = 8
    L_W = 9
    XL_M = 10
    XL_W = 11
    XXL_M = 12
    XXL_W = 13
    XXXL_M = 14
    XXXL_W = 15


class TypeOfSession(messages.Enum):
    """ TypeOfSession -- session type enumeration value."""
    NOT_SPECIFIED = 1
    Workshop = 2
    Lecture = 3
    Keynote = 4
    Information = 5
    Networking = 6


class ConferenceQueryForm(messages.Message):
    """ConferenceQueryForm -- Conference query inbound form message"""
    field = messages.StringField(1)
    operator = messages.StringField(2)
    value = messages.StringField(3)


class ConferenceQueryForms(messages.Message):
    """ConferenceQueryForms -- multiple ConferenceQueryForm inbound form message"""
    filters = messages.MessageField(ConferenceQueryForm, 1, repeated=True)
