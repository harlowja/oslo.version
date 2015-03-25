# -*- coding: utf-8 -*-

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import inspect
import logging

import six

from oslo_version._i18n import _
from oslo_version import releases


# Get the sorted order so we can just use it...
_ORDERED_RELEASES = sorted(releases.Releases)

LOG = logging.getLogger(__name__)


class deprecated(object):
    """A decorator to mark callables as deprecated.

    This decorator **logs** a deprecation message when the callable it
    decorates is used. The message will include the release where the callable
    was deprecated, the release where it may be removed and possibly an
    optional replacement.

    Examples:

    1. Specifying the required deprecated release

    >>> @deprecated(as_of=releases.ICEHOUSE)
    ... def a(): pass

    2. Specifying a replacement:

    >>> @deprecated(as_of=releases.ICEHOUSE, in_favor_of='f()')
    ... def b(): pass

    3. Specifying the release where the functionality may be removed:

    >>> @deprecated(as_of=releases.ICEHOUSE, remove_in=+1)
    ... def c(): pass

    4. Specifying the deprecated functionality will not be removed:
    >>> @deprecated(as_of=releases.ICEHOUSE, remove_in=0)
    ... def d(): pass

    5. Specifying a replacement, deprecated functionality will not be removed:
    >>> @deprecated(as_of=releases.ICEHOUSE, in_favor_of='f()', remove_in=0)
    ... def e(): pass

    """

    _deprecated_msg_with_alternative = _(
        '%(what)s is deprecated as of %(as_of)s in favor of '
        '%(in_favor_of)s and may be removed in %(remove_in)s.')

    _deprecated_msg_no_alternative = _(
        '%(what)s is deprecated as of %(as_of)s and may be '
        'removed in %(remove_in)s. It will not be superseded.')

    _deprecated_msg_with_alternative_no_removal = _(
        '%(what)s is deprecated as of %(as_of)s in favor of %(in_favor_of)s.')

    _deprecated_msg_with_no_alternative_no_removal = _(
        '%(what)s is deprecated as of %(as_of)s. It will not be superseded.')

    def __init__(self, as_of,
                 in_favor_of=None, remove_in=2, what=None, log=None):
        """Initialize decorator

        :param as_of: the release deprecating the callable. Constants
            are define in this class for convenience.
        :param in_favor_of: the replacement for the callable (optional)
        :param remove_in: an integer specifying how many releases to wait
            before removing (default: 2)
        :param what: name of the thing being deprecated (default: the
            callable's name)
        :param log: logger to use when reporting about the deprecated
            feature (default: this modules logger)
        """
        self.as_of = as_of
        self.in_favor_of = in_favor_of
        self.remove_in = remove_in
        self.what = what
        if log is None:
            self.log = LOG
        else:
            self.log = log

    def __call__(self, func_or_cls):
        if not self.what:
            self.what = func_or_cls.__name__ + '()'
        msg, details = self._build_message()

        if inspect.isfunction(func_or_cls):

            @six.wraps(func_or_cls)
            def wrapped(*args, **kwargs):
                _report_deprecated_feature(self.log, msg, details)
                return func_or_cls(*args, **kwargs)

            return wrapped
        elif inspect.isclass(func_or_cls):
            orig_init = func_or_cls.__init__

            @six.wraps(orig_init, assigned=('__name__', '__doc__'))
            def new_init(self, *args, **kwargs):
                _report_deprecated_feature(self.log, msg, details)
                orig_init(self, *args, **kwargs)

            func_or_cls.__init__ = new_init
            return func_or_cls
        else:
            raise TypeError('deprecated can be used only with functions or '
                            'classes')

    @staticmethod
    def _translate_release(release):
        if not isinstance(release, releases.Releases):
            release_enum = releases.Releases.match(release)
            if release_enum is None:
                raise ValueError("No known release '%s'" % (release))
            return release_enum
        return release

    def _get_safe_to_remove_release(self, release):
        # TODO(dstanek): this method will have to be reimplemented once
        #    when we get to the X release because once we get to the Y
        #    release, what is Y+2?
        release = self._translate_release(release)
        release_idx = _ORDERED_RELEASES.index(release)
        new_release_idx = release_idx + self.remove_in
        try:
            return _ORDERED_RELEASES[new_release_idx]
        except IndexError:
            raise ValueError("No known release that is %s + %d"
                             % (release.name, self.remove_in))

    def _build_message(self):
        as_of = self._translate_release(self.as_of)
        remove_in = self._get_safe_to_remove_release(self.as_of)
        details = dict(what=self.what,
                       as_of=as_of.name,
                       remove_in=remove_in.name)
        if self.in_favor_of:
            details['in_favor_of'] = self.in_favor_of
            if self.remove_in > 0:
                msg = self._deprecated_msg_with_alternative
            else:
                # There are no plans to remove this function, but it is
                # now deprecated.
                msg = self._deprecated_msg_with_alternative_no_removal
        else:
            if self.remove_in > 0:
                msg = self._deprecated_msg_no_alternative
            else:
                # There are no plans to remove this function, but it is
                # now deprecated.
                msg = self._deprecated_msg_with_no_alternative_no_removal
        return msg, details


def _report_deprecated_feature(logger, msg, details):
    # TODO...
    print(msg % details)
