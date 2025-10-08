from tree_sitter import Language, Parser
import tree_sitter_python as tspython
import os

# Initialize parser
PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

def parse_python_file(file_path):
    """
    Parse a Python file and return the root AST node.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'rb') as f:
        code = f.read()
    tree = parser.parse(code)
    return tree.root_node

# Query functions

def extract_functions(node, parent_type=None):
    """
    Recursively extract all function definitions (including async, methods, nested, decorated) from the AST node.
    Returns a list of dicts with function details.
    """
    functions = []
    # Detect function type
    is_function = node.type == 'function_definition'
    is_async_function = node.type == 'async_function_definition'
    is_class = node.type == 'class_definition'
    # For class context
    class_name = None
    if is_class:
        name_node = node.child_by_field_name('name')
        class_name = name_node.text.decode('utf8') if name_node else None
    # Extract function details
    if is_function or is_async_function:
        func_name_node = node.child_by_field_name('name')
        func_name = func_name_node.text.decode('utf8') if func_name_node else '<lambda>'
        params_node = node.child_by_field_name('parameters')
        params = params_node.text.decode('utf8') if params_node else ''
        # Docstring extraction: first expression_statement with string child
        docstring = None
        for child in node.children:
            if child.type == 'expression_statement' and child.child_count > 0:
                str_node = child.children[0]
                if str_node.type == 'string':
                    docstring = str_node.text.decode('utf8')
                    break
        # Decorators
        decorators = []
        for child in node.children:
            if child.type == 'decorator':
                decorators.append(child.text.decode('utf8'))
        # Function type
        if parent_type == 'class_definition':
            func_type = 'method'
        elif is_async_function:
            func_type = 'async_function'
        else:
            func_type = 'function'
        functions.append({
            'type': func_type,
            'name': func_name,
            'parameters': params,
            'docstring': docstring,
            'decorators': decorators,
            'class': class_name if parent_type == 'class_definition' else None,
            'start_byte': node.start_byte,
            'end_byte': node.end_byte,
            'start_line': node.start_point[0],
            'end_line': node.end_point[0],
            'text': node.text.decode('utf8')
        })
    # Recursively extract from children
    for child in node.children:
        child_parent_type = node.type if is_class else parent_type
        functions.extend(extract_functions(child, parent_type=child_parent_type))
    return functions

def extract_classes(node, parent_class=None):
    """
    Recursively extract all class definitions and their attributes from the AST node.
    Returns a list of dicts with class details.
    """
    classes = []
    if node.type == 'class_definition':
        name_node = node.child_by_field_name('name')
        class_name = name_node.text.decode('utf8') if name_node else None
        base_node = node.child_by_field_name('base')
        base_classes = base_node.text.decode('utf8') if base_node else None
        attributes = []
        methods = []
        inner_classes = []
        instance_attributes = set()
        # Find the block node (class body)
        block_node = None
        for child in node.children:
            if child.type == 'block':
                block_node = child
                break
        # If block found, look for assignments and annotated_assignments inside
        # Only collect assignments from immediate children of block_node (not recursively)
        if block_node:
            for stmt in block_node.children:
                if stmt.type == 'assignment' or stmt.type == 'annotated_assignment':
                    for sub in stmt.children:
                        if sub.type == 'identifier':
                            attributes.append(sub.text.decode('utf8'))
                elif stmt.type in ('function_definition', 'async_function_definition'):
                    method_name_node = stmt.child_by_field_name('name')
                    method_name = method_name_node.text.decode('utf8') if method_name_node else None
                    methods.append(method_name)
                    # Scan for instance attributes in method body
                    method_block = None
                    for mchild in stmt.children:
                        if mchild.type == 'block':
                            method_block = mchild
                            break
                    if method_block:
                        for mstmt in method_block.children:
                            if mstmt.type == 'assignment':
                                left_node = mstmt.child_by_field_name('left')
                                # Check for self.<attr> (member_expression)
                                if left_node and left_node.type == 'member_expression':
                                    object_node = left_node.child_by_field_name('object')
                                    property_node = left_node.child_by_field_name('property')
                                    if object_node and object_node.text.decode('utf8') == 'self' and property_node:
                                        instance_attributes.add(property_node.text.decode('utf8'))
                elif stmt.type == 'class_definition':
                    inner_classes.extend(extract_classes(stmt, parent_class=class_name))
        # Also check for inner classes at the top level (for nested classes)
        for child in node.children:
            if child.type == 'class_definition' and child != block_node:
                inner_classes.extend(extract_classes(child, parent_class=class_name))
        classes.append({
            'name': class_name,
            'base_classes': base_classes,
            'attributes': attributes,
            'instance_attributes': list(instance_attributes),
            'methods': methods,
            'inner_classes': inner_classes,
            'parent_class': parent_class,
            'start_line': node.start_point[0],
            'end_line': node.end_point[0],
            'text': node.text.decode('utf8')
        })
    # Recursively extract from children
    for child in node.children:
        classes.extend(extract_classes(child, parent_class=parent_class))
    return classes

if __name__ == "__main__":
    # You can change this path to any Python file you want to parse
    file_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.py')
    try:
        root_node = parse_python_file(file_path)
        funcs = extract_functions(root_node)
        classes = extract_classes(root_node)
        for c in classes:
            print(f"Class: {c['name']}")
            if c['base_classes']:
                print(f"Base classes: {c['base_classes']}")
            print(f"Class attributes: {c['attributes']}")
            print(f"Instance attributes: {c['instance_attributes']}")
            print(f"Methods: {c['methods']}")
            if c['inner_classes']:
                print(f"Inner classes: {[ic['name'] for ic in c['inner_classes']]}")
            print(f"Lines: {c['start_line']}-{c['end_line']}")
            print(f"Code:\n{c['text']}\n")
        for f in funcs:
            print(f"Type: {f['type']}")
            if f['class']:
                print(f"Class: {f['class']}")
            print(f"Function: {f['name']}")
            print(f"Parameters: {f['parameters']}")
            if f['decorators']:
                print(f"Decorators: {f['decorators']}")
            if f['docstring']:
                print(f"Docstring: {f['docstring']}")
            print(f"Lines: {f['start_line']}-{f['end_line']}")
            print(f"Code:\n{f['text']}\n")
    except Exception as e:
        print(f"Error: {e}")
