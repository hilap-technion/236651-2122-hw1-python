import unittest
import ast


class TestParseUnparse(unittest.TestCase):
    def testParsing(self):
        classCode = "class Complex:\n" + \
                    "     def __init__(self, realpart, imagpart):\n" + \
                    "         self.r = realpart\n" + \
                    "         self.i = imagpart"
        try:
            parsed = ast.parse(classCode)
        except:
            self.assertTrue(False) #not supposed to fail

        self.assertEqual(ast.Module,type(parsed))
        self.assertEqual(1,len(parsed.body))
        classDef = parsed.body[0]
        self.assertEqual("Complex", classDef.name)

    def testPartialParsing(self):
        code = "def __init__(self, realpart, imagpart):\n" + \
               "    self.r = realpart\n" + \
               "    self.i = imagpart"
        try:
            parsed = ast.parse(code)
        except:
            self.assertTrue(False) #not supposed to fail
        self.assertEqual(ast.Module, type(parsed))

        parsed = ast.parse("""self.i = imagpart""")
        self.assertEqual(ast.Module,type(parsed))
        self.assertEqual(ast.Assign,type(parsed.body[0]))

    def testASTtoString(self):
        code = "def __init__(self, realpart, imagpart):\n" + \
               "    self.r = realpart\n" + \
               "    self.i = imagpart"
        parsed = ast.parse(code)
        self.assertEqual("def __init__(self, realpart, imagpart):\n" +\
                         "    self.r = realpart\n" +\
                         "    self.i = imagpart",ast.unparse(parsed))

    def testModifyAndWrite1(self):
        classCode = "class Complex:\n" + \
                    "     def __init__(self, realpart, imagpart):\n" + \
                    "         self.r = realpart\n" + \
                    "         self.i = imagpart"
        module = ast.parse(classCode)
        module.body[0].name = "Simple"
        self.assertEqual("class Simple:\n\n" + \
                         "    def __init__(self, realpart, imagpart):\n" + \
                         "        self.r = realpart\n" + \
                         "        self.i = imagpart",ast.unparse(module))

    def testModifyAndWrite2(self):
        classCode = "class Complex:\n" + \
                    "     def __init__(self, realpart, imagpart):\n" + \
                    "         self.r = realpart\n" + \
                    "         self.i = imagpart"
        module = ast.parse(classCode)
        newMethod = ast.FunctionDef("foo",[],[ast.Pass()],[],lineno=0)
        module.body[0].body.append(newMethod)
        self.assertEqual("class Complex:\n\n" + \
                         "    def __init__(self, realpart, imagpart):\n" + \
                         "        self.r = realpart\n" + \
                         "        self.i = imagpart\n\n" + \
                         "    def foo():\n" +\
                         "        pass", ast.unparse(module))

    def testModifyAndWrite3(self):
        classCode = "class Complex:\n" + \
                    "     def __init__(self, realpart, imagpart):\n" + \
                    "         self.r = realpart\n" + \
                    "         self.i = imagpart\n" + \
                    "         print(self.i)\n"
        module = ast.parse(classCode)
        class DeepReplace(ast.NodeTransformer):
            def visit_Call(self,node):
                if (node.func.id == "print"):
                    node.args[0] = ast.BinOp(ast.Name("realpart"),ast.Add(),ast.Name("imagpart"))
                return node

        newTree = DeepReplace().visit(module)
        self.assertEqual("class Complex:\n\n" + \
                         "    def __init__(self, realpart, imagpart):\n" + \
                         "        self.r = realpart\n" + \
                         "        self.i = imagpart\n" + \
                         "        print(realpart + imagpart)",ast.unparse(newTree))


if __name__ == '__main__':
    unittest.main()
