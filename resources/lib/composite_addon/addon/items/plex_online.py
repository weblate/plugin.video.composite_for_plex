# -*- coding: utf-8 -*-
"""

    Copyright (C) 2011-2018 PleXBMC (plugin.video.plexbmc) by hippojay (Dave Hawes-Johnson)
    Copyright (C) 2018-2020 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

from ..constants import MODES
from ..strings import encode_utf8
from ..strings import i18n
from .common import create_gui_item
from .common import get_link_url
from .common import get_thumb_image


def create_plex_online_item(context, item):
    details = {
        'title': encode_utf8(item.data.get('title', item.data.get('name', i18n('Unknown'))))
    }
    extra_data = {
        'type': 'Video',
        'installed': int(item.data.get('installed', 2)),
        'key': item.data.get('key', ''),
        'thumb': get_thumb_image(context, item.server, item.data),
        'mode': MODES.CHANNELINSTALL
    }

    if extra_data['installed'] == 1:
        details['title'] = details['title'] + ' (%s)' % encode_utf8(i18n('installed'))

    elif extra_data['installed'] == 2:
        extra_data['mode'] = MODES.PLEXONLINE

    item_url = get_link_url(item.server, item.url, item.data)

    extra_data['parameters'] = {
        'name': details['title']
    }

    return create_gui_item(context, item_url, details, extra_data)
