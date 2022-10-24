WITH date('2021-06-30') as curDate
WITH curDate, curDate-duration({days:30}) as curDate30
MATCH (ah:AccHolder)-[:HAS_BANKACCOUNT]->(recAcc:BankAccount)<-[:SEND]-(trf:BankTransfer)
WHERE trf.transferDate >= curDate30
AND trf.transferDate <= curDate
WITH recAcc.accNum as accountNumber,
	min(trf.transferDate) as StartDate,
	max(trf.transferDate) as EndDate,
	duration.inDays(min(trf.transferDate),max(trf.transferDate)).days as NumDays,
	count(trf.amount) as NumDeposits,
	sum(trf.amount) as TotalDeposits
WHERE TotalDeposits > 10000
WITH collect({accNum: accountNumber,
				startDate: StartDate,
				endDate: EndDate,
				numDays: NumDays,
				numDeposits: NumDeposits,
				totDeposits: TotalDeposits}) as aggregators
				
// find all the rapid outgoing transfers of high percentage of incoming transfers
UNWIND aggregators as curAgg
MATCH (ba:BankAccount)-[:SEND]->(trf:BankTransfer)
WHERE ba.accNum = curAgg.accNum
AND trf.transferDate >= curAgg.startDate
AND trf.transferDate <= curAgg.endDate+duration({days:10})
WITH ba.accNum as accountNumber,
	curAgg.startDate as StartDate,
	max(trf.transferDate) as EndDate,
	duration.inDays(curAgg.startDate,max(trf.transferDate)).days as NumDays,
	curAgg.numDeposits as NumDeposits,
	curAgg.totDeposits as TotalDeposits,
	count(trf.amount) as NumWithdrawals,
	sum(trf.amount) as TotalWithdrawals,
	abs(sum(trf.amount))/curAgg.totDeposits as pctWithdrawal
WHERE pctWithdrawal > 0.75 AND pctWithdrawal <= 1.0

MATCH p = (ah:AccHolder)-[:HAS_BANKACCOUNT]->(ba:BankAccount)-[:SEND]->(:BankTransfer)-[:SEND]->(:BankAccount)
WHERE ba.accNum = accountNumber
RETURN p