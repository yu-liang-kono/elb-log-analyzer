#!/usr/bin/env python

# standard library imports
from calendar import timegm
from datetime import datetime, timedelta

# third party related imports

# local library imports
from elb_log_analyzer.query.base_query import BaseQuery


class BaseTimeRangeQuery(BaseQuery):
    """Base class for time range query class.

    It is used for query documents: `begin_at` <= field < `end_at`.
    """

    def __init__(self, begin_at, end_at):
        """Constructor

        Args:
            begin_at: A datetime.date, datetime.datetime object.
            end_at: A datetime.date, datetime.datetime object.
        """

        super(BaseTimeRangeQuery, self).__init__()
        self.begin_at = begin_at
        self.end_at = end_at

    def get_index_name(self):

        # normalize to datetime object
        normalize = lambda d: datetime.utcfromtimestamp(timegm(d.timetuple()))
        d = normalize(normalize(self.begin_at).date())
        e = normalize(self.end_at)
        day = timedelta(days=1)
        span = []

        while d < e:
            span.append(d)
            d += day

        return ','.join(['logstash-' + s.strftime('%Y.%m.%d') for s in span])
