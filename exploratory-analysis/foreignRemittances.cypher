MATCH(c1:Country)<-[:CITIZEN_OF]-(sender:AccHolder)-[:HAS_BANKACCOUNT]->(fromAcc:BankAccount)-[:SEND]->(trf:BankTransfer)-[:SEND]->(toAcc:BankAccount)<-[:HAS_BANKACCOUNT]-(receiver:AccHolder)-[:CITIZEN_OF]->(c2:Country)
WHERE c1.name <> c2.name
WITH c1, c2, sender, receiver
MATCH (receiver)-[:HAS_BANKACCOUNT]->(:BankAccount)-[:SEND]->(:BankTransfer)-[:SEND]->(:BankAccount)<-[:HAS_BANKACCOUNT]-(newReceiver:AccHolder)-[:CITIZEN_OF]->(c1)
WITH sender, newReceiver
MATCH p=(sender)-[:SEND|HAS_BANKACCOUNT|WORKS_AS*2..4]-(newReceiver)
RETURN p