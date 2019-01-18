from typing import List

from wt.common.serializers import serialize_money, deserialize_money
from wt.costs.expenditures._obj import (
    BoundExpenditure,
    Expenditure,
    ExpenditureStatus,
    ExpenditureType,
)
from wt.fields.files import FilesSerializer, FilesDeserializer
from wt.common.serializers import remove_nones


class ExpendituresSerializer:
    def __init__(self, files_serializer: FilesSerializer):
        self._files_serializer = files_serializer

    def serialize_expenditure(self, expenditure: BoundExpenditure):
        return remove_nones(
            {
                "id": expenditure.simple_id.simple_id,
                "name": expenditure.name,
                "description": expenditure.description,
                "date_opened": expenditure.date_opened,
                "date_closed": expenditure.date_closed,
                "deadline": expenditure.deadline,
                "cost": serialize_money(expenditure.cost),
                "status": expenditure.status.value,
                "type": expenditure.type.value,
                "files": self._files_serializer.serialize_files(expenditure.files)
            }
        )

    def serialize_expenditures(self, expenditures: List[BoundExpenditure]):
        return [
            self.serialize_expenditure(expenditure)
            for expenditure
            in expenditures
        ]


class ExpendituresDeserializer:
    def __init__(self, files_deserializer: FilesDeserializer):
        self._files_deserializer = files_deserializer

    def deserialize_expenditure(self, expenditure) -> Expenditure:
        return Expenditure(
            name=expenditure["name"],
            description=expenditure["description"],
            date_opened=expenditure["date_opened"],
            date_closed=expenditure.get("date_closed"),
            deadline=expenditure.get("deadline"),
            cost=deserialize_money(expenditure["cost"]),
            status=ExpenditureStatus(expenditure["status"]),
            type_=ExpenditureType(expenditure["type"]),
            files=self._files_deserializer.deserialize_files(expenditure["files"]),
        )
