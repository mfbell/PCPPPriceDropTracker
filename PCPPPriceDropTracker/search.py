"""Search Tools."""

import re

from tools import main


__all__ = ["SearchEngine"]

class SearchEngine():
    """Main related search functions.

    db_handler - DBHandler.Handler
    output_columns - A list of the column IDs of result data to send to outputs.
    search_string - A tk.StringVar of the user's search input.
    data_outputs - A list of functions to send result data to.
    search_filters - A list of functions which output a search filter's
        built SQL string other than values which should be given secondly in
        a list. e.g. "Active = ?", [1]

    push(results) - Call all data_outputs with results
        results is entended to be in a database select query format.
    update() - Run a search and push.
        Use to trigger updates
    search() - Search function, returns results

    """

    def __init__(self, db_handler, output_columns, search_string, data_outputs = [], search_filters = []):
        """Initialization.

        db_handler - DBHandler
        output_columns - A list of the column IDs of result data to send to
            outputs.
        search_string - A tk.StringVar of the user's search input.
        data_outputs - A list of functions to send result data to.
            e.g. GUI.main.ResultsPanel.input
        search_filters - A list of functions which output a search filter's
            built SQL string other than values which should be given secondly in
            a list. e.g. "Active = ?", [1]


        """
        self.db_handler = db_handler
        self.output_columns = output_columns
        self.search_string = search_string
        self.data_outputs = data_outputs
        self.search_filters = search_filters

    def push(self, results):
        """Send data to data_outputs."""
        for output in self.data_outputs:
            output(results)

    def update(self):
        self.push(self.search())

    def search(self):
        """Magic Search(TM) /s

        Need to update to use FTS5 searching!

        """
        logger = getLogger(".".join([pdname, __name__, "SearchEngine", "search"]))
        search_string = self.search_string.get()
        non_split_char = '"'
        # more effcient way?
        words = []
        while True:
            part = re.search('(.+?)'.join([non_split_char, non_split_char]), search_string)
            if not part:
                words.extend([word.strip() for word in search_string.split()])
                break
            pre, post = part.span()
            words.extend([word.strip() for word in search_string[:pre].split()])
            words.append(part.group(1).strip())
            search_string = search_string[post + 1:]
        logger.debug("Words from string: {0}".format(words))
        results = []
        if len(words) > 6:
            results.append(("Possible search combinations exceeds SQLite expression limit. Using linear search.", "ErrorMessage"))
            logger.info("Possible search combinations exceeds SQLite expression limit. Using linear search.")
            combinations = ["%" + "%".join(word for word in words) + "%"] # Could do up to so many combinations
        elif not words:
            combinations = []
            logger.debug("No combinations created.")
        else:
            combinations = ["%" + "%".join(order) + "%" for order in list(permutations(words))]
            logger.debug("Full search can be done.")
        if combinations:
            combinations_str = "(Name LIKE {0})".format(" OR Name LIKE ".join("?" for _ in combinations))
        else:
            combinations_str = ""
        # Filters
        search_filters_string = ""
        search_filters_values = []
        for search_filter in self.search_filters:
            string, values = search_filter()
            search_filters_string = ' AND '.join([search_filters_string, string])
            search_filters_values.extend(values)
        logger.debug("Filters are: {0}".format(search_filters_string, search_filters_values))
        # Query
        join = " AND " if search_filters_string and combinations_str else ""
        results += self.query("""SELECT {0} FROM Offers
                                     JOIN Products ON Offers.ProductID = Products.ProductID
                                 WHERE {1} {2}
                                     {3}""".format(", ".join(self.output_columns),
                                                   search_filters_string,
                                                   join
                                                   combinations_str),
                              search_filters_values.extend(combinations))
        logger.debug("Search complete.")
        return results


if __name__ == '__main__':
    main(__doc__)


# Old
"""Search for offer in database and return results.

--== Behaviour ==--
Note: Any strings put into a query are not case sensitive as this part
of SQLite.

+ Smart Search +
Smart Search starts with the string in search_string. It first splits
the string and then strips each part.
    If over six words long, the possible combinations exceeds SQLite
    query expression limit. For now a linear search is done with the
    words reassembed in order joined, prefix and sufexed with wildcards.
    This may change in the future to use different orders.
If there is no words the search will now neglect to include smart search.
Now all combinations are generated from the words: This is all different
ways the words can be arranged, then joined, prefix and sufexed with
wildcards.
In the search all these are listed in the query under 'Name LIKE <str>
OR ...'. At the moment smart search is limited to Name only but I hope
to expand to other columns, however this will reduce the possible length
of searches as expressions will have to be spread over more conditions.
Example:
"Intel Core" ->
["Intel", "Core"] ->
[("Intel", "Core"), ("Core", "Intel")] ->
["%Intel%Core%", "%Core%Intel%"] ->
SQL: "...
      WHERE [<conditions> AND]
          (Name LIKE '%Intel%Core%' OR Name LIKE '%Core%Intel%')" =>
Return ...

+ Returns +
If there is no results None is returned.
If there is, results will be returned as: (Entry, Entry, ...)
Where Entries are rows in Offers (with Products data) which fit
conditions given to the SQL query.
Entries will contrain the tuple of the column data of the entry in order
which it was requested. See Behaviour->Args->columns for more info.

--== Future Updates ==--
See a doc I will create for this at some point.
    Stuff like all column smart searching, rank results by relivance eta.

"""
