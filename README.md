[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
# py-typescript-generator

`py-typescript-generator` is a tool to create TypeScript type definitions from Python classes. 

> Note: Currently, only Python dataclasses are supported, but it's possible to extend this to other sources, like attrs classes or SqlAlchemy models.

This project is heavily inspired by the [typescript-generator](https://github.com/vojtechhabarta/typescript-generator) project by 
Vojtěch Habarta, a TypeScript generator for Java classes.

**Example**  
Consider the following dataclass:
```python
from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass
class DemoClass:
    my_int: int
    my_optional_string: Optional[str]
    my_list: List[str]
    my_dict: Dict[str, str]
```
For this class, the following TypeScript interface is generated:
```typescript
interface DemoClass {
    my_int: number
    my_optional_string: string | undefined
    my_list: string[]
    my_dict: { [index: string]: string }
}
```
`py-typescript-generator` supports basic Python types like `int`, `float`, `str`, `datetime` or `UUID` and collections like `List`, `Set` or `Dict`. `Optional` is also supported.

For more details on type mapping, see [Type Mapping](##Type Mapping).

## Usage
### Installation
You can install `py-typescript-generator` via `pip`, currently only from Github:
```shell
pip install git+https://github.com/Latios96/py-typescript-generator.git@v0.1.3
```
or if you are using poetry:
```shell
poetry add git+ssh://git@github.com:Latios96/py-typescript-generator.git#v0.1.3
```
### Invocation
`py-typescript-generator` is invoked by a custom Python Script, which is placed in your project. Note that `py-typescript-generator` needs to import your classes, so make sure all your imported dependencies are available when generating your types.

To generate your TypeScript types, pass a list of your classes: 

```python
from dataclasses import dataclass
from py_typescript_generator import TypeGenerationPipelineBuilder

@dataclass
class MyExampleClass:
    value: int

if __name__ == "__main__":
    TypeGenerationPipelineBuilder() \
        .for_types([MyExampleClass]) \ 
        .to_file("demo.ts") \
        .build() \
        .run()
```
Types used as field types are automatically discovered and don't have to be passed in manually.

Now just execute the script you created and your TypeScript types are generated to the file path you configured.

### Advanced features
#### Type overrides
You can override how a certain type is mapped in TypeScript. This is usefull if a type is represented diffenent in JSON as in your Python dataclass. For example, a `datetime` object by default is mapped to a `string`, but you might return them in JSON as UNIX timestamps. In this case, you override the `datetime` mapping to `int`:  
```python
TypeGenerationPipelineBuilder() \
    .for_types([MyExampleClass]) \ 
    .with_type_overrides({datetime: int})
    .to_file("demo.ts") \
    .build() \
    .run()
```
#### CamelCase conversion
In Python, fields are usually declared in snake_case. However, sometimes they are converted to camelCase in JSON, since this is the convention in JavaScript / TypeScript. `py-typescript-generator` also supports camelCase conversion for fields:
```python
TypeGenerationPipelineBuilder() \
    .for_types([MyExampleClass]) \ 
    .convert_field_names_to_camel_case()
    .to_file("demo.ts") \
    .build() \
    .run()
```


## Type Mapping
Python classes and Enums are supported. Python classes are mapped as TypeScript interfaces, Enums are mapped as TypeScript enums.
> Note: only str and int values are supported for Enums.

Currently, only Python dataclasses can be analyzed and mapped. However, this can be extended.

The following Python types are automatically recognized and mapped as following:

| Python type         | Typescript type                                        |
|---------------------|--------------------------------------------------------|
| int                 | number                                                 |
| float               | number                                                 |
| str                 | str                                                    |
| bytes               | str                                                    |
| bool                | boolean                                                |
| datetime            | str                                                    |
| UUID                | str                                                    |
| Optional[T]         | T \| undefined         |
| List[T]             | T[]                                                    |
| Set[T]              | T[]                     |
| FrozenSet[T]        | T[]                     |
| OrderedSet[T]       | T[]                     |
| Dict[str, T]        | { [index: string]: T } (Fails, if key type is not str) |
| DefaultDict[str, T] | { [index: string]: T } (Fails, if key type is not str) |
