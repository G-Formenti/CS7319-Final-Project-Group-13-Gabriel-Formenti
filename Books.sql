BEGIN TRANSACTION;

DROP TABLE IF EXISTS Books;

CREATE TABLE Books (
  Book_Title VARCHAR(256),
  Author VARCHAR(256) NOT NULL,
  Pages_Read DECIMAL NOT NULL,      
  Pages_Book DECIMAL NOT NULL,
  Date_Inserted DATE NOT NULL, 
  Progress DECIMAL(10,3)
);

CREATE OR REPLACE FUNCTION Book_Percentage_Update()
RETURNS TRIGGER AS $$
BEGIN
    NEW.Progress := (NEW.Pages_Read / NEW.Pages_Book) * 100;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Book_Percentage
BEFORE INSERT OR UPDATE
ON Books
FOR EACH ROW
EXECUTE FUNCTION Book_Percentage_Update();

CREATE OR REPLACE FUNCTION Number_of_Pages_Exceeded()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Pages_Read > NEW.Pages_Book THEN
        RAISE EXCEPTION 'Pages Read Exceeds Pages in Book';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER Check_Pages_Insert
BEFORE INSERT ON Books
FOR EACH ROW
EXECUTE FUNCTION Number_of_Pages_Exceeded();

CREATE TRIGGER Check_Pages_Update
BEFORE UPDATE ON Books
FOR EACH ROW
EXECUTE FUNCTION Number_of_Pages_Exceeded();

COMMIT TRANSACTION;
