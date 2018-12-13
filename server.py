import web
import os
from web import form

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/images/(.*)', 'images', #this is where the image folder is located....
    'results',
)

query_form = form.Form(
    form.Textbox('query',description='query'),
)

class index:

    def GET(self):
        form = query_form()
        return render.index(form)
    def POST(self):
        form = query_form()
        user_data = web.input()
        return render.index(form)

class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"            }

        if name in os.listdir('images'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('images/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
