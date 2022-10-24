MATCH (c1:Country)<-[:CITIZEN_OF]-(ah1:AccHolder)-[:HAS_BANKACCOUNT]->(sender:BankAccount)-[:SEND]->
(trf:BankTransfer)-[:SEND]->(receiver:BankAccount)<-[:HAS_BANKACCOUNT]-(ah2:AccHolder)-[:CITIZEN_OF]->(c2:Country)
// remove local transfers
WHERE c1.name <> c2.name
WITH c1, c2
,count(trf.amount) as numTransfers, sum(trf.amount) as totalTransfer
WHERE numTransfers > 2
MATCH p=(c1)<-[:CITIZEN_OF]-(ah1:AccHolder)-[:HAS_BANKACCOUNT]->(sender:BankAccount)-[:SEND]->
(trf:BankTransfer)-[:SEND]->(receiver:BankAccount)<-[:HAS_BANKACCOUNT]-(ah2:AccHolder)-[:CITIZEN_OF]->(c2)
RETURN p