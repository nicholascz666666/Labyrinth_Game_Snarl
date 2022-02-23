# Instruction to run SnarlServer4

* To run the server4, simply run command ./snarlServer4 to start the server with optional command line arguments:
--generate INT, where INT is a positive integer specifying the number of level that will be generated.

# Instruction to run SnarlGen
* To run snarlGen, simply run command ./snarlGen to start the program, with the following optional arguments:
* --rooms INT, where INT is a positive integer specifying the number of rooms in the level. Default: 5.
* --min ROWS COLS, specifying the minimum possible dimensions in the generated level. Default: 4 4. The format of the input should be like: --min ROWS COLS
* --max ROWS COLS, specifying the maximum dimensions of a room. Default: 15 15. The format of the input should be like: --max ROWS COLS
* --json, specifying that a JSON level representation should be printed to standard output. 
* --render, specifying that a preview of the level should be rendered to the screen. The snarlGen requires an X session to display a GUI if the argument --render is given.
