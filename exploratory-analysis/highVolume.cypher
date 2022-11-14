WITH date('2021-06-30') as curDate, 180000 as curThreshold
WITH curThreshold, curDate, curDate-duration({days:30}) as curDate30
WITH curDate, curDate30, curThreshold
UNWIND [days IN range(1,duration.between(curDate30,curDate).days) | 
         curDate30 + duration({days:days})] as day
OPTIONAL MATCH (credit)-[:SEND]->(acc:BankAccount) //inward transfers
WHERE credit.transferDate = day
OPTIONAL MATCH (acc)-[:SEND]->(debit) //outward transfers
WHERE debit.transferDate = day
WITH acc, day, curThreshold, sum(credit.amount) as credits, sum(debit.amount) as debits
WHERE credits > curThreshold OR debits > curThreshold
MATCH path=(acc)<-[:HAS_BANKACCOUNT]-(ah:AccHolder)-[rel*2..4]-(ah2:AccHolder)
WHERE ALL(r in rel WHERE not(type(r)='CITIZEN_OF') )
RETURN path