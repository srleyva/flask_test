from api.databases import db


class AccountSourceTree:
    """Loads an account source tree from the database.
    """

    SOURCE_TREE_SQL = """
    WITH RECURSIVE source_tree AS (
      SELECT rds.id rds_id,
             NULL::INTEGER AS child_rds_id
      FROM report_data_sources rds
        JOIN reports r ON r.id = rds.report_id
        JOIN users u ON u.id = r.user_id
        LEFT JOIN source_reports sr ON r.id = sr.report_id
      WHERE sr.id IS NULL AND u.account_id = {account_id}
      UNION
      SELECT rds.id,
             prds.id
      FROM report_data_sources prds
        JOIN source_tree t ON t.rds_id = prds.id
        LEFT JOIN source_reports sr ON sr.data_source_id = prds.data_source_id
        LEFT JOIN report_data_sources rds ON rds.report_id = sr.report_id
    )
    SELECT DISTINCT rds.report_id, cr.name report_name, rs.row_count, rs.size_on_disk, rs.min_date, rs.max_date,
           cr.edited_at, cr.edited_by_user_id, u.email edited_by_email,
           CASE WHEN cr.enabled THEN 'Available' ELSE 'Unavailable' END state,
           CASE WHEN cc.id IS NOT NULL THEN 'cc' || cc.id::VARCHAR || '_s' || s.id::VARCHAR
                WHEN c.id IS NOT NULL THEN 'c' || c.id::VARCHAR || '_s' || s.id::VARCHAR
                ELSE 'r' || r.id::VARCHAR END parent_id,
           CASE WHEN cc.id IS NOT NULL THEN 'custom_connection' WHEN c.id IS NOT NULL THEN 'connection' ELSE 'report' END source_type,
           COALESCE(c.id, cc.id, r.id) source_id, COALESCE(c.name, cc.name, r.name) source_name,
           CASE WHEN c.id IS NOT NULL OR cc.id IS NOT NULL THEN s.id END scope_id,
           CASE WHEN c.id IS NOT NULL OR cc.id IS NOT NULL THEN s.name END scope_name,
           CASE WHEN c.id IS NOT NULL OR cc.id IS NOT NULL THEN pds.row_count ELSE prs.row_count END parent_row_count,
           CASE WHEN c.id IS NOT NULL OR cc.id IS NOT NULL THEN pds.size_on_disk ELSE prs.size_on_disk END parent_size_on_disk,
           CASE WHEN c.id IS NOT NULL OR cc.id IS NOT NULL THEN pds.min_date ELSE prs.min_date END parent_min_date,
           CASE WHEN c.id IS NOT NULL OR cc.id IS NOT NULL THEN pds.max_date ELSE prs.max_date END parent_max_date,
           CASE WHEN c.id IS NOT NULL THEN c.state
                WHEN cc.id IS NOT NULL THEN cc.state
                ELSE CASE WHEN r.enabled THEN 'Available' ELSE 'Unavailable' END
                END parent_state
    FROM source_tree t
      JOIN report_data_sources rds ON (t.child_rds_id = rds.id AND t.rds_id IS NULL) OR (t.rds_id = rds.id)
      JOIN scopes s ON rds.scope_id = s.id
      LEFT JOIN connections c ON rds.data_source_id = c.data_source_id
      LEFT JOIN custom_connections cc ON rds.data_source_id = cc.data_source_id
      LEFT JOIN source_reports sr ON rds.data_source_id = sr.data_source_id
      LEFT JOIN reports r ON sr.report_id = r.id
      LEFT JOIN data_source_scope_stats pds ON ((c.data_source_id = pds.data_source_id OR cc.data_source_id = pds.data_source_id) AND s.id = pds.scope_id)
      LEFT JOIN report_stats prs ON r.id = prs.report_id
      LEFT JOIN reports cr ON rds.report_id = cr.id
      LEFT JOIN report_stats rs ON cr.id = rs.report_id
      LEFT JOIN users u ON cr.edited_by_user_id = u.id
    -- Have to order so edited conns are first so they are added to the sourcetree as such
    -- If they are not then they will appear as custom sources
    ORDER BY rds.report_id;
    """ # NOQA

    def __init__(self, account_id):
        self.account_id = account_id
        self.data = {
            "account_id": self.account_id,
            "dag": []
        }

    def refresh(self):
        """Refreshes the source tree from the database.
        """
        sql = self.SOURCE_TREE_SQL.format(account_id=self.account_id)
        result = db.engine.execute(sql)
        for row in result:
            node_id = f"r{row['report_id']}"
            node = self._find_node_(node_id)
            if node is None:
                node = {
                    "id": node_id,
                    "parents": []
                }
                self.data["dag"].append(node)

            parent_node = self._find_node_(row["parent_id"])
            if parent_node is None:
                # First time add it
                parent_node = {
                    "id": row["parent_id"],
                    "parents": []
                }
                self.data["dag"].append(parent_node)

            node["parents"].append(parent_node["id"])

    def _find_node_(self, id):
        results = list(filter(lambda node: node["id"] == id, self.data["dag"]))
        # Nodes are unique, so there should only ever be one result at most
        if len(results) > 0:
            return results[0]
