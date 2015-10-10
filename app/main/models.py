from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import text
from flask import abort


class Dataset(db.Model):
    __tablename__ = 'datasets'

    id = db.Column(db.Integer, primary_key=True)
    datatype = db.Column(db.String(15), nullable=False)
    model = db.Column(db.String(15), nullable=False)
    modelname = db.Column(db.String(50), nullable=False)
    scenario = db.Column(db.String(15), nullable=False)
    resolution = db.Column(db.String(15), nullable=False)
    temperatures = db.relationship('Temperature', backref='datasets')

    @hybrid_property
    def type(self):
        return self.datatype.lower().capitalize()


class Temperature(db.Model):
    __tablename__ = 'temperatures'

    id = db.Column(db.Integer, primary_key=True)
    dataset_id = db.Column(db.Integer, db.ForeignKey('datasets.id'))
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'))
    year = db.Column(db.Integer, nullable=False)
    january = db.Column(db.Float, nullable=False)
    february = db.Column(db.Float, nullable=False)
    march = db.Column(db.Float, nullable=False)
    april = db.Column(db.Float, nullable=False)
    may = db.Column(db.Float, nullable=False)
    june = db.Column(db.Float, nullable=False)
    july = db.Column(db.Float, nullable=False)
    august = db.Column(db.Float, nullable=False)
    september = db.Column(db.Float, nullable=False)
    october = db.Column(db.Float, nullable=False)
    november = db.Column(db.Float, nullable=False)
    december = db.Column(db.Float, nullable=False)
    updated = db.Column(db.DateTime, nullable=True)


class DB:
    @classmethod
    def getCommunity(cls, id):
        cmd = """
            SELECT id, name, latitude, longitude, northing, easting
            FROM new_communities
            WHERE id=:id;
            """
        result = db.engine.execute(text(cmd), id=id).fetchone()
        return result or abort(500)

    @classmethod
    def getCommunities(cls):
        cmd = """
            SELECT id, name
            FROM new_communities
            ORDER BY name ASC;
            """
        result = db.engine.execute(text(cmd), id=id).fetchall()
        return result or abort(500)

    @classmethod
    def getDatasets(cls):
        cmd = """
            SELECT DISTINCT ON (
                doc->'model',
                doc->'datatype',
                doc->'resolution',
                doc->'modelname',
                doc->'scenario'
            )
                doc->'model' AS model,
                doc->'datatype' AS datatype,
                doc->'resolution' AS resolution,
                doc->'modelname' AS modelname,
                doc->'scenario' AS scenario
            FROM new_communities c,
                jsonb_array_elements(c.data)
                WITH ORDINALITY t1(doc, rn)
            ORDER BY datatype ASC, modelname ASC, scenario ASC;
            """
        result = db.engine.execute(text(cmd), id=id).fetchall()
        return result or abort(500)

# WITH x AS (
#     SELECT name, jsonb_array_elements(data) AS data
#     FROM new_communities
#     WHERE name='Anchorage')
# SELECT d.key::INTEGER AS year, d.value AS temperatures
# FROM x, jsonb_each(data) d
# WHERE data->>'model'='CRU'
# AND d.key NOT IN ('model', 'datatype', 'scenario', 'modelname', 'resolution');
