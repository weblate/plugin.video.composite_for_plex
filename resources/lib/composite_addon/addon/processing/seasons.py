# -*- coding: utf-8 -*-
"""

    Copyright (C) 2011-2018 PleXBMC (plugin.video.plexbmc) by hippojay (Dave Hawes-Johnson)
    Copyright (C) 2018-2019 Composite (plugin.video.composite_for_plex)

    This file is part of Composite (plugin.video.composite_for_plex)

    SPDX-License-Identifier: GPL-2.0-or-later
    See LICENSES/GPL-2.0-or-later.txt for more information.
"""

import xbmcplugin  # pylint: disable=import-error

from .episodes import process_episodes
from ...addon.common import CONFIG
from ...addon.common import SETTINGS
from ...addon.common import PrintDebug
from ...addon.common import get_handle
from ...addon.items.season import create_season_item
from ...addon.utils import get_xml
from ...plex import plex

LOG = PrintDebug(CONFIG['name'])


def process_seasons(url, rating_key=None, plex_network=None):
    if plex_network is None:
        plex_network = plex.Plex(load=True)

    xbmcplugin.setContent(get_handle(), 'seasons')

    if not url.startswith(('http', 'file')) and rating_key:
        # Get URL, XML and parse
        server = plex_network.get_server_from_uuid(url)
        url = server.get_url_location() + '/library/metadata/%s/children' % str(rating_key)
    else:
        server = plex_network.get_server_from_url(url)

    tree = get_xml(url)
    if tree is None:
        return

    will_flatten = False
    if SETTINGS.get_setting('flatten') == '1':
        # check for a single season
        if int(tree.get('size', 0)) == 1:
            LOG.debug('Flattening single season show')
            will_flatten = True

    items = []
    # For all the directory tags
    season_tags = tree.findall('Directory')
    for season in season_tags:

        if will_flatten:
            url = server.get_url_location() + season.get('key')
            process_episodes(url)
            return

        if SETTINGS.get_setting('disable_all_season') and season.get('index') is None:
            continue

        items.append(create_season_item(server, tree, season))

    if items:
        xbmcplugin.addDirectoryItems(get_handle(), items, len(items))

    xbmcplugin.endOfDirectory(get_handle(), cacheToDisc=SETTINGS.get_setting('kodicache'))