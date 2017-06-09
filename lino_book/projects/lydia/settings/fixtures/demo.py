# -*- coding: UTF-8 -*-
# Copyright 2015-2017 Luc Saffre
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from __future__ import print_function

import datetime

from django.conf import settings
from lino.api import rt, dd, _
from lino.utils import Cycler, i2d

from lino.core.roles import SiteAdmin
from lino_xl.lib.cal.choicelists import DurationUnits
#from lino_xl.lib.clocking.roles import Worker
from lino.utils.quantities import Duration
from lino.utils.mldbc import babel_named as named
from lino_xl.lib.online.auth.models import create_user

#from lino_xl.lib.clocking.choicelists import ReportingTypes


def objects():
    User = rt.models.auth.User
    Company = rt.models.contacts.Company

    cons = rt.models.auth.UserTypes.items_dict['100']
    sec = rt.models.auth.UserTypes.items_dict['200']
    yield create_user("marc", cons)
    yield create_user("mathieu", cons)
    yield create_user("luc", sec)

    USERS = Cycler(User.objects.all())
    WORKERS = Cycler(User.objects.filter(
        username__in='mathieu marc'.split()))
    END_USERS = Cycler(User.objects.filter(user_type=''))

    #yield clockings_objects()
    yield faculties_objects()
    # yield votes_objects()

    obj = Company(
        name="Tough Thorough Thought Therapies",
        country_id="BE", vat_id="BE12 3456 7890")
    yield obj
    settings.SITE.site_config.update(site_company=obj)

    # acct = rt.models.sepa.Account(
    #     partner=obj, iban="BE83540256917919", bic="BBRUBEBB")
    # yield acct

    # jnl = rt.models.ledger.Journal.get_by_ref('PMO')
    


def clockings_objects():
    # was previously in clockings
    Company = rt.models.contacts.Company
    # Vote = rt.models.votes.Vote
    SessionType = rt.models.clocking.SessionType
    Session = rt.models.clocking.Session
    Ticket = rt.models.contacts.Person
    User = rt.models.auth.User
    UserTypes = rt.models.auth.UserTypes
    # devs = (UserTypes.developer, UserTypes.senior)
    devs = [p for p in UserTypes.items()
            if p.has_required_roles([Worker])
            and not p.has_required_roles([SiteAdmin])]
    workers = User.objects.filter(user_type__in=devs)
    WORKERS = Cycler(workers)
    TYPES = Cycler(SessionType.objects.all())
    # TICKETS = Cycler(Ticket.objects.all())
    DURATIONS = Cycler([12, 138, 90, 10, 122, 209, 37, 62, 179, 233, 5])

    # every fourth ticket is unassigned and thus listed in
    # PublicTickets
    # for i, t in enumerate(Ticket.objects.exclude(private=True)):
    for i, t in enumerate(Ticket.objects.all()):
        if i % 4:
            t.assigned_to = WORKERS.pop()
            yield t

    for u in workers:

        # VOTES = Cycler(Vote.objects.filter(user=u))
        # TICKETS = Cycler(Ticket.objects.filter(assigned_to=u))
        TICKETS = Cycler(Ticket.objects.filter())
        # if len(VOTES) == 0:
        #     continue

        for offset in (0, -1, -3, -4):

            date = dd.demo_date(offset)
            worked = Duration()
            ts = datetime.datetime.combine(date, datetime.time(9, 0, 0))
            for i in range(7):
                obj = Session(
                    ticket=TICKETS.pop(),
                    session_type=TYPES.pop(), user=u)
                obj.set_datetime('start', ts)
                d = DURATIONS.pop()
                worked += d
                if offset < 0:
                    ts = DurationUnits.minutes.add_duration(ts, d)
                    obj.set_datetime('end', ts)
                yield obj
                if offset == 0 or worked > 8:
                    break

def faculties_objects():
    "was previously in faculties.fixtures.demo2"

    Faculty = rt.models.faculties.Faculty
    Competence = rt.models.faculties.Competence
    Demand = rt.models.faculties.Demand
    # Ticket = rt.models.tickets.Ticket
    User = rt.models.auth.User

    yield named(Faculty, _('Analysis'))
    yield named(Faculty, _('Code changes'))
    yield named(Faculty, _('Documentation'))
    yield named(Faculty, _('Testing'))
    yield named(Faculty, _('Configuration'))
    yield named(Faculty, _('Enhancement'))
    yield named(Faculty, _('Optimization'))
    yield named(Faculty, _('Offer'))

    SKILLS = Cycler(Faculty.objects.all())
    END_USERS = Cycler(dd.plugins.faculties.end_user_model.objects.all())

    i = 0
    for j in range(2):
        for u in User.objects.all():
            i += 1
            yield Competence(user=u, faculty=SKILLS.pop())
            if i % 2:
                yield Competence(user=u, faculty=SKILLS.pop())
            if i % 3:
                yield Competence(
                    user=u, faculty=SKILLS.pop(),
                    end_user=END_USERS.pop())
            
    for i, t in enumerate(
            dd.plugins.faculties.demander_model.objects.all()):
        yield Demand(demander=t, skill=SKILLS.pop())
        if i % 3:
            yield Demand(demander=t, skill=SKILLS.pop())