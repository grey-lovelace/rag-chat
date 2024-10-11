from src.vector_store import VectorStore

urls = [
    #  Source Allies Urls
    # "https://sourceallies.com",
    # "https://www.sourceallies.com/about-us/",
    # "https://www.sourceallies.com/partner-with-us/",
    # "https://www.sourceallies.com/what-we-do/",
    # "https://www.sourceallies.com/meet-our-team",
    # "https://www.sourceallies.com/careers/",
    # "https://www.sourceallies.com/blog/index.html",
    # "https://www.sourceallies.com/ml"

    #TravelEx Urls
    "https://www.travelexinsurance.com/travel-insurance/plans",
    "https://www.travelexinsurance.com/travel-insurance/plans/travel-select",
    "https://www.travelexinsurance.com/travel-insurance/plans/travel-basic",
    "https://www.travelexinsurance.com/travel-insurance/plans/travel-america",
    "https://www.travelexinsurance.com/travel-insurance/upgrades",
    "https://www.travelexinsurance.com/travel-insurance/upgrades/rental-car-insurance",
    "https://www.travelexinsurance.com/travel-insurance/upgrades/medical-coverage",
    "https://www.travelexinsurance.com/travel-insurance/upgrades/common-carrier-a-d-and-d",
    "https://www.travelexinsurance.com/travel-insurance/upgrades/adventure-sports",
    "https://www.travelexinsurance.com/travel-insurance/upgrades/cancel-for-any-reason",

    #PDF Path
    # "./data/benefits",
]

for url in urls:
    VectorStore.embed_data(url)