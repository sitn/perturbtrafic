from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text,
)

from geoalchemy2 import Geometry
from sqlalchemy import func

from .meta import Base


class EvenementLigne(Base):
    __tablename__ = 'evenement_ligne'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_evenement = Column(BigInteger)
    geometry = Column(Geometry('LINESTRING'))

    def set_json_geometry(self, geojson, srid):
        self.geometry = func.public.ST_SetSRID(func.public.ST_GeomFromGeoJSON(geojson), srid)

    def set_text_geometry(self, text, srid):
        self.geometry = func.public.ST_SetSRID(func.public.ST_GeomFromText(text), srid)


#Index('my_index', EvenementLigne.nom, unique=True, mysql_length=255)
