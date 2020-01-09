# -*- coding: utf-8 -*-
"""

    Copyright (C) 2011-2018 PleXBMC (plugin.video.plexbmc) by hippojay (Dave Hawes-Johnson)
    Copyright (C) 2018-2020 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

from kodi_six import xbmcplugin  # pylint: disable=import-error

from ..common import get_handle
from ..context import Item
from ..items.directory import create_directory_item
from ..items.movie import create_movie_item
from ..items.photo import create_photo_item
from ..items.track import create_track_item
from ..utils import get_xml


def process_photos(context, url, tree=None):
    server = context.plex_network.get_server_from_url(url)

    tree = get_xml(context, url, tree)
    if tree is None:
        return

    content_type = 'images'
    items = []
    for photo in tree:
        item = Item(server, url, tree, photo)
        if photo.tag.lower() == 'photo':
            items.append(create_photo_item(context, item))
        elif photo.tag.lower() == 'directory':
            items.append(create_directory_item(context, item))
        elif photo.tag.lower() == 'track':  # mixed content photo playlist
            content_type = 'movies'  # use movies for mixed content playlists
            items.append(create_track_item(context, item))
        elif photo.tag.lower() == 'video':  # mixed content photo playlist
            content_type = 'movies'  # use movies for mixed content playlists
            items.append(create_movie_item(context, item))

    xbmcplugin.setContent(get_handle(), content_type)

    if items:
        xbmcplugin.addDirectoryItems(get_handle(), items, len(items))

    xbmcplugin.endOfDirectory(get_handle(), cacheToDisc=context.settings.get_setting('kodicache'))
