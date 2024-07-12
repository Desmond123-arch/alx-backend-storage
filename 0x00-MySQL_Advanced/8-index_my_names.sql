-- Create the index idx_name_first on the 
-- table names and the first letter of the name
DROP INDEX idx_name_first ON names;
CREATE INDEX idx_name_first ON names (LEFT(name, 1));
