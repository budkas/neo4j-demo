WITH date('2021-06-30') as curDate, 190000 as curThreshold
WITH curThreshold, curDate, curDate-duration({days:30}) as curDate30
MATCH (trf:BankTransfer)
CALL {
    WITH trf, curDate, curDate30, curThreshold
    MATCH (trf)<-[:SEND]-(acc:BankAccount)
    WHERE trf.transferDate <= curDate
    AND trf.transferDate >= curDate30
    WITH acc.accNum as curAccNum, trf.transferDate as transactionDate, sum(trf.amount) as totAmount, curThreshold
    WHERE totAmount > curThreshold
    RETURN curAccNum, transactionDate, totAmount, 'Debit' as transactionType
    UNION ALL
    WITH trf, curDate, curDate30, curThreshold
    MATCH (trf)-[:SEND]->(acc:BankAccount)
    WHERE trf.transferDate <= curDate
    AND trf.transferDate >= curDate30
    WITH acc.accNum as curAccNum, trf.transferDate as transactionDate, sum(trf.amount) as totAmount, curThreshold
    WHERE totAmount > curThreshold
    RETURN curAccNum, transactionDate, totAmount, 'Credit' as transactionType 
}
WITH curAccNum, transactionDate, totAmount, transactionType
MATCH p=(ah:AccHolder)-[:HAS_BANKACCOUNT]->(ba:BankAccount {accNum: curAccNum})-[:SEND]-(:BankTransfer)
RETURN p