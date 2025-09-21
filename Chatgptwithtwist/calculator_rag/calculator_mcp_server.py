#!/usr/bin/env python3

import logging
import sys
from typing import Optional, Dict, Any

from mcp.server.fastmcp import FastMCP
from database import setup_database, get_embedding_model, get_calculations
from calculator import (
    process_query,
    get_user_balance,
    search_transactions,
    show_user_balance,
    undo_last_transaction,
    handle_go_back,
    user_balances,
    user_last_results
)

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

mcp = FastMCP("Calculator RAG Server")

@mcp.tool()
def process_transaction(query: str) -> Dict[str, Any]:
    """Process a calculator transaction like 'ram has 5kg' or 'sita takes 2kg from ram'"""
    try:
        result = process_query(query)
        return {
            "message": result,
            "balances": dict(user_balances),
            "success": True
        }
    except Exception as e:
        return {
            "message": f"Error: {str(e)}",
            "balances": dict(user_balances),
            "success": False
        }

@mcp.tool()
def get_balance(username: str) -> Dict[str, Any]:
    """Get current balance for a user"""
    try:
        balance_info = show_user_balance(username)
        return {
            "username": username,
            "balance": get_user_balance(username),
            "details": balance_info,
            "success": True
        }
    except Exception as e:
        return {
            "username": username,
            "balance": 0,
            "details": f"Error: {str(e)}",
            "success": False
        }

@mcp.tool()
def search_history(query: str) -> Dict[str, Any]:
    """Search transaction history"""
    try:
        results = search_transactions(query)
        return {
            "query": query,
            "results": results,
            "success": True
        }
    except Exception as e:
        return {
            "query": query,
            "results": f"Error: {str(e)}",
            "success": False
        }

@mcp.tool()
def undo_transaction(username: str) -> Dict[str, Any]:
    """Undo last transaction for a user"""
    try:
        result = undo_last_transaction(username)
        return {
            "username": username,
            "message": result,
            "new_balance": get_user_balance(username),
            "success": True
        }
    except Exception as e:
        return {
            "username": username,
            "message": f"Error: {str(e)}",
            "new_balance": get_user_balance(username),
            "success": False
        }

@mcp.tool()
def go_back(query: str) -> Dict[str, Any]:
    """Go back to previous state like 'ram go back 3 transactions'"""
    try:
        result = handle_go_back(query)
        return {
            "query": query,
            "message": result,
            "balances": dict(user_balances),
            "success": True
        }
    except Exception as e:
        return {
            "query": query,
            "message": f"Error: {str(e)}",
            "balances": dict(user_balances),
            "success": False
        }

@mcp.tool()
def clear_memory(clear_all: bool = False) -> Dict[str, Any]:
    """Clear memory and optionally all transactions"""
    try:
        if clear_all:
            result = process_query("clear all")
        else:
            result = process_query("clear memory")

        return {
            "message": result,
            "balances": dict(user_balances),
            "success": True
        }
    except Exception as e:
        return {
            "message": f"Error: {str(e)}",
            "balances": dict(user_balances),
            "success": False
        }

@mcp.tool()
def get_all_balances() -> Dict[str, Any]:
    """Get all user balances"""
    try:
        return {
            "balances": dict(user_balances),
            "total": sum(user_balances.values()),
            "users": len(user_balances),
            "last_results": dict(user_last_results),
            "success": True
        }
    except Exception as e:
        return {
            "balances": {},
            "total": 0,
            "users": 0,
            "last_results": {},
            "success": False,
            "error": str(e)
        }

@mcp.resource("balance://{username}")
def balance_resource(username: str) -> str:
    balance = get_user_balance(username)
    return f"{username}: {balance}"

@mcp.resource("transactions://recent")
def recent_transactions() -> str:
    transactions = get_calculations(limit=10)
    if not transactions:
        return "No transactions"

    output = []
    for t in transactions:
        timestamp = t['timestamp'].strftime("%H:%M") if t['timestamp'] else ""
        output.append(f"{t['user']}: {t['query']} = {t['result']} ({timestamp})")

    return "\n".join(output)

@mcp.resource("summary://all")
def summary() -> str:
    total = sum(user_balances.values())
    lines = [
        f"Users: {len(user_balances)}",
        f"Total: {total}",
        ""
    ]

    for user, balance in user_balances.items():
        lines.append(f"{user}: {balance}")

    return "\n".join(lines)

def initialize():
    logger.info("Starting calculator server...")

    if not setup_database():
        logger.error("Database setup failed")
        return False

    logger.info("Loading model...")
    get_embedding_model()

    logger.info("Ready!")
    return True

if __name__ == "__main__":
    if not initialize():
        sys.exit(1)

    mcp.run(transport="stdio")