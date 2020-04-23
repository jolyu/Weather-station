from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

def GetDbRef(keyLoc, dbURL):
    """ 
    Creates a connecton reference to the Firebase database, using a key with location keyLoc and the URL for the realtime database dbURL.
    """
    # Credentials file
    cred = credentials.Certificate(keyLoc)

    # Initialize the app
    firebase_admin.initialize_app(cred, dict(
        databaseURL = dbURL
    ))
    # Return the actual database reference
    return db.reference()


def PushDB(dbRef, data):
    """
    Push data to a database with reference dbRef. Data should be a dictionary with only data, with no time, it will be added when sent.
    """
    # Finds current timestamp
    timestamp = datetime.now().timestamp()
    # Converts it to string firebase can use
    tsShort = str(round(timestamp))
    # Add the timestamp to dataset
    data.update(time = timestamp)
    # Add data with key tsShort to the database with reference dbRef
    dbRef.child(tsShort).set(data)

    print("Pushed data to database.\n")