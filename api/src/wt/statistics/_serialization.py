from wt.statistics._obj import Statistics
from wt.common.serializers import serialize_money


class StatisticsSerializer:
    @staticmethod
    def serialize_statistics(statistics: Statistics) -> dict:
        return {
            "progress": statistics.progress,
            "estimated_duration": statistics.estimated_duration,
            "estimated_cost": serialize_money(statistics.estimated_cost),
            "burned_duration": statistics.burned_duration,
            "burned_cost": serialize_money(statistics.burned_cost),
            "burned_expenditures_cost": serialize_money(statistics.burned_expenditures_cost),
        }
