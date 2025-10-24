"""
Main CLI entry point for PENGUIN
Provides commands for data collection, analysis, and management
"""

import asyncio
import click
from typing import Optional

from penguin.data.registry import registry
from penguin.data.storage.database import db
from penguin.data.storage.store import store
from penguin.core.config import config


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """PENGUIN - AI-Powered Stock Analysis Platform"""
    pass


@cli.command()
def init():
    """Initialize database and create tables"""
    click.echo("Initializing PENGUIN database...")

    try:
        db.connect()
        db.create_tables()
        click.echo("Database initialized successfully!")
    except Exception as e:
        click.echo(f"Error initializing database: {e}", err=True)
        raise click.Abort()


@cli.group()
def collectors():
    """Manage data collectors"""
    pass


@collectors.command('list')
def list_collectors():
    """List all available collectors"""
    click.echo("Discovering collectors...")
    registry.auto_discover()

    collectors_list = registry.list_collectors()

    if not collectors_list:
        click.echo("No collectors found.")
        return

    click.echo("\nAvailable Data Collectors:")
    click.echo("=" * 80)

    for collector_info in collectors_list:
        status = "ENABLED" if collector_info['enabled'] else "DISABLED"
        auth = "Auth Required" if collector_info['requires_auth'] else "No Auth"

        click.echo(f"\n{collector_info['name']}")
        click.echo(f"  Category: {collector_info['category']}")
        click.echo(f"  Frequency: {collector_info['frequency']}")
        click.echo(f"  Status: {status}")
        click.echo(f"  {auth}")


@collectors.command('test')
@click.argument('collector_name')
@click.option('--symbol', '-s', multiple=True, help='Stock symbols to test')
def test_collector(collector_name: str, symbol: tuple):
    """Test a specific collector"""
    click.echo(f"Testing collector: {collector_name}")

    # Discover collectors
    registry.auto_discover()

    # Get the collector
    collector = registry.get_collector(collector_name)

    if not collector:
        click.echo(f"Collector '{collector_name}' not found", err=True)
        return

    # Validate credentials
    click.echo("Validating credentials...")
    if not collector.validate_credentials():
        click.echo("Credential validation failed!", err=True)
        return

    click.echo("Credentials valid!")

    # Collect data
    symbols = list(symbol) if symbol else None

    click.echo(f"Collecting data...")
    if symbols:
        click.echo(f"Filtering for symbols: {', '.join(symbols)}")

    try:
        # Run async collection
        data = asyncio.run(collector.collect(symbols=symbols, limit=10))

        click.echo(f"\nCollected {len(data)} data points!")

        # Show sample
        if data:
            click.echo("\nSample data point:")
            click.echo("-" * 80)
            sample = data[0]
            for key, value in sample.items():
                if key != 'metadata':
                    click.echo(f"{key}: {value}")

            if 'metadata' in sample:
                click.echo("\nMetadata:")
                for key, value in sample['metadata'].items():
                    click.echo(f"  {key}: {value}")

    except Exception as e:
        click.echo(f"Error during collection: {e}", err=True)
        raise


@cli.command()
@click.argument('collector_name')
@click.option('--symbol', '-s', multiple=True, help='Stock symbols to collect')
@click.option('--limit', '-l', default=100, help='Number of items to collect')
@click.option('--save/--no-save', default=True, help='Save to database')
def collect(collector_name: str, symbol: tuple, limit: int, save: bool):
    """Collect data from a specific collector"""
    click.echo(f"Running collector: {collector_name}")

    # Discover and get collector
    registry.auto_discover()
    collector = registry.get_collector(collector_name)

    if not collector:
        click.echo(f"Collector '{collector_name}' not found", err=True)
        return

    # Collect data
    symbols = list(symbol) if symbol else None

    try:
        data = asyncio.run(collector.collect(symbols=symbols, limit=limit))
        click.echo(f"Collected {len(data)} data points")

        if save and data:
            # Ensure database is connected
            db.connect()

            # Save to database
            click.echo("Saving to database...")
            saved_count = store.save_data_points(data)
            click.echo(f"Saved {saved_count} data points to database!")

            # Update collector status
            store.update_collector_status(collector_name, success=True)

        # Show summary
        if data:
            symbols_found = set(d['symbol'] for d in data if d.get('symbol'))
            if symbols_found:
                click.echo(f"\nSymbols found: {', '.join(sorted(symbols_found))}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if save:
            store.update_collector_status(collector_name, success=False, error=str(e))
        raise


@cli.command()
@click.option('--symbol', '-s', help='Filter by symbol')
@click.option('--source', help='Filter by source')
@click.option('--hours', '-h', default=24, help='Hours to look back')
@click.option('--limit', '-l', default=100, help='Max results')
def query(symbol: Optional[str], source: Optional[str], hours: int, limit: int):
    """Query collected data"""
    click.echo(f"Querying data (last {hours} hours)...")

    db.connect()

    data_points = store.get_recent_data_points(
        symbol=symbol,
        source=source,
        hours=hours,
        limit=limit
    )

    if not data_points:
        click.echo("No data found.")
        return

    click.echo(f"\nFound {len(data_points)} data points:")
    click.echo("=" * 80)

    for point in data_points[:10]:  # Show first 10
        click.echo(f"\n{point.timestamp} | {point.symbol} | {point.source}")
        click.echo(f"  Type: {point.data_type} | Value: {point.value}")

    if len(data_points) > 10:
        click.echo(f"\n... and {len(data_points) - 10} more")


@cli.command()
def status():
    """Show system status"""
    click.echo("PENGUIN System Status")
    click.echo("=" * 80)

    # Check configuration
    click.echo("\nConfiguration:")
    click.echo(f"  Reddit API: {'Configured' if config.REDDIT_CLIENT_ID else 'NOT CONFIGURED'}")
    click.echo(f"  Database: {config.DATABASE_URL.split('@')[-1] if '@' in config.DATABASE_URL else config.DATABASE_URL}")

    # Check collectors
    click.echo("\nCollectors:")
    registry.auto_discover()
    collectors_list = registry.list_collectors()
    enabled = [c for c in collectors_list if c['enabled']]
    click.echo(f"  Total: {len(collectors_list)}")
    click.echo(f"  Enabled: {len(enabled)}")

    # Try to connect to database
    try:
        db.connect()
        click.echo("\nDatabase: CONNECTED")
    except Exception as e:
        click.echo(f"\nDatabase: ERROR - {e}")


if __name__ == '__main__':
    cli()
