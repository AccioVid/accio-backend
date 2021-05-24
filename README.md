# ACCIO

## Getting started

install [docker-compose](https://docs.docker.com/compose/install/)

first time setup
```bash
docker-compose up -d
scripts/init.sh
pip install -r requirements.txt
```



for database migration and setup:
```bash
flask db migrate
flask db upgrade
```

to login to accio db inside the container:
```
docker-compose exec db bash
psql accio -U postgres
```

run the server

```bash
flask run
```

To run yolo object detection you have to donwload the [yolov3.weights](https://pjreddie.com/media/files/yolov3.weights)
Then add yolov3.weights in
```
plugins/yolo_object_detection/yolo_coco
```
## Implementation Details

### Tables
- Videos
  - id
  - title
  - metadata
  - path/url
- Plugins
  - id
  - name
  - is_enabled
  - executable_path
  - system_configuration
  - plugin_configuration
  
### Services, Classes and Directory Structure
- api/ - flask api serving the frontend
- engine/ - module carrying all the logic happening behind the scenes
  - datafeed::DataFeeder
  - keyframes::KeyFrameExtractor
  - plugins::PluginManager
    - abstracts the interaction with plugins
  - engine::EngineManager
    - discover video from datafeed
    - for each plugin in plugins list
      - perform keyframes extraction on video (depending on its system configuration)
      - form input obj (either output of keyframes or raw video)
      - output = PluginManager.run(plugin, input_obj)
      - Indexer.index(video, output)
  - indexer::Indexer
    - reflect output results to video db records
      - output: (view only)
        ```json
        {
          "src_name": "xxx",
          "results": "xxx"
          [
            {
              "from": "xxx",
              "to": "xxx",
              "content": "xxx",
              "bb": [],
              "confidence": "xx" 
            }
          ]
        }
        ```

- plugins/ - repository of all implemented plugins
  - each plugin inherits from an AbstractPlugin class, implementing a `run` method and `configurationDict` field



### Screens

#### Client UI
A search box that sends the query to /api/search?q="xxx"x and renders the results with potential interaction with the videos and their frames

#### Admin UI
A place to manage plugins and their configuration

