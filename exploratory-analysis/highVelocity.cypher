MATCH (acc:BankAccount)-[r:SEND]-(:BankTransfer)
WITH distinct acc, count(r) as cnt
WHERE cnt > 23
MATCH path=(acc)<-[:HAS_BANKACCOUNT]-(ah:AccHolder)-[rel*2..4]-(ah2:AccHolder)
WHERE ALL(r in rel WHERE not(type(r)='CITIZEN_OF') )
RETURN path