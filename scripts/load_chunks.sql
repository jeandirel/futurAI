\copy chunks (id, source, position, text, embedding) FROM '/tmp/chunks.tsv' WITH (FORMAT csv, DELIMITER E'\t', QUOTE '"', ESCAPE '"');
