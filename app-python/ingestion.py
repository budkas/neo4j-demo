# %%
from Connection import Neo4j

# %%
neo4j_conn = Neo4j()
driver = neo4j_conn.get_driver()

# %%
def drop_all_nodes():
    """
    This function deletes all the nodes from the Neo4j database.
    
    Parameters:

    Returns: int
        Returns the number of nodes deleted
    """
    def delete_all_nodes_tx(tx):
        cypher = "MATCH(n) DETACH DELETE n RETURN 1"
        result = tx.run(cypher)
        return len([row for row in result])

    with driver.session() as session:
        return session.execute_write(delete_all_nodes_tx)

# %%
def create_constrints():
    """
    This function creates the required constraints for the graph database
    """
    # Define the Cypher
    constraint_cyphers = [
        """
        CREATE CONSTRAINT cn_unq_accholder_cif IF NOT EXISTS
        FOR (ah:AccHolder)
        REQUIRE ah.cif IS UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_accholder_email IF NOT EXISTS
        FOR (ah:AccHolder)
        REQUIRE ah.email IS UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_bankaccount_accnum IF NOT EXISTS
        FOR (acc:BankAccount)
        REQUIRE acc.accNum is UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_phone_number IF NOT EXISTS
        FOR (p:Phone)
        REQUIRE p.number is UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_job_title IF NOT EXISTS
        FOR (j:Job)
        REQUIRE j.title is UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_country_name IF NOT EXISTS
        FOR (c:Country)
        REQUIRE c.name is UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_address_street_zip IF NOT EXISTS
        FOR (addr:Address)
        REQUIRE (addr.street, addr.zip) IS NODE KEY;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_banktransfer_transactionId IF NOT EXISTS
        FOR (trf:BankTransfer)
        REQUIRE trf.transactionId is UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_nn_banktransfer_amount IF NOT EXISTS
        FOR (trf:BankTransfer)
        REQUIRE trf.amount is NOT NULL;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_creditcard_cardnum IF NOT EXISTS
        FOR (cc:CreditCard)
        REQUIRE cc.cardNum is UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_purchase_transactionId IF NOT EXISTS
        FOR (p:Purchase)
        REQUIRE p.transactionId is UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_nn_purchase_amount IF NOT EXISTS
        FOR (p:Purchase)
        REQUIRE p.amount is NOT NULL;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_merchant_name IF NOT EXISTS
        FOR (m:Merchant)
        REQUIRE m.name is UNIQUE;
        """
        ,
        """
        CREATE CONSTRAINT cn_unq_cardissuer_name IF NOT EXISTS
        FOR (c:CardIssuer)
        REQUIRE c.name is UNIQUE;
        """
    ]

    # Execute in an Implicit transaction
    with driver.session() as session:
        for stmt in constraint_cyphers:
            r = session.run(stmt)

# %%
def load_customer_csv():

    # Define the cypher statement
    import_customer_cypher = r"""
    CALL {
        LOAD CSV WITH HEADERS FROM "file:///./banking/customers.csv" AS row

        // *** Create Account Holders ***
        CREATE (ah:AccHolder {
            cif: toInteger(row.CIF),
            name: row.FirstName + " " + row.LastName, 
            email: toLower(row.EmailAddress),
            age: toInteger(row.Age),
            gender: toUpper(row.Gender),
            country: trim(row.Country)
        })

        // *** Create Bank Accounts ***
        MERGE (ba:BankAccount {
            accNum: row.AccountNumber
        })

        // *** Create Credit Cards ***
        MERGE (cc:CreditCard {
            cardNum: row.CardNumber
        })

        // *** Create Address ***
        MERGE (addr:Address {
            street: apoc.text.capitalizeAll(apoc.text.replace(toLower(trim(split(row.Address,',')[0])),'\s+',' ')),
            zip: toInteger(trim(split(row.Address,',')[1]))
        })

        // *** Create Phone ***
        MERGE (phone:Phone {
            number: row.PhoneNumber
        })

        // *** Create Job ***
        MERGE (job:Job {
            title: row.JobTitle
        })

        // *** Create Country ***
        MERGE (country:Country {
            name: apoc.text.capitalizeAll(toLower(trim(row.Country)))
        })

        // *** Relate AccHolders to Address ***
        MERGE (ah)-[:HAS_ADDRESS]->(addr)

        // *** Relate AccHolders to Phone ***
        MERGE (ah)-[:HAS_PHONE]->(phone)

        // *** Relate AccHolders to BankAccount ***
        MERGE (ah)-[:HAS_BANKACCOUNT]->(ba)

        // *** Relate AccHolders to CreditCard ***
        MERGE (ah)-[:HAS_CREDITCARD]->(cc)

        // *** Relate AccHolders to Job ***
        MERGE (ah)-[:WORKS_AS]->(job)

        // *** Relate AccHolders to Country ***
        MERGE (ah)-[:CITIZEN_OF]->(country)
        
    } IN TRANSACTIONS OF 10 ROWS
    """

    # Execute in an Implicit transaction
    with driver.session() as session:
        r = session.run(import_customer_cypher)

# %%
def load_transfers_csv():

    # Define the cypher statement
    create_transfers_cypher = r"""
    CALL {
        LOAD CSV WITH HEADERS FROM "file:///./banking/transfers.csv" AS row

        // *** Create BankTransfers ***
        CREATE (trf:BankTransfer {
            transactionId: toInteger(row.TransactionID),
            amount: toFloat(row.Amount),
            transferDate: date(datetime({epochMillis:apoc.date.parse(row.TransferDatetime, "ms", "yyyy-MM-dd HH:mm:ss")})),
            transferTime: time(datetime({epochMillis:apoc.date.parse(row.TransferDatetime, "ms", "yyyy-MM-dd HH:mm:ss")}))
        })
    } IN TRANSACTIONS OF 100 ROWS
    """

    # Define a cypher statment to create necessary reletionships
    create_rels_cypher = r"""
    CALL {
        LOAD CSV WITH HEADERS FROM "file:///./banking/transfers.csv" AS row

        // *** Relate Transfers to Sender Account and Receiver Account***
        MATCH(trf:BankTransfer {transactionId: toInteger(row.TransactionID)})
        MATCH(sendAcc:BankAccount {accNum: row.SenderAccountNumber})
        MATCH(recAcc:BankAccount {accNum: row.ReceiverAccountNumber})
        MERGE(sendAcc)-[:SEND]->(trf)
        MERGE(trf)-[:SEND]->(recAcc)
    } IN TRANSACTIONS OF 100 ROWS
    """

    # Execute in an Implicit transaction
    with driver.session() as session:
        r = session.run(create_transfers_cypher)
        r = session.run(create_rels_cypher)

# %%
def load_purchases_csv():

    # Define the cypher statement
    create_purchases_cypher = r"""
    CALL {
        LOAD CSV WITH HEADERS FROM "file:///./banking/purchases.csv" AS row

        // *** Create Purchases ***
        CREATE (p:Purchase {
            transactionId: toInteger(row.TransactionID),
            amount: toFloat(row.Amount),
            purchaseDate: date(datetime({epochMillis:apoc.date.parse(row.PurchaseDatetime, "ms", "yyyy-MM-dd HH:mm:ss")})),
            purchaseTime: time(datetime({epochMillis:apoc.date.parse(row.PurchaseDatetime, "ms", "yyyy-MM-dd HH:mm:ss")}))
        })

        // *** Create Merchant ***
        MERGE (m:Merchant {
            name: trim(row.Merchant)
        })

        // *** Create Card Issuer ***
        MERGE (ci:CardIssuer {
            name: trim(row.CardIssuer)
        })

        WITH p, m, ci, row
        MATCH(cc:CreditCard {cardNum: row.CardNumber})
        MERGE(p)-[:ISSUED_BY]->(ci)
        MERGE(p)-[:WITH_CARD]->(cc)
        MERGE(p)-[:FROM]->(m)
    } IN TRANSACTIONS OF 100 ROWS
    """
    
    # Execute in an Implicit transaction
    with driver.session() as session:
        r = session.run(create_purchases_cypher)

# %%
def load_countries_csv():

    # Define the cypher statement
    update_countries_cypher = r"""
    CALL {
        LOAD CSV WITH HEADERS FROM "file:///./banking/countries.csv" AS row

        MERGE (c:Country {name: apoc.text.capitalizeAll(toLower(trim(row.ShortName)))})
        ON CREATE SET c.name = apoc.text.capitalizeAll(toLower(trim(row.ShortName))),
                        c.code = row.Alpha3Code,
                        c.region = row.Region
        ON MATCH SET c.code = row.Alpha3Code,
                        c.region = row.Region 
    } IN TRANSACTIONS OF 10 ROWS
    """

    # Execute in an Implicit transaction
    with driver.session() as session:
        r = session.run(update_countries_cypher)

# %%
def load_data():
    """
    This function delete any exisiting data, create required constraints for the demo banking use case,
    and load data from customer, tranfers and purchase CSV files.
    """
    # Clear the database
    drop_all_nodes()
    print("Database cleaned!")

    # Create required constraints
    create_constrints()
    print("Constraints created!")

    # Import customer.csv and create relevant nodes and relationships
    load_customer_csv()
    print("customer.csv loaded successfully!")

    # Import transfers.csv and create relevant nodes and relationships
    load_transfers_csv()
    print("transfers.csv loaded successfully!")

    # Import purchases.csv and create relevant nodes and relationships
    load_purchases_csv()
    print("purchases.csv loaded successfully!")

    #Enrich country nodes
    load_countries_csv()
    print("countries.csv loaded successfully")

# %%
load_data()


