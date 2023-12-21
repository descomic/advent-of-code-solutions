from modules import parse_modules, ButtonModule, Module, LOW_SIGNAL


def press_button(button: ButtonModule) -> list[str]:
    result: list[str] = []
    modules_to_process: list[Module] = [button]
    signals_to_send: list[int] = [LOW_SIGNAL]
    callers: list[str] = [""]

    while len(modules_to_process) > 0:
        number_of_modules_to_process = len(modules_to_process)
        for _ in range(number_of_modules_to_process):
            module = modules_to_process.pop(0)
            signal = signals_to_send.pop(0)
            caller = callers.pop(0)
            processed_signal: int = module.process_signal(signal, caller)
            if processed_signal is None:
                continue
            for destination in module.destination_modules:
                result.append(
                    f"{module.name} -{'low' if processed_signal == LOW_SIGNAL else 'high'}-> {destination.name}"
                )
                modules_to_process.append(destination)
                signals_to_send.append(processed_signal)
                callers.append(module.name)
    return result


def compute_total_number_low_times_high_pulses(file_name: str) -> int:
    button: ButtonModule

    with open(file_name) as file:
        lines: list[str] = file.read().splitlines()
        button = parse_modules(lines)

    low_pulses: int = 0
    high_pulses: int = 0

    i = 0
    while i < 1000:
        steps: list[str] = press_button(button)
        joined_steps: str = "\n".join(steps)
        print(joined_steps)
        print()
        low_pulses += joined_steps.count("-low")
        high_pulses += joined_steps.count("-high")
        i += 1

    return low_pulses * high_pulses


if __name__ == "__main__":
    print(compute_total_number_low_times_high_pulses("input.txt"))
