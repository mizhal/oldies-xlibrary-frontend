#######################
## @deps pila web
#######################
import web
from beaker.middleware import SessionMiddleware
from web.contrib.template import render_mako

urls = (
	'/pager', "Pager",
	'/book', "Book",
	'/all.html', "Library"
)

#######################
## @deps servicios del SO
#######################
import os
from popen2 import popen2

########################
##
########################
from xlibrary.facade import XLibrary

xlib = XLibrary()
lib = xlib.openLibrary()

class Pager:
	def GET(self):
		input = web.input(_unicode=False)
		page = input.page
		id=input.id
		box=input.box
		
		if int(page) < 1:
			page = 1
		
		book = lib.getBook(id)
		fname = book.fname
		
		web.header("content-type", "image/png")
		pout, pin = popen2('''pdftoppm -scale-to %s -f %s -l %s -gray "%s" | pnmtopng'''%(box,page, page, fname))
		return pout.read()
		
render = render_mako(
        directories=[os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

class Book:
	def GET(self):
		web.header("content-type", "text/html")
		input = web.input(_unicode=False)
		return render.book(id=input.id)
			
class Library:
	def GET(self):
		web.header("content-type", "text/html")
		return render.library(books=lib.listBooks())

application = SessionMiddleware(web.application(urls, globals()).wsgifunc())