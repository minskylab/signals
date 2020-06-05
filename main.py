import db
import config
import manager
import api

if __name__ == "__main__":
    conf = config.load_config()
    db_instance = db.DB(conf.postgres_uri)

    peruvian_extractor = manager.Extractor(db_instance, "peru") # search query in twitter

    controller = manager.Manager(db_instance)
    controller.register_new_extractor(peruvian_extractor)
    # controller.launch_extractors()

    app = api.craft_api(db_instance, conf)

    app.run(debug=True, port=8080)
