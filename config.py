import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # Para producción, DATABASE_URL se establece con el comando gcloud.
    # Para desarrollo, construimos una ruta absoluta a la DB local.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:eK86MYFIPB8c32t7@db.vwdujeylaytybxdwqnsz.supabase.co:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False