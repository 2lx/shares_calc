DBFILE="shares.db"
rm -f "$DBFILE"
sqlite3 "$DBFILE" ".read dbscript.sql"

for f in *out.csv; do
    echo "Process file:" $f
    sqlite3 "$DBFILE" ".mode csv" ".separator ;" ".import $f Quotation"
done

echo "Inserted records:" $(sqlite3 "$DBFILE" "SELECT COUNT(*) FROM Quotation")
