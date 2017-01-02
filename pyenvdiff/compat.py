# -*- coding: utf-8 -*-


supported_info_types = []

try:
    supported_info_types.append(bool)
except:
    pass

try:
    supported_info_types.append(int)
except:
    pass

try:
    supported_info_types.append(str)
except:
    pass

try:
    supported_info_types.append(unicode)
except:
    pass

try:
    supported_info_types.append(list)
except:
    pass

try:
    supported_info_types.append(dict)
except:
    pass

supported_info_types = tuple(supported_info_types)