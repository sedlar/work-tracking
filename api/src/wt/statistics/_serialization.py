from wt.common.serializers import remove_nones
from wt.common.serializers import serialize_money
from wt.statistics._obj import Statistics


class StatisticsSerializer:
    @staticmethod
    def serialize_statistics(statistics: Statistics) -> dict:
        return remove_nones(
            {
                "progress": statistics.progress,
                "overall_progress": statistics.overall_progress,
                "estimated_duration": statistics.estimated_duration,
                "estimated_cost": serialize_money(statistics.estimated_cost),
                "burned_duration": statistics.burned_duration,
                "burned_cost": serialize_money(statistics.burned_cost),
                "burned_expenditures_cost": serialize_money(statistics.burned_expenditures_cost),
            }
        )
