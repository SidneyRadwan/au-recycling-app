"""PostgreSQL upsert logic for council data."""

import logging
from typing import Any

import psycopg2
from psycopg2.extras import execute_values

from config import settings
from models import CouncilData

logger = logging.getLogger(__name__)


def get_connection():
    url = settings.get_database_url()
    # Strip jdbc: prefix if present — psycopg2 requires a plain postgres:// DSN
    if url.startswith("jdbc:"):
        url = url[5:]
    return psycopg2.connect(
        url,
        user=settings.database_username,
        password=settings.database_password,
    )


def upsert_council(conn, council: CouncilData) -> int:
    """Upsert council and return its database ID."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO councils (name, slug, state, website, recycling_info_url, description)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO UPDATE SET
                name = EXCLUDED.name,
                state = EXCLUDED.state,
                website = EXCLUDED.website,
                recycling_info_url = EXCLUDED.recycling_info_url,
                description = EXCLUDED.description,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id
            """,
            (
                council.name,
                council.slug,
                council.state,
                council.website,
                council.recycling_info_url,
                council.description,
            ),
        )
        return cur.fetchone()[0]


def upsert_suburbs(conn, council_id: int, suburbs: list[str], state: str) -> None:
    """Upsert suburbs for a council."""
    if not suburbs:
        return
    with conn.cursor() as cur:
        rows: list[tuple[Any, ...]] = []
        for suburb_entry in suburbs:
            # Support "Suburb Name 2000" or just "Suburb Name"
            parts = suburb_entry.rsplit(" ", 1)
            if len(parts) == 2 and parts[1].isdigit():
                name, postcode = parts[0], parts[1]
            else:
                name, postcode = suburb_entry, "0000"
            rows.append((name, postcode, state, council_id))

        execute_values(
            cur,
            """
            INSERT INTO suburbs (name, postcode, state, council_id)
            VALUES %s
            ON CONFLICT DO NOTHING
            """,
            rows,
        )


def upsert_material(
    conn, material_slug: str, material_name: str, category: str | None
) -> int:
    """Upsert a material and return its ID."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO materials (name, slug, category)
            VALUES (%s, %s, %s)
            ON CONFLICT (slug) DO UPDATE SET
                name = EXCLUDED.name,
                category = COALESCE(EXCLUDED.category, materials.category)
            RETURNING id
            """,
            (material_name, material_slug, category),
        )
        return cur.fetchone()[0]


def upsert_council_material(
    conn,
    council_id: int,
    material_id: int,
    bin_type: str,
    instructions: str | None,
    notes: str | None,
) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO council_materials (council_id, material_id, bin_type, instructions, notes)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (council_id, material_id) DO UPDATE SET
                bin_type = EXCLUDED.bin_type,
                instructions = EXCLUDED.instructions,
                notes = EXCLUDED.notes
            """,
            (council_id, material_id, bin_type, instructions, notes),
        )


def get_council_scraper_configs() -> list[dict]:
    """Return councils that have a recycling_info_url set — the scraper work list."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT slug, name, state, website, recycling_info_url, description "
            "FROM councils WHERE recycling_info_url IS NOT NULL ORDER BY slug"
        )
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, row)) for row in cur.fetchall()]
    conn.close()
    # Rename to match scraper config key expected by GenericCouncilScraper
    for row in rows:
        row["recycling_url"] = row.pop("recycling_info_url")
    return rows


def save_council_data(council: CouncilData) -> None:
    """Full upsert pipeline for a council and all its data."""
    logger.info("Saving council: %s", council.slug)
    conn = get_connection()
    try:
        council_id = upsert_council(conn, council)
        logger.info("  Council ID: %d", council_id)

        upsert_suburbs(conn, council_id, council.suburbs, council.state)
        logger.info("  Upserted %d suburbs", len(council.suburbs))

        for cm in council.materials:
            # Derive material name from slug (title case, replace hyphens)
            material_name = cm.material_slug.replace("-", " ").title()
            material_id = upsert_material(conn, cm.material_slug, material_name, None)
            upsert_council_material(
                conn,
                council_id,
                material_id,
                cm.bin_type.value,
                cm.instructions,
                cm.notes,
            )
        logger.info("  Upserted %d council materials", len(council.materials))

        conn.commit()
        logger.info("  Committed successfully")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
