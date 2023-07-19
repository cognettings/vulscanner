from cfn_tools.yaml_loader import (
    construct_mapping,
    multi_constructor,
    TAG_MAP,
)
from custom_parsers.types import (
    ListToken,
)
import yaml


class BasicLoader(  # pylint: disable=too-many-ancestors
    yaml.SafeLoader,
):
    pass


class Loader(  # pylint: disable=too-many-ancestors
    yaml.SafeLoader,
):
    pass


def overloaded_construct_mapping(
    self: yaml.Loader,
    node: yaml.Node,
    deep: bool = False,
) -> dict:
    mapping = dict(construct_mapping(self, node, deep=deep))
    mapping["__column__"] = node.start_mark.column
    mapping["__line__"] = node.start_mark.line + 1
    return mapping


def overloaded_construct_sequence(
    self: yaml.Loader,
    node: yaml.Node,
    deep: bool = False,
) -> ListToken:
    return ListToken(
        value=[
            self.construct_object(child, deep=deep) for child in node.value
        ],
        column=node.start_mark.column,
        line=node.start_mark.line,
    )


def overloaded_construct_yaml_timestamp(
    self: yaml.Loader,
    node: yaml.ScalarNode,
) -> str:
    result: str = self.construct_yaml_timestamp(node).isoformat()
    return result


def overloaded_multi_constructor(
    loader: yaml.Loader,
    tag_suffix: str,
    node: yaml.Node,
) -> dict:
    mapping = dict(multi_constructor(loader, tag_suffix, node))
    mapping["__column__"] = node.start_mark.column
    mapping["__line__"] = node.start_mark.line + 1
    return mapping


def load_as_yaml(
    content: str,
    *,
    loader_cls: type[yaml.SafeLoader] = BasicLoader,
) -> dict:
    try:
        loader = loader_cls(content)
        try:
            if loader.check_data():
                return loader.get_data()
            return {}
        finally:
            loader.dispose()
    except yaml.error.YAMLError:
        return {}


BasicLoader.add_constructor(
    "tag:yaml.org,2002:timestamp",
    overloaded_construct_yaml_timestamp,
)
BasicLoader.add_constructor(TAG_MAP, construct_mapping)
BasicLoader.add_multi_constructor("!", multi_constructor)

Loader.add_constructor(
    "tag:yaml.org,2002:timestamp",
    overloaded_construct_yaml_timestamp,
)
Loader.add_constructor(TAG_MAP, overloaded_construct_mapping)
Loader.add_constructor("tag:yaml.org,2002:seq", overloaded_construct_sequence)
Loader.add_multi_constructor("!", overloaded_multi_constructor)
