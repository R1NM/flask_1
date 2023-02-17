from flask import Flask, request, redirect

app = Flask(__name__)

#pages
nxtId=4
topics = [
    {'id':1, 'title': 'html', 'body': 'html is...'},
    {'id':2, 'title': 'css', 'body': 'css is...'},
    {'id':3, 'title': 'javascript', 'body': 'javascript is...'},
]

#get contents
def getContents():
    liTags=''
    for topic in topics:
        liTags+=f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'
    #
    return liTags


#template
def template(contents,title,body,id=None):
    contextUI=''
    if id !=None:
        contextUI=f'''
            <li><a href="/update/{id}">update</a></li>
            <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"></form></li>
        '''

    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            <h2>{title}</h2>
            {body}
            <ul>           
                <li><a href="/create">create</a></li>
                {contextUI}
            <ul>
        </body>
    </html>
    '''



#index
@app.route('/')
def index():
    return template(getContents(),'Welcome','Hello')

#create
@app.route('/create/',methods=['GET','POST'])
def create():
    if request.method == 'GET':
        content = f'''
            <form action="/create/" method="POST">
                <p><input type="text" name = "title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>    
                <p><input type="submit" value="create"></p>
            </form>
        '''
        return template(getContents(),'Create',content)
    elif request.method == 'POST' :
        global nxtId
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id':nxtId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = f'/read/{nxtId}'
        nxtId+=1
        return redirect(url)

#read
@app.route('/read/<int:id>')
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title=topic['title']
            body= topic['body']
            break
        #
    #

    return template(getContents(),title,body,id)
###

#update
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method == 'GET':

        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title=topic['title']
                body= topic['body']
                break
            #
        #

        content = f'''
            <form action="/update/{id}" method="POST">
                <p><input type="text" name = "title" placeholder="title" value = {title}></p>
                <p><textarea name="body" placeholder="body">{body}</textarea></p>    
                <p><input type="submit" value="update"></p>
            </form>
        '''
        return template(getContents(),'Update',content)

    elif request.method == 'POST' :
        global nxtId
        title = request.form['title']
        body = request.form['body']

        for topic in topics:
            if id == topic['id']:
                topic['title']=title
                topic['body']=body
                break
            #
        #

        url = f'/read/{id}'
        return redirect(url)

#delete
@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
        #
    #
    
    return redirect('/')
###


app.run(debug=True)