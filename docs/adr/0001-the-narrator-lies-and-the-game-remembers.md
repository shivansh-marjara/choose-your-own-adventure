# The narrator lies, and the game remembers you

We write run history to a local `keeper_save.json` and use it to have the Narrator address the player by name and refer to their previous ending, and we write the Narrator as a deliberately unreliable character — its lines and the ending text frame the lighthouse as a rescue when it is a trap.

We chose this over an honest, self-contained story because the challenge rewards an unusual submission, and because persistence turns a one-shot CYOA into something that greets a returning player differently. The cost is real: the game now writes to disk and behaves differently on the second run, which is surprising if you only read the code once.