-- Q4 filtro selectivo: una semana de enero de 2026 (candidato a predicate pushdown).
SELECT taxi, count(*) AS viajes, sum(total_amount) AS ingresos
FROM {SRC}
WHERE pickup >= TIMESTAMP '2026-01-10' AND pickup < TIMESTAMP '2026-01-17'
GROUP BY taxi;
