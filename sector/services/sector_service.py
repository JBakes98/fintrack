from dataclasses import dataclass
import requests
from sector.models import Sector


@dataclass
class SectorDto:
    name: str


class SectorService:
    def create_sector_Dto(self, dto):
        payload = self._prepare_sector_payload(dto)

        try:
            print("Payload: {}".format(payload))
            response = requests.post("192.168.1.97:1111/api/v1/sector/list/", json=payload)
            response.raise_for_status()
        except requests.RequestException:
            print('SectorService Create failure')

        Sector.objects.create(
            name=dto.name,
        )

    @staticmethod
    def _prepare_sector_payload(dto):
        # Returns the Dto in JSON format
        print('Creating payload')
        return {
            'name': dto.name,
        }