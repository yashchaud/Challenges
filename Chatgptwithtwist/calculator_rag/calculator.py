import re
from datetime import datetime
from database import store_calculation, get_calculations, search_calculations, delete_calculation

user_balances = {}
user_last_results = {}  # Track last result per user
global_last_result = 0  # Only for sum_all operations


def parse_transaction(text):
    text_lower = text.lower()

    users = re.findall(r'\b(ram|sita|john|mary|alice|bob)\b', text_lower)
    numbers = re.findall(r'\d+(?:\.\d+)?', text)

    amount = float(numbers[0]) if numbers else 0
    from_user = users[0] if users else "system"
    to_user = users[1] if len(users) > 1 else None

    # Check if this references previous result
    has_previous_ref = any(phrase in text_lower for phrase in [
        "previous", "from previous", "to previous", "from last", "to last",
        "last number", "last result", "previous number", "previous result",
        "with last", "by last", "times last", "divide by last", "multiply by last",
        "add to last", "subtract from last", "plus last", "minus last",
        "reduce from last", "reduces from last", "from result", "from last result",
        "from previous result", "from number", "from last number"
    ])

    if has_previous_ref and amount > 0:
        # Use last_result as the base for the operation
        pass

    operation = "add"
    if "total" in text_lower and "go back" not in text_lower:
        operation = "show_total"
    elif any(phrase in text_lower for phrase in ["sum all", "sum of all"]):
        operation = "sum_all"
    elif any(phrase in text_lower for phrase in ["clear memory", "clear your memory", "reset memory"]):
        operation = "clear_memory"
    elif any(phrase in text_lower for phrase in ["delete all", "clear all", "reset all", "remove all"]):
        operation = "clear_all"
    elif any(word in text_lower for word in [
        # Subtract synonyms - ALL forms of reduce should subtract
        "subtracts", "subtract", "minus", "reduce", "reduces", "reduced", "reducing",
        "decrease", "decreases", "decreased", "decreasing", "lower", "lowers", "lowered", "lowering",
        "deduct", "deducts", "deducted", "deducting", "less", "loses", "lost", "losing",
        "drops", "dropped", "dropping", "cut", "cuts", "cutting", "diminish", "diminishes", "diminished"
    ]) or any(phrase in text_lower for phrase in [
        "subtract from last", "minus last", "reduce from last", "reduces from last", "reduced from last",
        "reduce from", "reduces from", "reduced from", "reducing from",
        "from last", "from result", "from number", "from last result", "from last number"
    ]):
        operation = "subtract"
    elif any(phrase in text_lower for phrase in [
        # Take from operations (special transfer case)
        "takes from", "removes from", "steals from", "gets from"
    ]):
        operation = "takes_from"
    elif any(word in text_lower for word in [
        # Multiply synonyms
        "multiply", "multiplies", "multiplied", "times", "x", "*", "double", "doubles",
        "triple", "triples", "scale", "scales", "boost", "boosts"
    ]) or any(phrase in text_lower for phrase in [
        "times last", "multiply by last", "by last", "with last"
    ]):
        operation = "multiply"
    elif any(word in text_lower for word in [
        # Divide synonyms
        "divide", "divides", "divided", "split", "splits", "half", "halve", "halves",
        "/", "share", "shares", "partition", "partitions"
    ]) or any(phrase in text_lower for phrase in [
        "divide by last", "divided by last", "split by last"
    ]):
        operation = "divide"
    elif any(word in text_lower for word in [
        # Transfer synonyms
        "gives", "give", "transfers", "transfer", "sends", "send", "pays", "pay",
        "hands", "passes", "delivers", "provides"
    ]):
        operation = "transfer"
    elif any(word in text_lower for word in [
        # Add synonyms (default)
        "has", "gets", "get", "receives", "receive", "adds", "add", "gains", "gain",
        "increases", "increase", "plus", "+", "grows", "grows", "raises", "raise"
    ]) or any(phrase in text_lower for phrase in [
        "add to last", "plus last", "to last", "with last number"
    ]):
        operation = "add"

    return {
        "from_user": from_user,
        "to_user": to_user,
        "amount": amount,
        "operation": operation,
        "original_text": text,
        "has_previous_ref": has_previous_ref
    }


def execute_transaction(transaction):
    global global_last_result, user_balances, user_last_results
    from_user = transaction["from_user"]
    to_user = transaction["to_user"]
    amount = transaction["amount"]
    operation = transaction["operation"]
    has_previous_ref = transaction.get("has_previous_ref", False)

    if from_user not in user_balances:
        user_balances[from_user] = 0
    if from_user not in user_last_results:
        user_last_results[from_user] = 0

    # Handle previous references - use USER-SPECIFIC last result
    if has_previous_ref and operation in ["subtract", "add", "multiply", "divide"]:
        user_last = user_last_results[from_user]

        # Determine the operand: use specified amount or the last result itself
        if amount == 0:
            # No amount specified, check what kind of reference this is
            text_lower = transaction["original_text"].lower()
            if any(phrase in text_lower for phrase in ["last number", "last result", "previous number", "previous result"]):
                # Use the last result as the operand
                operand = user_last
            else:
                # Default to 1 for phrases like "from last", "from previous"
                operand = 1
        else:
            # Use the specified amount
            operand = amount

        print(f"DEBUG: {from_user} {operation} {operand} from last result {user_last}")

        if operation == "subtract":
            result = user_last - operand
        elif operation == "add":
            result = user_last + operand
        elif operation == "multiply":
            result = user_last * operand
        elif operation == "divide":
            result = user_last / operand if operand != 0 else user_last

        user_balances[from_user] = result
        user_last_results[from_user] = result
        global_last_result = result
        result_text = f"{from_user} now has {result}"

        store_calculation(
            query=transaction["original_text"],
            operation=operation,
            result=result,
            user=from_user
        )

        return {
            "result": result,
            "message": result_text,
            "users": dict(user_balances)
        }

    if operation == "show_total":
        result_text = f"{from_user} current balance: {user_balances[from_user]}"
        return {
            "result": user_balances[from_user],
            "message": result_text,
            "users": dict(user_balances)
        }

    elif operation == "sum_all":
        all_transactions = get_calculations(limit=1000)
        total_sum = sum(calc['result'] for calc in all_transactions)
        user_balances[from_user] = total_sum
        user_last_results[from_user] = total_sum
        global_last_result = total_sum
        result_text = f"{from_user} now has {total_sum}"

        store_calculation(
            query=transaction["original_text"],
            operation=operation,
            result=total_sum,
            user=from_user
        )

        return {
            "result": total_sum,
            "message": result_text,
            "users": dict(user_balances)
        }

    elif operation == "clear_memory":
        user_balances.clear()
        user_last_results.clear()
        global_last_result = 0
        result_text = "Memory cleared - all balances reset to 0"

        return {
            "result": 0,
            "message": result_text,
            "users": dict(user_balances)
        }

    elif operation == "clear_all":
        from database import clear_all_calculations
        clear_all_calculations()
        user_balances.clear()
        user_last_results.clear()
        global_last_result = 0
        result_text = "All transactions deleted and memory cleared"

        return {
            "result": 0,
            "message": result_text,
            "users": dict(user_balances)
        }

    elif operation == "add":
        user_balances[from_user] += amount
        user_last_results[from_user] = user_balances[from_user]
        global_last_result = user_balances[from_user]
        result_text = f"{from_user} now has {user_balances[from_user]}"

    elif operation == "subtract":
        user_balances[from_user] -= amount
        user_last_results[from_user] = user_balances[from_user]
        global_last_result = user_balances[from_user]
        result_text = f"{from_user} now has {user_balances[from_user]}"

    elif operation == "multiply":
        user_balances[from_user] *= amount
        user_last_results[from_user] = user_balances[from_user]
        global_last_result = user_balances[from_user]
        result_text = f"{from_user} now has {user_balances[from_user]}"

    elif operation == "divide":
        if amount != 0:
            user_balances[from_user] /= amount
        user_last_results[from_user] = user_balances[from_user]
        global_last_result = user_balances[from_user]
        result_text = f"{from_user} now has {user_balances[from_user]}"

    elif operation == "takes_from" and to_user:
        # When A takes from B: A gains, B loses
        if to_user not in user_balances:
            user_balances[to_user] = 0
        if to_user not in user_last_results:
            user_last_results[to_user] = 0

        user_balances[from_user] += amount  # Taker gains
        user_balances[to_user] -= amount    # Source loses

        user_last_results[from_user] = user_balances[from_user]
        user_last_results[to_user] = user_balances[to_user]
        global_last_result = user_balances[from_user]
        result_text = f"{from_user}: {user_balances[from_user]}, {to_user}: {user_balances[to_user]}"

    elif operation == "transfer" and to_user:
        if to_user not in user_balances:
            user_balances[to_user] = 0
        if to_user not in user_last_results:
            user_last_results[to_user] = 0

        user_balances[from_user] -= amount
        user_balances[to_user] += amount
        user_last_results[from_user] = user_balances[from_user]
        user_last_results[to_user] = user_balances[to_user]
        global_last_result = user_balances[from_user]
        result_text = f"{from_user}: {user_balances[from_user]}, {to_user}: {user_balances[to_user]}"

    else:
        result_text = f"Unknown operation"

    # Only store in database for actual calculations, not show operations
    if operation != "show_total":
        store_calculation(
            query=transaction["original_text"],
            operation=operation,
            result=user_balances[from_user],
            user=from_user
        )

        # For transfer operations, also store for the second user
        if operation in ["takes_from", "transfer"] and to_user:
            store_calculation(
                query=f"{to_user} affected by: {transaction['original_text']}",
                operation=f"{operation}_received",
                result=user_balances[to_user],
                user=to_user
            )

    return {
        "result": user_balances[from_user],
        "message": result_text,
        "users": dict(user_balances)
    }


def get_user_balance(username):
    return user_balances.get(username, 0)


def search_transactions(query_text):
    results = search_calculations(query_text, limit=5)

    if not results:
        return f"No transactions found for '{query_text}'"

    message = f"Found {len(results)} transactions:\n"
    for i, calc in enumerate(results, 1):
        try:
            timestamp = calc['timestamp'].strftime("%H:%M") if calc['timestamp'] else "Unknown"
        except:
            timestamp = "Unknown"
        message += f"{i}. [{calc['user']}] {calc['query']} = {calc['result']} ({timestamp})\n"

    return message.strip()


def show_user_balance(username):
    balance = get_user_balance(username)
    recent_transactions = get_calculations(limit=3, user=username)

    message = f"{username} current balance: {balance}\n"
    if recent_transactions:
        message += "Recent transactions:\n"
        for calc in recent_transactions:
            try:
                timestamp = calc['timestamp'].strftime("%H:%M") if calc['timestamp'] else "Unknown"
            except:
                timestamp = "Unknown"
            message += f"- {calc['query']} = {calc['result']} ({timestamp})\n"

    return message.strip()


def undo_last_transaction(username):
    user_transactions = get_calculations(limit=1, user=username)
    if not user_transactions:
        return f"No transactions found for {username}"

    last_transaction = user_transactions[0]
    delete_calculation(last_transaction['id'])

    remaining_transactions = get_calculations(limit=1, user=username)
    if remaining_transactions:
        user_balances[username] = remaining_transactions[0]['result']
    else:
        user_balances[username] = 0

    return f"Undone last transaction for {username}. New balance: {user_balances[username]}"


def handle_go_back(text):
    text_lower = text.lower()
    users = re.findall(r'\b(ram|sita|john|mary|alice|bob)\b', text_lower)
    username = users[0] if users else "system"

    if "negative" in text_lower:
        user_transactions = get_calculations(limit=10, user=username)
        for transaction in user_transactions:
            if transaction['result'] < 0:
                user_balances[username] = transaction['result']
                return f"Went back to when {username} had negative balance: {transaction['result']}"
        return f"No negative balance found for {username}"

    numbers = re.findall(r'\d+', text)
    if numbers:
        steps = int(numbers[0])
        user_transactions = get_calculations(limit=steps+1, user=username)

        # Debug: show what transactions we found
        print(f"Debug: Found {len(user_transactions)} transactions for {username}")
        for i, t in enumerate(user_transactions[:steps+1]):
            print(f"  {i}: {t['query']} = {t['result']}")

        if len(user_transactions) > steps:
            target_transaction = user_transactions[steps]
            user_balances[username] = target_transaction['result']
            return f"Went back {steps} transactions. {username} now has {user_balances[username]}"

    return f"Could not go back for {username}"


def handle_clear_operations(text):
    text_lower = text.lower()
    users = re.findall(r'\b(ram|sita|john|mary|alice|bob)\b', text_lower)
    username = users[0] if users else "system"

    numbers = re.findall(r'\d+', text)
    if numbers:
        count = int(numbers[0])
        user_transactions = get_calculations(limit=count, user=username)

        deleted_count = 0
        for transaction in user_transactions:
            delete_calculation(transaction['id'])
            deleted_count += 1

        remaining_transactions = get_calculations(limit=1, user=username)
        if remaining_transactions:
            user_balances[username] = remaining_transactions[0]['result']
        else:
            user_balances[username] = 0

        return f"Cleared last {deleted_count} transactions for {username}. New balance: {user_balances[username]}"

    return undo_last_transaction(username)


def process_query(text):
    text_lower = text.lower().strip()

    if any(phrase in text_lower for phrase in ["balance", "current", "how much", "result"]) and "go back" not in text_lower:
        users = re.findall(r'\b(ram|sita|john|mary|alice|bob)\b', text_lower)
        username = users[0] if users else "system"
        return show_user_balance(username)

    elif any(phrase in text_lower for phrase in ["search", "find", "show", "did"]) and "go back" not in text_lower:
        return search_transactions(text)

    elif any(phrase in text_lower for phrase in ["go back", "back to"]):
        return handle_go_back(text)

    elif any(phrase in text_lower for phrase in ["clear last", "remove last", "delete last", "undo"]):
        return handle_clear_operations(text)

    else:
        transaction = parse_transaction(text)
        result = execute_transaction(transaction)
        return result["message"]