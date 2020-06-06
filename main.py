import db
import config
import manager
import api

import sys

if __name__ == "__main__":
    conf = config.load_config()
    mode = conf.mode
    if len(sys.argv) > 1:
        mode = sys.argv[1] # second argument

    db_instance = db.DB(conf.postgres_uri)

    peruvian_extractor = manager.Extractor(db_instance, "peru") # search query in twitter

    if mode == "full" or mode == "extractor":
        controller = manager.Manager(db_instance)
        controller.register_new_extractor(peruvian_extractor)
        controller.launch_extractors()

    if mode == "full" or mode == "api":
        app = api.craft_api(db_instance, conf)
        app.run(port=8080, host="0.0.0.0")
