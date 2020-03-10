DBFILE="shares.db"
rm -f "$DBFILE"
sqlite3 "$DBFILE" ".read dbscript.sql"

rm -f "csv/*out.csv" 2> /dev/null

for f in csv/*.csv; do
    echo "Format file:" $f
    ./format_csv.sh $f > "$f.out"
done

for f in csv/*.csv.out; do
    echo "Load file:" $f
    sqlite3 "$DBFILE" ".mode csv" ".separator ;" ".import '$f' Quotation"
done

echo "Inserted records:" $(sqlite3 "$DBFILE" "SELECT COUNT(*) FROM Quotation")
