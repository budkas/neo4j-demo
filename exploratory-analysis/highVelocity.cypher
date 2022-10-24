MATCH (acc1:BankAccount)-[r:SEND]-(:BankTransfer)
WITH distinct acc1, type(r) as rel, count(r) as cnt
WHERE cnt > 25
MATCH p1=(:AccHolder)-[:HAS_BANKACCOUNT]->(acc1)-[:SEND]-(:BankTransfer)-[:SEND]-(:BankAccount)<-[:HAS_BANKACCOUNT]-(:AccHolder)
RETURN p1