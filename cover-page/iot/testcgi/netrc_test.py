#!/usr/bin/env python
# -*- coding: utf-8 -*-
import netrc


"""
Set a path for your netrc file or ~/.netrc to default path
"""
HOST = 'academic-ni.cloud.thingworx.com'

secrets = netrc.netrc()
print(secrets.authenticators(HOST))
"""
Get login, account and password of netrc file
"""
#print(get)
