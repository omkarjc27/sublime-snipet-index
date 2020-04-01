import urllib.request,urllib.parse
import re
import sublime_plugin,sublime
import json


class SnippetindexCommand(sublime_plugin.TextCommand):

	def on_done(self, index):

		if index == -1:
			return

		hsh = self.search_result[int(index)][1]
		
		response = urllib.request.urlopen('https://snip-index.herokuapp.com/fetch/{}/{}'.format('py',hsh))
		html = response.read()
		code = str(json.loads(html.decode("utf-8"))[0])
		self.view.run_command('replacetext', {'text': code})

	def run(self, edit):
		self.edit = edit
		text = []
		print(self.view.settings().get("syntax"))
		for region in self.view.sel():

			if region.empty():
				word = self.view.word(region)
				if not word.empty():
					word = self.view.substr(word).strip()
					if re.search(r'\w+', word) != None:
						text.append(word)
			else:
				text.append(self.view.substr(region).strip())

		if len(text):

			keywords = ' '.join(['20']+text)
			params = urllib.parse.quote(keywords)
			
			response = urllib.request.urlopen('https://snip-index.herokuapp.com/search/{}/{}'.format('py',params))
			html = response.read()
			self.search_result = json.loads(html.decode("utf-8"))

			self.list = []
			for i in range(len(self.search_result)):
				self.list.append(str(self.search_result[i][2])+"|"+str(self.search_result[i][3]))
			

			self.view.window().show_quick_panel(self.list, self.on_done,1, 0)


class ReplacetextCommand(sublime_plugin.TextCommand):
	def run(self, edit, text):
		print(text)
		self.view.insert(edit, self.view.sel()[0].begin(),text)
		self.view.sel().clear()
