from dataclasses import dataclass
from typing import Sequence

from pytheus.exceptions import UnobservableMetricException


Labels = dict[str, str]


class MetricCollector:

    def __init__(self, name: str, required_labels: Sequence[str] | None = None) -> None:
        self.name = name
        self._required_labels = set(required_labels) if required_labels else None
        # TODO: pass metric class
        self._metric = Metric(self)
        self._labeled_metrics: dict[tuple[str, ...], Metric] = {}

        # this will register to the collector


# class or function based creation ?
class Metric:

    def __init__(
        self,
        collector: MetricCollector,
        labels: Labels | None = None,
    ) -> None:
        self._collector = collector
        self._labels = labels
        self._can_observe = self._check_can_observe()

    def _check_can_observe(self) -> bool:
        if not self._collector._required_labels:
            return True

        if not self._labels:
            return False

        # TODO: labels will need better validation checks
        if len(self._labels) != len(self._collector._required_labels):
            # TODO: custom exceptions required
            return False

        # TODO: allow partial labels
        return True

    # TODO: calling labels again should keep previous labels by default
    # allowing for partial labels
    # TODO: also consider adding default labels directly on the collector as well
    def labels(self, _labels: Labels) -> 'Metric':
        if not _labels or self._collector._required_labels is None:
            return self

        add_to_collector: bool = True

        # TODO: add labels validation
        if len(_labels) != len(self._collector._required_labels):
            add_to_collector = False

        sorted_label_values = tuple(v for _, v in sorted(_labels.items()))
        # get or add to collector
        if add_to_collector:
            if sorted_label_values in self._collector._labeled_metrics:
                metric = self._collector._labeled_metrics[sorted_label_values]
            else:
                metric = self.__class__(self._collector, _labels)
                self._collector._labeled_metrics[sorted_label_values] = metric
        else:
            metric = self.__class__(self._collector, _labels)

        return metric


class Counter(Metric):

    def __init__(
        self,
        collector: MetricCollector,
        labels: Labels | None = None,
    ) -> None:
        super().__init__(collector, labels)

        # TODO: value should be threadsafe and possibly support different kinds :)
        # possibly asyncio support could be considered and also multiprocessing
        self._value = 0

    def inc(self, value: float) -> None:
        if not self._can_observe:
            raise UnobservableMetricException

        self._value += value


# this could be a class method, but might want to avoid it
def create_metric(name: str, required_labels: Sequence[str] | None = None) -> Metric:
    collector = MetricCollector(name, required_labels)
    return Metric(collector)


def create_counter(name: str, required_labels: Sequence[str] | None = None) -> Metric:
    collector = MetricCollector(name, required_labels)
    return Counter(collector)


@dataclass
class Sample:
    name: str
    labels: dict[str, str]
    value: float


# maybe just go with the typing alias
@dataclass
class Label:
    name: str
    value: str


# m = MetricCollector('name', ['bbo'])
my_metric = create_metric('name', ['bbo'])
