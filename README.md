# shares_calc

An algorithm for finding optimal conditions for buying and selling shares (according to some elementary metrics). Draws diagrams with entry and exit points. 

Implemented with `python` (`matplotlib`), `sqlite3`, `awk`.

# Using
Download csv-files from `csv/source.url` (you can change the default parameters) and copy them to the `csv/` folder. Rename the csv files: they must end with the "_in.csv" suffix. You may need to change settings at the beginning of the `run_algo.py` file. Run
```
./init_db.sh
./run_algo.py shares.db
```
and enjoy :)
![image](https://user-images.githubusercontent.com/1208782/96649019-f8e84500-1338-11eb-836e-1102204fbacb.png)
