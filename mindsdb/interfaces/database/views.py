
from mindsdb.interfaces.storage import db


class ViewController:
    def add(self, name, query, integration_name, company_id=None):

        # check is name without paths
        # TODO or allow ?
        if len(name.split('.')) > 1:
            raise Exception(f'Name should be without dots: {name}')

        # name exists?
        rec = db.session.query(db.View.id).filter(db.View.name == name,
                                            db.View.company_id == company_id).first()
        if rec is not None:
            raise Exception(f'View already exists: {name}')

        integration_records = db.session.query(db.Integration).filter_by(company_id=company_id).all()

        if integration_name is not None:
            integration_id = None
            for record in integration_records:
                if record.name.lower() == integration_name.lower():
                    integration_id = record.id
                    break
            if integration_id is None:
                raise Exception(f"Can't find integration with name: {integration_name}")

        view_record = db.View(name=name, company_id=company_id, query=query)
        db.session.add(view_record)
        db.session.commit()

    def delete(self, name, company_id=None):

        rec = db.session.query(db.View).filter(db.View.name == name, db.View.company_id == company_id).first()
        if rec is None:
            raise Exception(f'db.View not found: {name}')
        db.session.delete(rec)
        db.session.commit()

    def _get_view_record_data(self, record):

        return {
            'name': record.name,
            'query': record.query
        }

    def get(self, id=None, name=None, company_id=None):
        if id is not None:
            records = db.session.query(db.View).filter_by(id=id, company_id=company_id).all()
        elif name is not None:
            records = db.session.query(db.View).filter_by(name=name, company_id=company_id).all()
        if len(records) == 0:
            raise Exception(f"Can't find view with name/id: {name}/{id}")
        elif len(records) > 1:
            raise Exception(f"There are multiple views with name/id: {name}/{id}")
        record = records[0]
        return self._get_view_record_data(record)

    def get_all(self, company_id=None):
        view_records = db.session.query(db.View).filter_by(company_id=company_id).all()
        views_dict = {}
        for record in view_records:
            views_dict[record.name] = self._get_view_record_data(record)
        return views_dict
