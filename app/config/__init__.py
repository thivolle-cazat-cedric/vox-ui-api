# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)


def config_loader(config, environment):
    """
    Charge la configuration de l'application.

    :param flask.Config config: généralement app.config
    :param str environement: le nom de l'environement (prod, dev, test, ...)

    :return: None

    L'ordre de chargement est le suivant :

      * la configuration par defaut (app.config.default)
      * la configuration en fonction de l'environment (prod, dev, test, ...) dans le app.config.env
      * la configuration de l'utilisateur depuis le fichier definit dans la
        variable d'environement VOX_PEER_CONFIG.

    Il permet de surcharger la configuration.
    """

    config.from_object('app.config.default')
    config.from_object('app.config.env.%s' % (environment))
    config.from_envvar('VOX_PEERS_CONFIG', silent=True)
