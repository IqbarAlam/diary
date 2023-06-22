from flask import Flask,render_template,jsonify,request
from pymongo import MongoClient
from datetime import datetime

con_string='mongodb+srv://IqbarNuansaAlam:20060217alam@cluster0.rna8sob.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(con_string)
db = client.Testing

app= Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    articles = list(db.diary.find({}, {'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form.get('sample_give')
    # print(sample_receive)
    title_receive = request.form.get("title_give")
    content_receive = request.form.get("content_give")
    profile_receive = request.files['profile_give']
    extension_prf = profile_receive.filename.split('.')[-1]

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    today = datetime.now()  
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    file_name_profile = f'static/profile-{mytime}.{extension_prf}'
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)
    profile_receive.save(file_name_profile)

    time = today.strftime('%Y.%m.%d')

    doc = {
        'file' : filename,
        'profile': file_name_profile,   
        'title': title_receive,
        'content': content_receive,
        'time':time,         
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': 'data was saved'})

if __name__== '__main__':
    app.run('0.0.0.0', port=5000, debug=True )