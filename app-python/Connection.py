# tag::import[]
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# end::import[]

class Neo4j:
    """
    Initiate the Neo4j Driver
    """
    # tag::initDriver[]
    def __init__(self):
        
        load_dotenv()
        NEO4J_URI=os.getenv('NEO4J_URI')
        NEO4J_USERNAME=os.getenv('NEO4J_USERNAME')
        NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')

        assert NEO4J_URI is not None, "Missing .env?"

        # Create a new Driver instance
        self.driver = GraphDatabase.driver(NEO4J_URI,
            auth=(NEO4J_USERNAME, NEO4J_PASSWORD))
        # Verify Connectivity
        self.driver.verify_connectivity()
    # end::initDriver[]


    """
    Get the instance of the Neo4j Driver created in the `initDriver` function
    """
    # tag::getDriver[]
    def get_driver(self):
        return self.driver

    # end::getDriver[]

    """
    If the driver has been instantiated, close it and all remaining open sessions
    """
    # tag::closeDriver[]
    def close_driver(self):
        if self.driver != None:
            self.driver.close()
            self.driver = None

            return self.driver
    # end::closeDriver[]