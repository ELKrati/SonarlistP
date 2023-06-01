from elasticsearch import Elasticsearch

# Create Elasticsearch client
es = Elasticsearch(hosts=['http://localhost:9200'])

# Check if Elasticsearch is running
if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Failed to connect to Elasticsearch")

# Define index mapping
index_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "text"},
            "industry": {"type": "keyword"},
            "locality": {"type": "keyword"},
            "region": {"type": "keyword"},
            "country": {"type": "keyword"},
            "linkedin": {"type": "keyword"}
        }
    }
}

# Create index with mapping
es.indices.create(index="your_index_name", body=index_mapping)

import csv

def index_data_from_csv(filename, index_name):
    with open(filename, 'r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        bulk_data = []

        for row in reader:
            # Prepare data for indexing
            document = {
                "name": row['name'],
                "industry": row['industry'],
                "locality": row['locality'],
                "region": row['region'],
                "country": row['country'],
                "linkedin": row['linkedin_url']
            }

            # Create index operation
            index_op = {
                "_index": index_name,
                "_source": document
            }

            bulk_data.append(index_op)

            # Perform bulk indexing in batches of 1000 documents
            if len(bulk_data) >= 1000:
                es.bulk(index=index_name, body=bulk_data)
                bulk_data = []

        # Index any remaining documents
        if bulk_data:
            es.bulk(index=index_name, body=bulk_data)

def search_data(query, index_name):
    search_body = {
        "query": {
            "match": {
                "name": query
            }
        }
    }

    # Perform search
    response = es.search(index=index_name, body=search_body)

    # Extract and process search results
    hits = response['hits']['hits']
    for hit in hits:
        source = hit['_source']
        print("Name:", source['name'])
        print("Industry:", source['industry'])
        print("Locality:", source['locality'])
        print("Region:", source['region'])
        print("Country:", source['country'])
        print("LinkedIn:", source['linkedin'])
        print()
index_data_from_csv('/Users/buropa/Downloads/free_company_dataset_2.csv', 'companies')
search_data('facebook.com', 'companies')
