class Domains:

    GET_UNVISITED_DOMAINS_SQL = """
        SELECT id, domain
        FROM Domains
        WHERE visited = 0;
    """

    @staticmethod
    def get_all_unvisisted(conn):
        cursor = conn.cursor()
        result = cursor.execute(GET_UNVISITED_DOMAINS_SQL)
        return result.fetchmany()
