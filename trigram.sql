CREATE OR REPLACE FUNCTION public.generatetrigram(string text)
 RETURNS TABLE(trigram text)
 LANGUAGE plpgsql
AS $function$
	declare top int;
	begin
		top = case
			when length(string) > 2 then length(string) - 2
			else 0
		end;
		return query with N16 as 
		(
			select V.v from 
			(
				values
					(0),(0),(0),(0),(0),(0),(0),(0),
					(0),(0),(0),(0),(0),(0),(0),(0)
			) as V (v)
		),
		Nums as
		(
			select cast(row_number() over (order by A.v) as int) n
			from N16 as A
			cross join N16 as B
		),
		Trigrams as 
		(
			select substring(string, N.n, 3) trigram from Nums as N order by N.n limit top
		) 	
		
		select distinct T.trigram
			from Trigrams as T 
--			where T.trigram collate Latin1_General_BIN2 
			where T.trigram not like '%[^A-Z0-9a-z]%';
	end;
$function$
;

create extension pg_trgm;

create table if not exists Trigrams as (
  select
    id, trgm.trgm as trigram
  from
    bstrings20,
    lateral unnest(show_trgm(bstrings20.phash)) as trgm
  where 
    length(trim(trgm)) = 3;
);

-- create and index view over trigrams table to make it fast and easy to find 
-- which trigrams are the most and least common in the data
create materialized view trigramCountView as 
  select t.trigram, count(*) as cnt
  from trigrams t group by t.trigram;

create unique index trgm_ind on trigramCountView(trigram);
cluster trigramCountView using trgm_ind;

-- most selective trigram for search string
-- always return a row (NULL if no trigrams found)

create or replace function getBestTrigrams(string text)
returns table(trgm1 text, trgm2 text, trgm3 text)
language plpgsql
as $function$
	begin
		return query
		select 
			max(case when bt.n = 1 then bt.trigram end) as trgm1,
			max(case when bt.n = 2 then bt.trigram end) as trgm2,
			max(case when bt.n = 3 then bt.trigram end) as trgm3
		from (
			SELECT 
				cast(row_number() over (order by tcv.cnt asc) as int) n,
				gt.trigram as trigram
			from
				-- TODO: wrap unnest in a function
				trigramCountView tcv
					join (select * from unnest(show_trgm(string)) as trigram where length(trim(trigram)) = 3) gt 
					on gt.trigram = tcv.trigram order by tcv.cnt asc 
		) bt;
	end;
$function$;

-- retrieve from trigram tables all rows that match values retrived from getBestTrigram()
create or replace function getMatchingTrigramId(trgm1 text, trgm2 text, trgm3 text)
returns table (id integer)
language plpgsql 
as $function$
	begin
		if trgm1 is not null then
			if trgm2 is not null then
				if trgm3 is not null then
					-- 3 available trigrams
					return query 
						select id from trigrams t1 where t1.trigram = trgm1
						intersect 
						select id from trigrams t2 where t2.trigram = trgm2
						intersect
						select id from trigrams t3 where t3.trigram = trgm3;
				end if;
				-- 2 available trigrams
					return query 
						select id from trigrams t1 where t1.trigram = trgm1
						intersect 
						select id from trigrams t2 where t2.trigram = trgm2;
		
			end if;
			-- 1 available trigram
			return query
				select id from trigrams t1 where t1.trigram = trm1;
		end if;
	end;
$function$;

-- search implementation
create or replace function trigramSearch(searchterm text) 
returns table (string text)
language plpgsql
as $function$
	
	begin
		
		return query 
			select r.string from getbesttrigrams(searchterm) gbt,
			lateral (
				-- trigram search
				select e.id, e.phash from getmatchingtrigramid() as mid
				join bstrings20 as e on e.id = mid.id
				where gbt.trgm1 is not null and e.phash like searchterm
				
				union all
				
				-- non-trigram search
				select e.id, e.phash from bstrings20 as e where
					-- no trigram found
					gbt.trgm1 is null and e.phash like searchterm
			) as r;
		
	end;
	

$function$