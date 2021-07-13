import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import JSON
import warnings 
warnings.filterwarnings(action='ignore')

from flask_cors import CORS, cross_origin
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/accio"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)
# app.config['CORS_HEADERS'] = 'application/json'
# app.config['Access-Control-Allow-Origin'] = '*'

class DBModel:
    def __repr__(self):
        return f"<{type(self)} {self.name}>"

    def save(self):
        db.session.add(self)
        self.persist()

    def delete(self):
        db.session.delete(self)
        self.persist()
    
    def persist(self):
        db.session.commit()


class PluginsModel(DBModel, db.Model):
    __tablename__ = 'plugins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    is_enabled = db.Column(db.Boolean)
    executable_path = db.Column(db.String())
    system_configuration = db.Column(JSON)
    plugin_configuration = db.Column(JSON)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_enabled": self.is_enabled,
            "executable_path": self.executable_path,
            "system_configuration": self.system_configuration,
            "plugin_configuration": self.plugin_configuration,
        }

class VideosModel(DBModel, db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    duration = db.Column(db.Integer())
    url = db.Column(db.String())
    results = db.Column(JSON)
    processed = db.Column(db.Boolean)

    def __init__(self, name, duration, url, results=None, processed=False):
        self.name = name
        self.duration = duration
        self.url = url
        self.results = results
        self.processed = processed

    def to_json(self):
        return {
            "name": self.name,
            "duration": self.duration,
            "url": self.url,
            "results": self.results,
            "processed": self.processed,
        }

# apis
@app.route('/')
@cross_origin()
def hello():
    return "Hello World, I'm Accio!"

@app.route('/plugins', methods=['GET'])
@cross_origin()
def get_plugins():
    plugins = PluginsModel.query.all()
    return {
        "response": [p.to_json() for p in plugins]
    }
#end def

@app.route('/plugins', methods=['POST'])
@cross_origin()
def edit_plugin():
    data = request.get_json('query')
    id = data['id']
    plugin = PluginsModel.query.get(id)
    for key, value in data.items():
        if key != 'id' and hasattr(plugin, key):
            setattr(plugin, key, value)
    plugin.save()
    return {
        "response": plugin.to_json()
    }
#end def



@app.route('/search', methods=['POST'])
@cross_origin()
def videos_search():
    keywords = request.get_json('query')['query'].split(' ')
    videos = set([])
    for keyword in keywords:
        results = VideosModel.query.filter(VideosModel.results.contains(keyword))
        for r in results:
            videos.add(r)
    
    videos = list(videos)
    for v in videos:
        new_results = []
        old_results = json.loads(v.results)
        for frame_results in old_results:
            for result in frame_results['results']:
                done = False
                for keyword in keywords:
                    is_enabled = PluginsModel.query.filter_by(name=result['content-type'], is_enabled=True).count()
                    
                    if keyword in result['content'] and is_enabled > 0:
                        new_results.append(frame_results)
                        done = True
                        break
                if done:
                    break
        v.results = new_results
    return {
        "response": [v.to_json() for v in videos]
    }
#end def

if __name__ == '__main__':
    app.run(debug=True)

