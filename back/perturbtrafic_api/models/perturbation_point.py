from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Text
)

from geoalchemy2 import Geometry
from sqlalchemy import func


from .meta import Base

import json

class PerturbationPoint(Base):
    __tablename__ = 'perturbation_point'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_perturbation = Column(BigInteger)
    geometry = Column(Geometry('POINT'))

    def set_json_geometry(self, geojson, srid):
        self.geometry = func.public.ST_SetSRID(func.public.ST_GeomFromGeoJSON(geojson), srid)

    def set_text_geometry(self, text, srid):
        self.geometry = func.public.ST_SetSRID(func.public.ST_GeomFromText(text), srid)

#Index('my_index', PerturbationPoint.nom, unique=True, mysql_length=255)
