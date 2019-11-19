from sqlalchemy import (
    Column,
    Index,
    BigInteger,
    Float,
    Numeric,
    Text,
    Boolean,
    DateTime
)

from .meta import Base

from geoalchemy2 import Geometry
from sqlalchemy import func

class Deviation(Base):
    __tablename__ = 'deviation'
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    id_perturbation = Column(BigInteger)
    geometry = Column(BigInteger)

    def set_json_geometry(self, geojson, srid):
        self.geometry = func.public.ST_SetSRID(func.public.ST_GeomFromGeoJSON(geojson), srid)

    def format(self):
        return {
            'id': self.id,
            'id_perturbation': self.id_perturbation,
            'geometry': func.public.ST_GeomAsGeoJSON(self.geometry)
        }



#Index('my_index', Deviation.nom, unique=True, mysql_length=255)
