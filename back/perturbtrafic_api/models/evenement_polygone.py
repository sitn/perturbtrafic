from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from geoalchemy2 import Geometry
from sqlalchemy import func

from .meta import Base


class EvenementPolygone(Base):
    __tablename__ = 'evenement_polygone'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_evenement = Column(BigInteger)
    geometry = Column(Geometry('POLYGON'))

    def set_json_geometry(self, geojson, srid):
        self.geometry = func.public.ST_SetSRID(func.public.ST_GeomFromGeoJSON(geojson), srid)

    def set_geometry_collection(self, geom_collection, srid):
        self.geometry = func.public.ST_SetSRID(func.public.ST_GeomFromGeoJSON(func.public.ST_AsGeoJSON(geom_collection)), srid)

    def set_text_geometry(self, text, srid):
        self.geometry = func.public.ST_SetSRID(func.public.ST_GeomFromText(text), srid)

#Index('my_index', EvenementLigne.nom, unique=True, mysql_length=255)
