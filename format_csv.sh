DBFILE="shares.db"

cat "$1" | tail -n +2 | awk '
    BEGIN {
        FS = ";"

        shareCmd = "sqlite3 $DBFILE \".separator , |\" \"SELECT Abbr FROM Share ORDER BY rowid;\"";
        shareCmd |& getline shareResponse
        shareCount = split(shareResponse, shareNames, "|") - 1

        marketCmd = "sqlite3 $DBFILE \".separator , |\" \"SELECT Abbr FROM Market ORDER BY rowid;\"";
        marketCmd |& getline marketResponse
        marketCount = split(marketResponse, marketNames, "|") - 1
    };

    function formatDate(str)
    {
        return substr(str, 1, 4) "-" substr(str, 5, 2) "-" substr(str, 7, 2)
    }

    function formatTime(str)
    {
        return substr(str, 1, 2) ":" substr(str, 3, 2) ":" substr(str, 5, 2)
    }

    function getMarketId(str)
    {
        for (i = 1; i <= marketCount; i++)
            if (str == marketNames[i])
                return i;

        return 0;
    }

    function getShareId(str)
    {
        for (i = 1; i <= shareCount; i++)
            if (str == shareNames[i])
                return i;

        return 0;
    }

    {
        split($1, ids, ".");
        marketId = getMarketId(ids[1]);
        shareId = getShareId(ids[2]);

        print marketId ";"                          \
              shareId ";"                           \
              formatDate($3) " " formatTime($4) ";" \
              $5 ";" $6 ";" $7 ";" $8 ";" $9;
    }
'
