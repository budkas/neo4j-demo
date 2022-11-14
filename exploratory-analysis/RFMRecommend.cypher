WITH date('2021-06-30') as curDate, 'ENEL' as merchantName
WITH curDate, merchantName, curDate-duration({days:30}) as curDate30
MATCH(ah:AccHolder)-[h:HAS_CREDITCARD]->(c:CreditCard)<-[w:WITH_CARD]-(p:Purchase)-[:FROM]->(m:Merchant {name:merchantName})
WHERE p.purchaseDate <= curDate AND p.purchaseDate >= curDate30
WITh ah,
    SUM(p.amount) as monetory,
    COUNT(DISTINCT p) as frequency,
    MIN(
        duration.inDays(
            p.purchaseDate, curDate
        ).days
    ) AS recency
WHERE recency < 5 AND monetory > 5000 AND frequency > 2
WITH ah
MATCH (ah)-[:HAS_BANKACCOUNT]->(:BankAccount)-[:SEND]-(:BankTransfer)-[:SEND]-(:BankAccount)<-[:HAS_BANKACCOUNT]-(friend:AccHolder)
WITH ah as cust, friend as friend, count(friend) as frequency
WHERE frequency > 0
RETURN  friend