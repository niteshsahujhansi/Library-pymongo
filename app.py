from datetime import date
from flask import Flask, render_template
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, request 

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/library'
mongo = PyMongo(app)

mylist=[
    {
            "book_name": "blockchain",
            "category": "mca-iv",
            "rent_per_day": "5"
        },
        {
            "book_name": "machine learning",
            "category": "mca-iv",
            "rent_per_day": "5"
        },
        {
            "book_name": "data analytics",
            "category": "mca-iv",
            "rent_per_day": "5"
        },
        {
            "book_name": "python",
            "category": "mca-iii",
            "rent_per_day": "4"
        },
        {
            "book_name": "operating system",
            "category": "mca-iii",
            "rent_per_day": "4"
        },
        {
            "book_name": "database",
            "category": "mca-iii",
            "rent_per_day": "4"
        },
        {
            "book_name": "organization and architechure",
            "category": "mca-iii",
            "rent_per_day": "4"
        },
        {
            "book_name": "c",
            "category": "mca-ii",
            "rent_per_day": "3"
        },
        {
            "book_name": "data structure and algorithms",
            "category": "mca-ii",
            "rent_per_day": "3"
        }
    ]

mongo.db.BOOKS.insert_many(mylist)
# mongo.db.BOOKS.updateOne({}, {'$setOnInsert' :mylist},{'upsert' :'true'})


# add books detail
@app.route('/books', methods=['POST'])
def add_book():
    _json = request.json
    _book_name = _json['book_name']
    _category = _json['category']
    _rent_per_day = _json['rent_per_day']

    if _book_name and _category and _rent_per_day and request.method =='POST':
        id = mongo.db.BOOKS.insert_one({'book_name':_book_name, 'category':_category, 'rent_per_day':_rent_per_day})
        res = jsonify('Book added successfully')
        res.status_code = 200
        return res 
    else:
        return not_found()
  
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    res = jsonify(message)
    res.status_code = 404
    return res 

# all data
@app.route('/')
def book_issued_perso():
    book_issued_persons = [mongo.db.BOOKS.find(),mongo.db.TRANSACTION.find()]
    res = dumps(book_issued_persons)
    return res 

  

# FIRST QUERY
@app.route('/books/<book_name>')
def book_issued_persons(book_name):
    book_issued_persons = mongo.db.BOOKS.find({'book_name': {'$regex': book_name}})
    res = dumps(book_issued_persons)
    return res 

# SECOND QUERY
@app.route('/books/rent_per_day_price_range/<start>-<end>')
def rent_per_day_price_range(start,end):
    books = mongo.db.BOOKS.find(
        {'$and':
        [{"rent_per_day":
          {'$gte':start}}, 
         {"rent_per_day":
          {'$lte':end}}]}
        )
    res = dumps(books)
    return res 

# THIRD QUERY
@app.route('/books/category/<category>/book_name/<book_name>/rent_per_day_price_range/<start>-<end>')
def category_book_name_rent_per_day_price_range(category,book_name,start,end):
    books = mongo.db.BOOKS.find(
        {'$and':
        [         
          {'category':category},
          
          {'book_name': {'$regex': book_name}},
          
          {"rent_per_day":
          {'$gte':start}}, 
          {"rent_per_day":
          {'$lte':end}}
        ]}
        )
    res = dumps(books)
    return res 


mylist2=[
        {
            "person_name": "ram",
            "book_name": "blockchain",
            "issue_date": "01.01.2022",
            "price": "75",
            "return_date": "15.01.2022"
        },
        {
            "person_name": "ram",
            "book_name": "machine learning",
            "issue_date": "01.01.2022"
        },
        {
            "person_name": "shyam",
            "book_name": "machine learning",
            "issue_date": "01.01.2022"
        },
        {
            "person_name": "shyam",
            "book_name": "data analytics",
            "issue_date": "01.01.2022"
        },
        {
            "person_name": "sita",
            "book_name": "python",
            "issue_date": "8.01.2022"
        },
        {
            "person_name": "sita",
            "book_name": "data structure",
            "issue_date": "8.01.2022"
        },
        {
            "person_name": "geeta",
            "book_name": "operationg system",
            "issue_date": "8.01.2022"
        },
        {
            "person_name": "geeta",
            "book_name": "database",
            "issue_date": "8.01.2022"
        }

]

mongo.db.TRANSACTION.insert_many(mylist2)


# fourth queary (issue transaction) 
@app.route('/transaction/issue', methods=['POST'])
def issue():
    _json = request.json
    _person_name = _json['person_name']
    _book_name = _json['book_name']
    _issue_date = _json['issue_date']

    if _person_name and _issue_date and request.method =='POST':
        id = mongo.db.TRANSACTION.insert_one({'person_name':_person_name, 'book_name':_book_name, 'issue_date':_issue_date})
        res = jsonify('Book issued successfully')
        res.status_code = 200
        return res 
    else:
        return not_found()

# fifth query (return transaction)
@app.route('/transaction/return', methods=['POST'])
def returnn():
    _json = request.json
    _person_name = _json['person_name']
    _return_date = _json['return_date']
    _price = _json['price']
    
    if _return_date and _price and request.method =='POST':
        id = mongo.db.TRANSACTION.update_one(
            {'person_name':_person_name},
            {
                "$set": {'return_date':_return_date, 'price':_price}})
        res = jsonify('Book returned successfully')
        res.status_code = 200
        return res 
    else:
        return not_found()

# sixth query
@app.route('/transaction/book_issued_persons/<book_name>')
def book_issued_personss(book_name):
    book_issued_persons = (
        mongo.db.TRANSACTION.find({"book_name":book_name}),
        mongo.db.TRANSACTION.count_documents({"book_name":book_name}))
    res = dumps(book_issued_persons)
    return res

# seventh query
@app.route('/transaction/person_issued_books/<person_name>')
def book_issued_personsss(person_name):
    book_issued_persons = (
        mongo.db.TRANSACTION.find({"person_name":person_name}),
        mongo.db.TRANSACTION.count_documents({"person_name":person_name}))
    res = dumps(book_issued_persons)
    return res

# eighth query
@app.route('/transaction/date_range_issued_persons_books/(<start>)-(<end>)')
def rook_issued_personssss(start,end):
    books = mongo.db.TRANSACTION.find(
        {'$and':
        [{"issue_date":
          {'$gte':start}}, 
         {"return_date":
          {'$lte':end}}]}
        )
    res = dumps(books)
    return res







if __name__ == "__main__":
    app.run(debug=True)

