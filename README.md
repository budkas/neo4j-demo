# Neo4j Demo Application
## How to setup?
1. Clone the repository
2. Setup the Python environment
    * Create a new Python(3.9) virtual environment for the project<br>
    * Install the required Python packages using the *requirements.txt*
3. Start the Neo4j Enterprise docker
    * Issue ```docker-compose up``` command from the root directory<br>
    Note: *plugins folder contains the neo4j's extension library - APOC*
    * Login to Neo4j Browser: http://localhost:7474<br>
    Username: *neo4j*, Password: *test*

## Data Model
The image below illustrates the proposed graph data model for the banking dataset (https://gist.github.com/maruthiprithivi/f11bf40b558879aca0c30ce76e7dec98) provided.
![Graph data model](./data-model/dataModel-banking.png "Graph data model")

### Constraints
The table below shows the constraints used to ensure the data integrity of the proposed data model.
![Graph data model](./data-model/constraints-banking.png "Graph data model")
## Import Data
Note: *Duplicate records (based on the TransactionID) have been removed from transfers.csv and purchases.csv.* 
1. Run all the cells in *app-python/ingestion.ipynb* to create the graph data model and load the data from the CSV files (customer, transfers, and purchases) residing in the *data/banking* folder.
Alternatively, you can run the *ingestion.py* file in the app-python folder as follows:
```
    cd app-python
    python ingestion.py
```
## Python Application to Explore Patterns
The *analysis.ipynb* file inside the *app-python* folder contains the cypher queries-based functions used to identify a few useful patterns based on the dataset and the proposed data model. You can pass different parameters to change the output as per your business requirement.

## Exploratory Analysis
I developed the following 06 Cypher queries to explore interesting patterns in the banking dataset. You can find these queries inside the *exploratory-analysis* folder. This folder also contains screenshots corresponding to the graph output of each Cypher query.
### layering.cypher
This Cypher query looks for passthrough payments (A)->(B)->(C). The query scans transfers over 1000 over the last 30 days from 2021-06-30 to find passthrough payments, i.e., any outward transfers of a high percentage (>75%) of an incoming transfer within the last seven days. The query returns the route of the passthrough payments.
The *analysis.ipynb* file inside the *app-python* folder contains the cypher queries-based functions used to identify a few useful patterns based on the dataset and the proposed data model.

### aggregators.cypher
This Cypher query examines deposits (incoming transfers) or withdrawals (outgoing transfers) made during a lookback period of 30 days (from 2021-06-30) where multiple in and out transfer amounts aggregate over 10,000. Then, it looks for rapid outgoing transfers (i.e., within 10 days from the incoming transfer date) from those accounts where the aggregated outgoing transfer amount is within 75%-100% of the incoming transfers. The query returns the identified account holders (aggregators) and their money transfer behaviour.

### RFM.cypher
The Recency, Frequency, and Monetary (RFM) analysis the loyalty of the customers towards various merchants. This Cypher query looks back at the last 30 days of purchase records from 2021-06-30 to obtain the recency, frequency, and monetary values for customers against different merchants. Next, the query identifies high-value high-loyal customers (recency < 5 AND monetary > 5000 AND frequency > 2) and returns their interactions with corresponding merchants.

### foreignRemittances.cypher
For this analysis, I considered the customer's country as the location of their bank. In this case, any bank transfer to a bank account from an account in a different country is considered a foreign remittance. This Cypher query identifies the countries between which the volume of foreign remittances is high. The query returns the flow of bank transfers between selected countries.

### highVolume.cypher
This Cypher query identifies accounts with high volume incoming and outgoing transfers for the last 30 days (from 2021-06-30). An account is considered a high-volume transaction account if the aggregated incoming or outgoing transfers exceed 190000. The query returns the selected accounts and corresponding incoming and outgoing transfers.

### highVelocity.cypher
This Cypher query counts the total number of incoming and outgoing transfers to an account to identify high-velocity bank accounts. The query returns bank accounts with more than 25 transactions (incoming or outgoing) and corresponding incoming and outgoing transfers along with the account holders at the other end of the transactions.