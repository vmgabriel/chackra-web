import enum
import pydantic


class MeasureUnitType(enum.StrEnum):
    KG = "KG"
    LB = "lb"
    L = "L"
    ML = "ML"
    Gr = "gr"
    UNIT = "UNIT"
    SPOON = "SPOON"

    def is_weight(self) -> bool:
        return self in [MeasureUnitType.KG, MeasureUnitType.LB, MeasureUnitType.Gr]

    def is_volume(self) -> bool:
        return self in [MeasureUnitType.L, MeasureUnitType.ML]

    def is_the_same_measure_unit(self, other: "MeasureUnitType") -> bool:
        if self == other:
            return True
        return (self.is_weight() and other.is_weight()) or (self.is_volume() and other.is_volume())


DEFAULT_MEASURE_UNIT_WEIGHT = MeasureUnitType.Gr
DEFAULT_MEASURE_UNIT_VOLUME = MeasureUnitType.L
DEFAULT_MEASURE_UNITS = MeasureUnitType.UNIT


class QuantityConverter:
    @staticmethod
    def lb_to_gr(lb: float) -> float:
        return lb * 453.592

    @staticmethod
    def kg_to_gr(kg: float) -> float:
        return kg * 1000

    @staticmethod
    def ml_to_l(ml: float) -> float:
        return ml / 1000


class Quantity(pydantic.BaseModel):
    measure_unit: MeasureUnitType
    value: float

    def __str__(self) -> str:
        return f"{self.value} {self.measure_unit.value}"

    def __add__(self, other: "Quantity") -> "Quantity":
        if self.measure_unit == other.measure_unit:
            return Quantity(measure_unit=self.measure_unit, value=self.value + other.value)
        if not self.measure_unit.is_the_same_measure_unit(other.measure_unit):
            raise ValueError("Los unidades de medida no coinciden")

        current = self.to_default_unit()
        other = other.to_default_unit()
        return Quantity(measure_unit=current.measure_unit, value=current.value + other.value)

    def __sub__(self, other: "Quantity") -> "Quantity":
        if self.measure_unit == other.measure_unit:
            return Quantity(measure_unit=self.measure_unit, value=self.value - other.value)
        if not self.measure_unit.is_the_same_measure_unit(other.measure_unit):
            raise ValueError("Los unidades de medida no coinciden")
        current = self.to_default_unit()
        other = other.to_default_unit()
        return Quantity(measure_unit=current.measure_unit, value=current.value - other.value)

    def __mul__(self, other: "Quantity") -> "Quantity":
        if self.measure_unit == other.measure_unit:
            return Quantity(measure_unit=self.measure_unit, value=self.value * other.value)
        if not self.measure_unit.is_the_same_measure_unit(other.measure_unit):
            raise ValueError("Los unidades de medida no coinciden")
        current = self.to_default_unit()
        other = other.to_default_unit()
        return Quantity(measure_unit=current.measure_unit, value=current.value * other.value)

    def __truediv__(self, other) -> "Quantity":
        if self.measure_unit == other.measure_unit:
            if other.value == 0:
                raise ZeroDivisionError("No se puede dividir entre cero")
            return Quantity(measure_unit=self.measure_unit, value=self.value / other.value)
        if not self.measure_unit.is_the_same_measure_unit(other.measure_unit):
            raise ValueError("Los unidades de medida no coinciden")
        current = self.to_default_unit()
        other = other.to_default_unit()
        if other.value == 0:
            raise ZeroDivisionError("No se puede dividir entre cero")
        return Quantity(measure_unit=current.measure_unit, value=current.value / other.value)


    def __neg__(self) -> "Quantity":
        return Quantity(measure_unit=self.measure_unit, value=-self.value)


    def to_default_unit(self) -> "Quantity":
        if self.measure_unit.is_weight() and self.measure_unit != DEFAULT_MEASURE_UNIT_WEIGHT:
            if self.measure_unit == MeasureUnitType.KG:
                return Quantity(measure_unit=MeasureUnitType.Gr, value=QuantityConverter.kg_to_gr(self.value))
            if self.measure_unit == MeasureUnitType.LB:
                return Quantity(measure_unit=MeasureUnitType.Gr, value=QuantityConverter.lb_to_gr(self.value))
            return self
        if self.measure_unit.is_volume() and self.measure_unit != DEFAULT_MEASURE_UNIT_VOLUME:
            return Quantity(measure_unit=MeasureUnitType.L, value=QuantityConverter.ml_to_l(self.value))
        return self
