from abc import ABC, abstractmethod

CONJUNCTION = "&"

FLIP_FLOP = "%"

ARROW = "->"
BROADCASTER = "broadcaster"

HIGH_SIGNAL: int = 1
LOW_SIGNAL: int = 0


class Module(ABC):
    def __init__(self, name: str):
        self.name: str = name
        self.destination_modules: list[Module] = list()
        self.signal_to_send: dict[int, int] = {}

    def add_destination_module(self, module: "Module"):
        self.destination_modules.append(module)

    @abstractmethod
    def process_signal(self, signal: int, caller: str = "") -> int | None:
        raise NotImplementedError("method receive_signal is not implemented")

    def __eq__(self, other):
        if not isinstance(other, Module):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name})"


class EmptyModule(Module):
    def process_signal(self, signal: int, caller: str = "") -> int | None:
        return None


class ButtonModule(Module):
    def process_signal(self, signal: int, caller: str = "") -> int | None:
        return LOW_SIGNAL


class BroadcastModule(Module):
    def process_signal(self, signal: int, caller: str = "") -> int | None:
        return signal


class FlipFlopModule(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.on: bool = False

    def process_signal(self, signal: int, caller: str = "") -> int | None:
        if signal == HIGH_SIGNAL:
            return None

        result = LOW_SIGNAL if self.on else HIGH_SIGNAL
        self.on = not self.on
        return result


class ConjunctionModule(Module):
    def __init__(self, name: str):
        super().__init__(name)
        self.last_remembered: dict[str, int] = {}

    def add_caller(self, caller: str):
        self.last_remembered[caller] = LOW_SIGNAL

    def process_signal(self, signal: int, caller: str = "") -> int | None:
        self.last_remembered[caller] = signal
        if LOW_SIGNAL in self.last_remembered.values():
            return HIGH_SIGNAL
        else:
            return LOW_SIGNAL


def parse_module(line: str) -> tuple[Module, list[str]]:
    if ARROW not in line:
        raise ValueError("invalid line, missing '->'")

    name_raw, destination_modules_raw = line.split(ARROW)

    name: str = name_raw.strip()
    destination_modules: list[str] = list(
        module.strip() for module in destination_modules_raw.split(",")
    )

    if name == BROADCASTER:
        return BroadcastModule(name), destination_modules

    if name.startswith(FLIP_FLOP):
        return FlipFlopModule(name[1:]), destination_modules

    if name.startswith(CONJUNCTION):
        return ConjunctionModule(name[1:]), destination_modules

    raise ValueError("invalid line, unknown module type")


def parse_modules(file: list[str]) -> ButtonModule:
    modules: list[Module] = []
    module_name_to_module: dict[str, Module] = {}
    link_to_destination_modules: dict[str, list[str]] = {}
    for line in file:
        module, destination_modules = parse_module(line)
        modules.append(module)
        module_name_to_module[module.name] = module
        link_to_destination_modules[module.name] = destination_modules

    for module in modules:
        destination_modules: list[str] = link_to_destination_modules[module.name]
        for destination_module_name in destination_modules:
            destination_module: Module
            if destination_module_name in module_name_to_module:
                destination_module: Module = module_name_to_module[
                    destination_module_name
                ]
            else:
                destination_module: Module = EmptyModule(destination_module_name)
            module.add_destination_module(destination_module)
            if isinstance(destination_module, ConjunctionModule):
                destination_module.add_caller(module.name)

    broadcaster: Module = module_name_to_module[BROADCASTER]
    if not isinstance(broadcaster, BroadcastModule):
        raise ValueError("invalid file, missing broadcaster")

    button: ButtonModule = ButtonModule("button")
    button.add_destination_module(broadcaster)

    return button
