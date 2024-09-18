from utils import FileOperationQueue, perform_file_operation

def parse_llm_response(conversation_thread, llm_response):
    file_op_queue = FileOperationQueue()
    file_operation_performed = False
    developer_input_required = False
    processed_response = []

    logger.info("Starting to process LLM response")
    logger.debug(f"Raw LLM response:\n{llm_response}")

    patterns = {
        'read': r'<read path=(?:")?([^">]+)(?:")? />',
        'write': r'<write path=(?:")?([^">]+)(?:")?>\s*([\s\S]*?)\s*</write>',
        'append': r'<append path=(?:")?([^">]+)(?:")?>([\s\S]*?)</append>',
        'delete': r'<delete path=(?:")?([^">]+)(?:")? />',
        'rename': r'<rename current_path=(?:")?([^">]+)(?:")? new_path=(?:")?([^">]+)(?:")? />',
        'move': r'<move current_path=(?:")?([^">]+)(?:")? new_path=(?:")?([^">]+)(?:")? />',
        'list_directory': r'<list_directory path=(?:")?([^">]+)(?:")? />',
        'create_directory': r'<create_directory path=(?:")?([^">]+)(?:")? />',
        'request_developer_action': r'<request_developer_action=true>'
    }

    for operation, pattern in patterns.items():
        matches = re.finditer(pattern, llm_response, re.DOTALL)
        for match in matches:
            if operation == 'read':
                path = os.path.abspath(match.group(1))
                read_op = file_op_queue.add_operation('read', path)
                # Add dependency: read operation depends on write operation to the same file
                for op in file_op_queue.queue:
                    if op.operation in ['write', 'append'] and op.args[0] == path:
                        file_op_queue.add_dependency(read_op, op)
            elif operation == 'write':
                path, content = match.groups()
                path = os.path.abspath(path)
                file_op_queue.add_operation('write', path, content)
            elif operation == 'append':
                path, content = match.groups()
                path = os.path.abspath(path)
                file_op_queue.add_operation('append', path, content)
            elif operation == 'delete':
                path = os.path.abspath(match.group(1))
                file_op_queue.add_operation('delete', path)
            elif operation == 'rename' or operation == 'move':
                current_path, new_path = match.groups()
                current_path = os.path.abspath(current_path)
                new_path = os.path.abspath(new_path)
                file_op_queue.add_operation(operation, current_path, new_path)
            elif operation == 'list_directory':
                path = os.path.abspath(match.group(1))
                file_op_queue.add_operation('list_directory', path)
            elif operation == 'create_directory':
                path = os.path.abspath(match.group(1))
                file_op_queue.add_operation('create_directory', path)
            elif operation == 'request_developer_action':
                developer_input_required = True
    
    # Process all queued operations
    results = file_op_queue.process_queue()

    for op, result in results.items():
        if op.operation == 'read':
            processed_response.append(f"Content of {op.args[0]}:\n{result}")
        elif op.operation == 'write':
            processed_response.append(f"File written: {op.args[0]}")
        elif op.operation == 'append':
            processed_response.append(f"Content appended to: {op.args[0]}")
        elif op.operation == 'delete':
            processed_response.append(f"File deleted: {op.args[0]}")
        elif op.operation in ['rename', 'move']:
            processed_response.append(f"File {op.operation}d from {op.args[0]} to {op.args[1]}")
        elif op.operation == 'list_directory':
            processed_response.append(f"Contents of {op.args[0]}:\n{', '.join(result)}")
        elif op.operation == 'create_directory':
            processed_response.append(f"Directory created: {op.args[0]}")
        
        if result is not False:
            file_operation_performed = True

    # Save action results to conversation thread
    processed_response = '\n'.join(processed_response)
    conversation_thread = f"{conversation_thread}\n\n*** OPERATION RESULTS ***\n\n{processed_response}"

    # Check if developer input is required
    if developer_input_required:
        return conversation_thread, True

    # Check if any file operation was performed
    if not file_operation_performed:
        # If no file operation was performed and no developer action was requested,
        # we assume the AI's response is complete and requires developer input
        return conversation_thread, True

    # Prepare response to developer (for logging purposes)
    response_to_developer = llm_response

    # Remove file contents of written files from the response (for logging purposes)
    for match in re.finditer(patterns['write'], llm_response, re.DOTALL):
        path, content = match.groups()
        if content:
            response_to_developer = response_to_developer.replace(content, f"[Content written to {path}]")

    logger.info(f"File operation performed: {file_operation_performed}")
    logger.info(f"Developer input required: {developer_input_required}")
    logger.debug(f"Processed response:\n{processed_response}")
    logger.debug(f"Response to developer:\n{response_to_developer}")

    # Return the updated conversation thread and False to indicate no developer input is required
    return conversation_thread, False