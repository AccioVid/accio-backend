import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/accio"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def __save_to_db(obj):
    db.session.add(obj)
    db.session.commit()

# models
class VideosModel(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    duration = db.Column(db.Integer())
    url = db.Column(db.String())
    """
        {
            
        }
    """
    results = db.Column(db.String())

    def __init__(self, name, duration, url, results):
        self.name = name
        self.duration = duration
        self.url = url
        self.results = json.dumps(results)

    @property
    def json_results(self):
        return json.loads(self.results)

    def __repr__(self):
        return f"<Video {self.name}>"




# apis
@app.route('/')
def hello():
    return "Hello World, I'm Accio!"

@app.route('/search')
# localhost:5000/search?query=hamada
def query():
    keyword = request.args.get('query')
    return {
        "keyword": keyword
    }
    # results = VideosModel.objects.filter(reults=match(keyword))
    # return results

if __name__ == '__main__':
    app.run(debug=True)
