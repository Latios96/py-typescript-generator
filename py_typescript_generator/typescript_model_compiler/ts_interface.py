from py_typescript_generator.typescript_model_compiler.ts_type import TsType


class TsInterface(TsType):
    def __str__(self):
        return f"TsInterface(name='{self.name}', is_optional='{self.is_optional}')"
