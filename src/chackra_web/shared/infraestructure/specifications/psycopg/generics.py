from chackra_web.shared.domain.model.specifications import (
    specifications as shared_specifications,
    generics as shared_generics
)


class PsycopgAndSpecification(shared_specifications.AndSpecification):
    def to_sql(self) -> tuple[str, tuple[str, ...]]:
        query1, params1 = self.specification_1.to_sql()
        query2, params2 = self.specification_2.to_sql()
        return f"({query1} AND {query2})", params1 + params2


class PsycopgOrSpecification(shared_specifications.OrSpecification):
    def to_sql(self) -> tuple[str, tuple[str, ...]]:
        query1, params1 = self.specification_1.to_sql()
        query2, params2 = self.specification_2.to_sql()
        return f"({query1} OR {query2})", params1 + params2


class PsycopgIdEqualSpecification(shared_generics.IdEqualSpecification):
    def to_sql(self) -> tuple[str, tuple[str, ...]]:
        return f"{self.ATTRIBUTE} = %s", (self.id_value.value,)


class PsycopgActiveEqualSpecification(shared_generics.ActiveEqualSpecification):
    def to_sql(self) -> tuple[str, tuple[str, ...]]:
        return f"{self.ATTRIBUTE} = %s", (str(self.active_status).lower(),)