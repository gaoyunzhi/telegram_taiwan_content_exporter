#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram.ext import Updater
import export_to_telegraph
import link_extractor
import yaml

source = ['https://whogovernstw.org', 'https://www.thinkingtaiwan.com']

with open('existing') as f:
	existing = set([x.strip() for x in f.readlines()])
with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

export_to_telegraph.token = credential['telegraph_token']

tele = Updater(credential['bot_token'], use_context=True)
debug_group = tele.bot.get_chat(-1001198682178)
taiwan_channel = tele.bot.get_chat(-1001250188871)

def add(link):
	existing.add(link)
	with open('existing', 'a') as f:
		f.write('\n' + link)

def export():
	for s in source:
		for link, _ in link_extractor.getLinks(s):
			if link in existing:
				continue
			r = export_to_telegraph.export(link, force=True, 
				toSimplified=True, throw_exception=True)
			taiwan_channel.send_message(r)
			add(link)

if __name__=='__main__':
	export()