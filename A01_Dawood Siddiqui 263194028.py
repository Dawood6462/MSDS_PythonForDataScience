class Preprocessor:
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.outputFile = "out1.txt"

    def removeBlankLines(self, lines):
        """In this function we are removing blank lines from the argument 'lines'."""
        filtered = []
        for line in lines:
            if line.strip():
                filtered.append(line)

        return filtered

    def removeComments(self, lines):
        """In this function we are removing comments from the argument 'lines'."""
        SLCommentRemoved = []
        for line in lines: #This paet is removing Single line comments from the input
            SLCommentRemoved.append(line.split("//")[0])

         #This paet is removing Multi line comments from the input and appendind the result in 'result' list
        result = []
        inMLcomment = False
        for line in SLCommentRemoved:
            if "/*" in line:
                inMLcomment = True
                line = line.split("/*")[0]
            elif "*/" in line:
                inMLcomment = False
                line = line.split("*/")[-1]
            elif not inMLcomment:
                result.append(line)
        
        return result

    
    def removeSpaces(self, lines):
        """In this function we are removing spaces from the argument 'lines'."""
        spacesRemoved = []
        for line in lines:
            spacesRemoved.append(" ".join(line.split()))

        return spacesRemoved

    def removeImports(self, lines):
        """In this function we are removing import statements from the argument 'lines'."""
        filtered = []
        for line in lines:
            if not (line.strip().startswith("@") or line.strip().startswith("import")):
                filtered.append(line)
        
        return filtered


    def Main(self):
        """Main method is handler of preprocessor clas. It is first opening the input file in read mode and then 
        passing the content of input file to respective methods to remove blank lines, import statements, spaces and 
        comments. After that, this content is being written to the output file."""
        with open(self.inputFile, 'r') as f:
            lines = f.readlines()

        lines = self.removeSpaces(lines)
        lines = self.removeBlankLines(lines)
        lines = self.removeComments(lines)
        lines = self.removeImports(lines)

        with open(self.outputFile, 'w') as f:
            f.write("\n".join(lines))
        
        print("Contents of the file " + self.outputFile +"after preprocessing:")
        with open(self.outputFile, 'r') as file:
            print(file.read())

class Processor:
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.outputFile = "out2.txt"

    def Main(self):
        """Main method is handler of Processor clas. It is first opening the input file in read mode and then 
        replacing new line Chars with spaces. After that, this content is being written to the output file."""
        with open(self.inputFile, 'r') as file:
            contents = file.read().replace('\n', ' ')
        
        contents += " $"  # Adding sentinel at the end

        with open(self.outputFile, 'w') as file:
            file.write(contents)
        
        print("Contents of the file " + self.outputFile +"after Processing:")
        with open(self.outputFile, 'r') as file:
            print(file.read())

class LexicalAnalyzer:
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.lexemes = []
        self.allKeywords = {"if", "else", "while", "for", "do", "int", "float", "double", "char", "void", 
                    "boolean", "true", "false", "return", "class", "public", "private", "protected",
                    "static", "final", "try", "catch", "throw", "interface"}

        self.allOperators = {"+", "-", "*", "/", "%", "=", "+=", "-=", "*=", "/=", "==", "!=", "<", ">", 
                     "<=", ">=", "++", "--", "&&", "||"}

        self.allPunctuations = {"{", "}", "[", "]", "(", ")", ",", ";", ":", "."}

    def keywordCheck(self, word):
        """This functioin is checking if argument 'word' is in list allKeywords"""
        return word in self.allKeywords

    def operatorCheck(self, char):
        """This functioin is checking if argument 'word' is in list allOperators"""
        return char in self.allOperators

    def puncCheck(self, char):
        """This functioin is checking if argument 'word' is in list allPunctuations"""
        return char in self.allPunctuations

    def literalCheck(self, word):
        """This functioin is checking if argument 'word' is a literal"""
        if word.isdigit():  # Checking if 'word' is int
            return True
        if word.startswith('"') and word.endswith('"'):  # Checking if 'word' is stribg
            return True
        if word.startswith("'") and word.endswith("'") and len(word) == 3:  # Checking if 'word' is char literal
            return True
        return False

    def classify_token(self, token):
        if self.keywordCheck(token):
            self.lexemes.append("Lexeme: " + token + " (Keyword)")
        elif self.literalCheck(token):
            self.lexemes.append("Lexeme: " + token + " (Literal)")
        else:
            self.lexemes.append("Lexeme: " + token + " (Identifier)")

    def Main(self):
        with open(self.inputFile, 'r') as f:
            contents = f.read().replace('$', '').strip()  # Remove sentinel for analysis

        # Splitting content manually by spaces and punctuators
        word = ""
        for char in contents:
            if char.isalnum() or char == "_":
                word += char
            else:
                if word:
                    self.classify_token(word)
                    word = ""
                if char.strip() and (self.operatorCheck(char) or self.puncCheck(char)):
                    self.lexemes.append("Lexeme: " + char)

        if word:  # Process the last token if exists
            self.classify_token(word)

        print("Final Output(LexicalAnalyzer):")
        for lexeme in self.lexemes:
            print(lexeme)


#Object of Preprocessor class.  It is taking file name as input
preprocessor = Preprocessor('File1.java')
preprocessor.Main()

#Object of Processor class.  It is taking output file of preprocessor class as input
processor = Processor('out1.txt')
processor.Main()

#Object of LexicalAnalyzer class.  It is taking output file of Processor class as input
lex_analyzer = LexicalAnalyzer('out2.txt')
lex_analyzer.Main()
