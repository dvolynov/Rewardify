# database/crud/base.py

from sqlalchemy.exc import SQLAlchemyError


class BaseDB:

  def __init__(self, db):
    self.db = db

  def _commit_refresh(self, obj):
    try:
      self.db.commit()
      self.db.refresh(obj)
      return obj
    except SQLAlchemyError as e:
      self.db.rollback()
      print(f"DB error: {e}")
      return None

  def _get_first(self, model, **filters):
    return self.db.query(model).filter_by(**filters).first()

  def _get_all(self, model, order_by=None, **filters):
    query = self.db.query(model).filter_by(**filters)
    if order_by:
      query = query.order_by(order_by)
    return query.all()

  def _get_by_filters(self, model, **filters):
    return self.db.query(model).filter_by(**filters).first()

  def _add_if_not_exists(self, model, unique_filter: dict, create_data: dict):
    existing = self.db.query(model).filter_by(**unique_filter).first()
    if existing:
      return existing
    new_obj = model(**create_data)
    self.db.add(new_obj)
    return self._commit_refresh(new_obj)

  def _create(self, model, **kwargs):
    obj = model(**kwargs)
    self.db.add(obj)
    return self._commit_refresh(obj)

  def _get_by_id(self, model, **filters):
    return self.db.query(model).filter_by(**filters).first()

  def _delete_by_filters(self, model, **filters):
    obj = self.db.query(model).filter_by(**filters).first()
    if not obj:
      return False
    self.db.delete(obj)
    self.db.commit()
    return True

  def _update_or_create(self, model, filters: dict, update_data: dict):
    obj = self.db.query(model).filter_by(**filters).first()
    if not obj:
      obj = model(**filters, **update_data)
      self.db.add(obj)
    else:
      for key, value in update_data.items():
        setattr(obj, key, value)
    return self._commit_refresh(obj)