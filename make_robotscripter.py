#!/usr/bin/env python

import sys

inroboscripter = open(sys.argv[1])
intemplate = open(sys.argv[2])
outroboscripter = open(sys.argv[3], 'w')

template_text = intemplate.read()

roboscripter = inroboscripter.read()

outroboscripter.write(roboscripter.replace("REPLACE_ME_1", template_text))

intemplate.close()
inroboscripter.close()
outroboscripter.close()

