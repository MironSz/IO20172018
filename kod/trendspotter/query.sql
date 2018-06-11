SELECT w.word, COUNT(woc.id) as uses
FROM crawler_word as w 
	LEFT JOIN crawler_wordoccurence as woc ON w.id == woc.word_id 
WHERE LENGTH(w.word) > 3 
GROUP BY w.id 
ORDER BY uses 
DESC LIMIT 30;
