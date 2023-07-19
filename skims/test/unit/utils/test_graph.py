from model.graph import (
    Graph,
)
import pytest
from utils import (
    graph as g,
)


@pytest.mark.skims_test_group("unittesting")
def test_all() -> None:
    graph = Graph()
    graph.add_node("1")
    graph.add_node("2")
    graph.add_node("3")
    graph.add_node("4")
    graph.add_node("5")
    graph.add_edge("1", "2", attr_0="b")
    graph.add_edge("1", "3", attr_0="a")
    graph.add_edge("2", "6", attr_0="b")
    graph.add_edge("3", "4", attr_0="b")
    graph.add_edge("4", "5", attr_1="a")

    # 1
    # -b-> 2
    #      -b-> 6
    # -a-> 3
    #      -b-> 4
    #           -a-> 5

    assert g.adj(graph, "1", depth=-1) == ("2", "3", "6", "4", "5")
    assert g.adj(graph, "1", depth=-1, attr_0="a") == ("3",)
    assert g.adj(graph, "1", depth=-1, attr_0="b") == ("2", "6")
    assert not g.adj(graph, "1", depth=+0)
    assert g.adj(graph, "1", depth=+1) == ("2", "3")
    assert g.adj(graph, "1", depth=+1, attr_0="a") == ("3",)
    assert g.adj(graph, "1", depth=+1, attr_0="b") == ("2",)
    assert not g.adj(graph, "1", depth=+1, attr_1="b")

    assert g.pred(graph, "5", depth=-1) == ("4", "3", "1")
    assert not g.pred(graph, "5", depth=-1, attr_0="a")
    assert g.pred(graph, "5", depth=-1, attr_1="a") == ("4",)
    assert not g.pred(graph, "5", depth=-1, attr_0="b")
    assert not g.pred(graph, "5", depth=+0)
    assert g.pred(graph, "5", depth=+1) == ("4",)
    assert not g.pred(graph, "5", depth=+1, attr_0="a")
    assert g.pred(graph, "5", depth=+1, attr_1="a") == ("4",)
    assert not g.pred(graph, "5", depth=+1, attr_0="b")
    assert g.pred(graph, "5", depth=+2) == ("4", "3")


@pytest.mark.skims_test_group("unittesting")
def test_cycles() -> None:
    graph = Graph()
    graph.add_node("1")
    graph.add_node("2")
    graph.add_edge("1", "2")
    graph.add_edge("2", "1")

    assert g.adj(graph, "1", depth=-1) == ("2", "1")


@pytest.mark.skims_test_group("unittesting")
def test_branches_adj() -> None:
    graph = Graph()
    graph.add_edge("1", "2", label_ast="AST", label_index="0")
    graph.add_edge("1", "3", label_ast="AST", label_index="1")
    graph.add_edge("2", "3", label_ast="AST", label_index="0")
    graph.add_edge("3", "5", label_cfg="CFG", label_index="1")
    graph.add_edge("5", "6", label_cfg="CFG", label_index="1")

    graph.add_edge("1", "4", label_cfg="CFG", label_ast="AST", label_index="2")

    assert g.adj_ast(graph, "1") == ("2", "3", "4")
    assert g.adj_cfg(graph, "1") == ("4",)

    assert g.adj_ast(graph, "1", strict=True) == ("2", "3")
    assert g.adj_cfg(graph, "3", strict=True, depth=-1) == ("5", "6")
