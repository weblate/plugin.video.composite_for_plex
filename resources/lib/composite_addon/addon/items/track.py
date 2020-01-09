# -*- coding: utf-8 -*-
"""

    Copyright (C) 2011-2018 PleXBMC (plugin.video.plexbmc) by hippojay (Dave Hawes-Johnson)
    Copyright (C) 2018-2020 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

import json

from ..constants import MODES
from ..logger import Logger
from ..strings import encode_utf8
from ..strings import i18n
from .common import create_gui_item
from .common import get_fanart_image
from .common import get_thumb_image
from .context_menu import ContextMenu

LOG = Logger()


def create_track_item(context, item, listing=True):
    part_details = ()

    for child in item.data:
        for babies in child:
            if babies.tag == 'Part':
                part_details = (dict(babies.items()))

    LOG.debug('Part: %s' % json.dumps(part_details, indent=4))

    details = {
        'TrackNumber': int(item.data.get('index', 0)),
        'discnumber': int(item.data.get('parentIndex', 0)),
        'title': str(item.data.get('index', 0)).zfill(2) + '. ' +
                 (item.data.get('title', i18n('Unknown'))),
        'rating': float(item.data.get('rating', 0)),
        'album': encode_utf8(item.data.get('parentTitle', item.tree.get('parentTitle', ''))),
        'artist': encode_utf8(item.data.get('grandparentTitle',
                                            item.tree.get('grandparentTitle', ''))),
        'duration': int(item.data.get('duration', 0)) / 1000,
        'mediatype': 'song'
    }

    section_art = get_fanart_image(context, item.server, item.tree)
    if item.data.get('thumb'):
        section_thumb = get_thumb_image(context, item.server, item.data)
    else:
        section_thumb = get_thumb_image(context, item.server, item.tree)

    extra_data = {
        'type': 'music',
        'fanart_image': section_art,
        'thumb': section_thumb,
        'key': item.data.get('key', ''),
        'ratingKey': str(item.data.get('ratingKey', 0)),
        'mode': MODES.PLAYLIBRARY
    }

    if item.tree.get('playlistType'):
        playlist_key = str(item.tree.get('ratingKey', 0))
        if item.data.get('playlistItemID') and playlist_key:
            extra_data.update({
                'playlist_item_id': item.data.get('playlistItemID'),
                'playlist_title': item.tree.get('title'),
                'playlist_url': '/playlists/%s/items' % playlist_key
            })

    if item.tree.tag == 'MediaContainer':
        extra_data.update({
            'library_section_uuid': item.tree.get('librarySectionUUID')
        })

    # If we are streaming, then get the virtual location
    url = '%s%s' % (item.server.get_url_location(), extra_data['key'])

    # Build any specific context menu entries
    context_menu = None
    if not context.settings.get_setting('skipcontextmenus'):
        context_menu = ContextMenu(context, item.server, url, extra_data).menu

    if listing:
        return create_gui_item(context, url, details, extra_data, context_menu, folder=False)

    return url, details
