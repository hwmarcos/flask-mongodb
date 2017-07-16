from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)
database = client['flask_mongo']
collection = database.books


@app.route('/')
def index():
    return render_template('main/home.html')


@app.route('/books/new', methods=['GET'])
def new():
    return render_template('books/new.html')


@app.route('/books', methods=['GET'])
def list():
    list_collection = collection.find()
    return render_template('books/list.html', books=list_collection)


@app.route('/books/<id>', methods=['GET'])
def listOne(id):
    data = collection.find_one({
        '_id': ObjectId(id)
    })
    return render_template('books/one.html', book=data)


@app.route('/books/edit/<id>')
def edit(id):
    data = collection.find_one({
        '_id': ObjectId(id)
    })
    return render_template('books/edit.html', book=data)


@app.route('/books/update/<id>', methods=['POST'])
def update(id):
    collection.update_one({
        '_id': ObjectId(id)
    }, {
        '$set': {
            'name': request.form['name'],
            'subtitle': request.form['subtitle'],
            'isbn': request.form['isbn'],
        }
    })
    return redirect(url_for('list'))


@app.route('/books/<id>', methods=['POST'])
def remove(id):
    collection.delete_many({
        '_id': ObjectId(id)
    })
    return redirect(url_for('list'))


@app.route('/books/create', methods=['POST'])
def create():
    collection.insert_one({
        'name': request.form['name'],
        'subtitle': request.form['subtitle'],
        'isbn': request.form['isbn'],
    })
    return redirect(url_for('list'))


@app.route('/books/list', methods=['GET'])
def booklist():
    result = collection.find().count()
    # result = collection.find().sort('isbn', DESCENDING)
    # result = collection.find().limit(2)
    return jsonify(result=result)


if __name__ == '__main__':
    app.run()
