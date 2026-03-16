#!/usr/bin/env python3
"""MCP server exposing Australia Recycling DB tools for the AI agent."""

import json
import logging
import sys

import psycopg2
from mcp.server.fastmcp import FastMCP

from config import settings

logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger(__name__)

mcp = FastMCP("australia-recycling")


def _get_conn():
    return psycopg2.connect(settings.database_url)


@mcp.tool()
def get_council_info(slug: str) -> str:
    """Get full recycling information for a council by its slug (e.g. city-of-sydney)."""
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, slug, state, website, recycling_info_url, description
                FROM councils WHERE slug = %s
                """,
                (slug,),
            )
            row = cur.fetchone()
            if not row:
                return json.dumps({"error": f"Council not found: {slug}"})

            council_id, name, c_slug, state, website, info_url, description = row

            cur.execute(
                """
                SELECT m.name, m.slug, m.category, cm.bin_type, cm.instructions, cm.notes
                FROM council_materials cm
                JOIN materials m ON m.id = cm.material_id
                WHERE cm.council_id = %s
                ORDER BY cm.bin_type, m.name
                """,
                (council_id,),
            )
            materials = [
                {
                    "material": r[0],
                    "slug": r[1],
                    "category": r[2],
                    "bin_type": r[3],
                    "instructions": r[4],
                    "notes": r[5],
                }
                for r in cur.fetchall()
            ]

        return json.dumps(
            {
                "name": name,
                "slug": c_slug,
                "state": state,
                "website": website,
                "recycling_info_url": info_url,
                "description": description,
                "materials": materials,
            },
            indent=2,
        )
    finally:
        conn.close()


@mcp.tool()
def search_materials(query: str, council_slug: str = "") -> str:
    """Search for recycling info about a material across all councils (or one council).

    Args:
        query: Material name or keyword (e.g. "cardboard", "battery", "soft plastic").
        council_slug: Optional council slug to limit the search.
    """
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            sql = """
                SELECT c.name, c.slug, m.name, m.slug, cm.bin_type, cm.instructions, cm.notes
                FROM council_materials cm
                JOIN councils c ON c.id = cm.council_id
                JOIN materials m ON m.id = cm.material_id
                WHERE (m.name ILIKE %s OR m.slug ILIKE %s)
            """
            params: list = [f"%{query}%", f"%{query}%"]
            if council_slug:
                sql += " AND c.slug = %s"
                params.append(council_slug)
            sql += " ORDER BY c.name, m.name LIMIT 50"

            cur.execute(sql, params)
            results = [
                {
                    "council": r[0],
                    "council_slug": r[1],
                    "material": r[2],
                    "material_slug": r[3],
                    "bin_type": r[4],
                    "instructions": r[5],
                    "notes": r[6],
                }
                for r in cur.fetchall()
            ]

        return json.dumps({"results": results, "count": len(results)}, indent=2)
    finally:
        conn.close()


@mcp.tool()
def list_councils(state: str = "") -> str:
    """List all available councils, optionally filtered by state code (e.g. NSW, VIC, QLD)."""
    conn = _get_conn()
    try:
        with conn.cursor() as cur:
            sql = "SELECT name, slug, state, website FROM councils"
            params: list = []
            if state:
                sql += " WHERE state = %s"
                params.append(state.upper())
            sql += " ORDER BY state, name"

            cur.execute(sql, params)
            councils = [
                {"name": r[0], "slug": r[1], "state": r[2], "website": r[3]}
                for r in cur.fetchall()
            ]

        return json.dumps({"councils": councils, "count": len(councils)}, indent=2)
    finally:
        conn.close()


if __name__ == "__main__":
    mcp.run()
