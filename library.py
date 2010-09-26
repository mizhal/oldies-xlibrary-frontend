#######################
## @deps pila web
#######################
import web
from beaker.middleware import SessionMiddleware
from web.contrib.template import render_mako

urls = (
	'/pager', "Pager",
	'/book', "Book",
	'/all.html', "Library",
	'/([0-9]+)/([0-9]+)/note', "Note",
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
		id = input.id
		box  = input.box
		
		if int(page) < 1:
			page = 1
		
		book = lib.getBook(id)
		fname = book.fname
		
		web.header("content-type", "image/png")
		
		pout, pin = popen2('''convert -negate -density 200 -resize %sx "%s"[%s] png:- '''%(box, fname, str(int(page) - 1)))
		
		#if input.has_key("cache"):
			#pout, pin = popen2('''nice -n 19 pdftoppm -cropbox -f %s -l %s -gray -png "%s" '''%(page, page, fname))
		#else:
			#pout, pin = popen2('''pdftoppm -cropbox -f %s -l %s -gray -png "%s" '''%(page, page, fname))
			
		image = pout.read()
		return image
		
render = render_mako(
	directories=[os.path.join(os.path.dirname(__file__), 'templates').replace('\\','/'),],
	input_encoding='utf-8',
	output_encoding='utf-8',
	)

class Book:
	def GET(self):
		web.header("content-type", "text/html")
		input = web.input(_unicode=False)
		book = lib.getBook(input.id)
		return render.book(id=input.id, title = book.title)
			
class Library:
	def GET(self):
		web.header("content-type", "text/html")
		return render.library(books=lib.listBooks())


class Note:
	def POST(self, book, page):
		received = web.input(_unicode=False)
		
		return "%s/%s/(%s,%s)"%(book, page, received.top, received.left)
		
	def GET(self, book, page):
		return book, page

application = SessionMiddleware(web.application(urls, globals()).wsgifunc())