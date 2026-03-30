import ab_utils as ab

if __name__ == "__main__":
    snakemake = ab.inject_snakemake("test")
    logger.info("Test INFO message")
    logger.debug("Test DEBUG message")
