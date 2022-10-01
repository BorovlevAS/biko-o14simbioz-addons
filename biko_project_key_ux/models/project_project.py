from odoo.addons.project_key.models.project_project import Project

class BikoProject(Project):
    
    def write(self, values):
        update_key = False
        amount_of_dashs = 0

        if "key" in values:
            key = values["key"]
            update_key = self.key != key
            amount_of_dashs = self.key.count('-') if self.key else 0

        res = super(Project, self).write(values)

        if update_key:
            # Here we don't expect to have more than one record
            # because we can not have multiple projects with the same KEY.
            self.update_sequence()
            self._update_task_keys(amount_of_dashs)

        return res

    def _update_task_keys(self, amount_of_dashs = 0):
        """
        This method will update task keys of the current project.
        """
        self.ensure_one()
        self.flush()
        reindex_query = """
        UPDATE project_task
        SET key = x.key
        FROM (
          SELECT t.id, p.key || '-' || split_part(t.key, '-', %s) AS key
          FROM project_task t
          INNER JOIN project_project p ON t.project_id = p.id
          WHERE t.project_id = %s
        ) AS x
        WHERE project_task.id = x.id;
        """

        self.env.cr.execute(reindex_query, (amount_of_dashs + 2, self.id,))
        self.env["project.task"].invalidate_cache(["key"], self.task_ids.ids)