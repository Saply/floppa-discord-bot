import dotenv, os, mongoengine

dotenv.load_dotenv()

AAA = os.getenv("MONGO_PASSWORD")
print(AAA)

mongoengine.connect("test")