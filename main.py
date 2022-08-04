from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Union

class Token(str, Enum):
    PTR_L = "<"
    PTR_R = ">"
    INCR = "+"
    DECR = "-"
    OUT = "."
    IN = ","
    JMP_IZ = "["
    JMP_NZ = "]"

VALID_TOKENS = [
    tok.value for tok in Token
]

@dataclass
class Instruction:
    """An optimisation class to store a recurring instruction in one."""
    token: Token
    amount: int


def parse_tokenlist(code: str) -> list[Token]:
    tokens = []
    for char in code:
        if char in VALID_TOKENS:
            tokens.append(Token(char))
    
    return tokens

NO_AM_OPTIMISE = (Token.JMP_IZ, Token.JMP_NZ)
def parse_instructions(code: list[Token]) -> list[Instruction]:
    instructions = []

    prev_instruction = code[0]
    amount = 1

    for token in code[1:]: # First instruction is alr accounted for.
        if token != prev_instruction or token in NO_AM_OPTIMISE:
            instructions.append(Instruction(
                prev_instruction,
                amount,
            ))
            prev_instruction = token
            amount = 1
        else:
            amount += 1
        
    return instructions

label_count = 0
def gen_label() -> str:
    global label_count
    label_count += 1
    return f"L{label_count}"

@dataclass
class Label:
    """A way to handle the jump operations nicely."""

    name: str
    instructions: list[Union[Instruction, Label]]

    @staticmethod
    def parse_instructions(code: list[Instruction]) -> Label:
        """Assumes the control flow instructions have been ommited from the start and beginning."""

        new_label = Label(
            gen_label(),
            [],
        )

        code_iter = iter(code)

        for idx, instruction in enumerate(code_iter):
            if instruction.token != Token.JMP_IZ:
                new_label.instructions.append(instruction)
            else:
                end_idx = idx
                depth = 1
                while depth:
                    print("Depth eq", depth)
                    print(code[idx:])
                    n_instruction = next(code_iter)
                    end_idx += 1
                    if n_instruction.token == Token.JMP_IZ:
                        depth += 1
                        print(depth, "add")
                    elif n_instruction.token == Token.JMP_NZ:
                        depth -= 1
                        print(depth, "sub")
                print("Stopped")
                new_label.instructions.append(
                    Label.parse_instructions(
                        code[idx + 1:end_idx - 1],
                    )
                )
        return new_label

HELLO_WORLD = """
>++++++++[<+++++++++>-]<.>++++[<+++++++>-]<+.+++++++..+++.>>++++++[<+++++++>-]<+
+.------------.>++++++[<+++++++++>-]<+.<.+++.------.--------.>>>++++[<++++++++>-
]<+
"""

tokens = parse_tokenlist(HELLO_WORLD)
print(tokens)
instructions = parse_instructions(tokens)
print(instructions)
label = Label.parse_instructions(instructions)
print(repr(label))
