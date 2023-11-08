/*
Implementing hamming distance extension for PSQL.

In Postgres:

CREATE FUNCTION HAMMING_DISTANCE(bytea, bytea) RETURNS integer
  	AS 'hamming.so', 'HAMMING_DISTANCE'
  	LANGUAGE C STRICT;
*/


// require postgresql-contrib package on AUR
#include "postgres.h"
#include "fmgr.h"

#ifdef PG_MODULE_MAGIC
PG_MODULE_MAGIC;
#endif

PG_FUNCTION_INFO_V1(HAMMING_DISTANCE);

Datum HAMMING_DISTANCE(PG_FUNCTION_ARGS)
{
	bytea* data1 = PG_GETARG_BYTEA_P(0);
	bytea* data2 = PG_GETARG_BYTEA_P(1);
	int32 dist = 0;
	int32 index = 0;
	char xor;
	char* st1 = (char*)data1;
	char* st2 = (char*)data2;

	// TODO: Maybe iterate to num_bytes, with int32 num_bytes = VARSIZE(data1) - VARHDRSZ;?
	for(index=0; index < 512; ++index) { 
		// Unroll loop internally
		xor = st1[index] ^ st2[index];
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
		dist += (xor&0x1); xor = xor >> 1;
	}

    PG_RETURN_INT32(dist);
}
