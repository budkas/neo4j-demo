WITH date('2021-06-30') as curDate
WITH curDate, curDate-duration({days:30}) as curDate30
MATCH p=(ah1:AccHolder)-[:HAS_BANKACCOUNT]->(ba1:BankAccount)-[:SEND]->(trf1:BankTransfer)-[:SEND]->(ba2:BankAccount)-[:SEND]->(trf2:BankTransfer)-[:SEND]->(ba3:BankAccount)<-[:HAS_BANKACCOUNT]-(ah2:AccHolder)
WHERE trf1.transferDate <= curDate
    AND trf1.transferDate >= curDate30
    AND trf2.transferDate >= trf1.transferDate
    AND duration.inDays(trf1.transferDate, trf2.transferDate).days <=7
    AND trf2.amount > trf1.amount * 0.75
    AND trf2.amount < trf1.amount
    AND trf1.amount > 1000
RETURN p