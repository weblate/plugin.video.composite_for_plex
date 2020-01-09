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
from .common import create_gui_item
from .common import get_fanart_image
from .common import get_thumb_image


def create_artist_item(context, item):
    details = {
        'artist': encode_utf8(item.data.get('title', ''))
    }

    details['title'] = details['artist']

    extra_data = {
        'type': 'Music',
        'thumb': get_thumb_image(context, item.server, item.data),
        'fanart_image': get_fanart_image(context, item.server, item.data),
        'ratingKey': item.data.get('title', ''),
        'key': item.data.get('key', ''),
        'mode': MODES.ALBUMS,
        'plot': item.data.get('summary', ''),
        'mediatype': 'artist'
    }

    url = '%s%s' % (item.server.get_url_location(), extra_data['key'])

    return create_gui_item(context, url, details, extra_data)
