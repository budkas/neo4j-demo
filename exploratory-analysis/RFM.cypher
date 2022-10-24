WITH date('2021-06-30') as curDate
WITH curDate, curDate-duration({days:30}) as curDate30
MATCH(ah:AccHolder)-[h:HAS_CREDITCARD]->(c:CreditCard)<-[w:WITH_CARD]-(p:Purchase)-[:FROM]->(m:Merchant)
WHERE p.purchaseDate <= curDate AND p.purchaseDate >= curDate30
WITh ah,
    m,
    SUM(p.amount) as monetory,
    COUNT(DISTINCT p) as frequency,
    MIN(
        duration.inDays(
            p.purchaseDate, curDate
        ).days
    ) AS recency
WHERE recency < 5 AND monetory > 5000 AND frequency > 2
WITH ah,m
MATCH p=(ah)-[:HAS_CREDITCARD]->(:CreditCard)<-[:WITH_CARD]-(:Purchase)-[:FROM]->(m)
RETURN p