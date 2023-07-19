import aioextensions
from collections.abc import (
    Collection,
)
from opentelemetry.instrumentation.instrumentor import (  # type: ignore
    BaseInstrumentor,
)
from opentelemetry.instrumentation.utils import (
    unwrap,
)
from opentelemetry.trace import (
    get_tracer,
)
from telemetry.utils import (
    is_root_span,
)
from typing import (
    Any,
    Callable,
)
from wrapt import (
    wrap_function_wrapper,
)


class AioextensionsInstrumentor(BaseInstrumentor):
    """OpenTelemetry instrumentor for aioextensions"""

    def instrumentation_dependencies(self) -> Collection[str]:
        return ["aioextensions ~= 21.0"]

    def _instrument(self, **kwargs: Any) -> None:
        # pylint: disable=attribute-defined-outside-init
        self._tracer = get_tracer(__name__)

        wrap_function_wrapper(
            aioextensions,
            "collect",
            self._patched_collect,
        )
        wrap_function_wrapper(
            aioextensions,
            "in_process",
            self._patched_in_executor,
        )
        wrap_function_wrapper(
            aioextensions,
            "in_thread",
            self._patched_in_executor,
        )

    def _uninstrument(self, **kwargs: Any) -> None:
        unwrap(aioextensions, "collect")
        unwrap(aioextensions, "in_process")
        unwrap(aioextensions, "in_thread")

    async def _patched_collect(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        name = f"{original_func.__module__}.{original_func.__qualname__}"
        with self._tracer.start_as_current_span(name):
            return await original_func(*args, **kwargs)

    async def _patched_in_executor(
        self,
        original_func: Callable[..., Any],
        _instance: Any,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Any:
        if is_root_span():
            return await original_func(*args, **kwargs)

        name = f"{original_func.__module__}.{original_func.__qualname__}"
        with self._tracer.start_as_current_span(name) as trace:
            function_name = f"{args[0].__module__}.{args[0].__qualname__}"
            trace.set_attribute("function", function_name)
            return await original_func(*args, **kwargs)
