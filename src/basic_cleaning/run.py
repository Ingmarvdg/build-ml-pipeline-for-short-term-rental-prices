#!/usr/bin/env python
"""
This script download a URL to a local destination
"""
import pandas as pd
import logging

import wandb
import click

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()

@click.command()
@click.argument("input_artifact", type=str, required=True)
@click.argument("output_artifact", type=str, required=True)
@click.argument("output_type", type=str, required=True)
@click.argument("output_description", type=str, required=True)
@click.argument("min_price", type=int, required=True)
@click.argument("max_price", type=int, required=True)
def go(input_artifact, output_artifact, output_type, output_description, min_price, max_price):
    # initialize run
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(locals())

    # load dataframe
    local_path = wandb.use_artifact(input_artifact).file()
    df = pd.read_csv(local_path)

    # Drop outliers
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    # filter longitude and latitude
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    df.to_csv(output_artifact, index=False)

    artifact = wandb.Artifact(
        output_artifact,
        type=output_type,
        description=output_description,
    )
    artifact.add_file(output_artifact)
    run.log_artifact(artifact)
    run.finish()


if __name__ == "__main__":
    go()