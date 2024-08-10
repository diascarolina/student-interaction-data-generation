from datetime import datetime, timedelta
import pandas as pd
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import XSD

# Function to load the existing ontology
def load_ontology(file_path):
    g = Graph()
    try:
        g.parse(file_path, format='turtle')
        print("Ontology loaded successfully.")
    except Exception as e:
        print(f"Error loading ontology: {e}")
        raise
    return g

# Read the CSV file
csv_path = 'data/simulation_data_50u_200d copy.csv'
df = pd.read_csv(csv_path)

# Load the existing ontology
ontology_path = 'ontology/ontologia_avia.ttl'
g = load_ontology(ontology_path)

# Define the namespace
URI = "http://www.semanticweb.org/carolinadias/ontologies/2024/6/ontologia_avia#"
EX = Namespace(URI)
g.bind("ex", EX)

# Helper function to calculate end time and ensure the format is correct
def calculate_end_time(start_time_str, duration_str):
    start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    h, m, s = map(int, duration_str.split(':'))
    duration = timedelta(hours=h, minutes=m, seconds=s)
    end_time = start_time + duration
    return end_time.strftime("%Y-%m-%dT%H:%M:%S")

# Iterate over the DataFrame rows and add instances
for index, row in df.iterrows():
    # Define URIs
    student_uri = URIRef(f"{URI}{row['username'].replace(' ', '_')}")
    room_uri = URIRef(f"{URI}{row['room'].replace(' ', '_')}")
    action_uri = URIRef(f"{URI}action_{index}")
    
    if pd.notna(row['object']):
        object_uri = URIRef(f"{URI}{row['object'].replace(' ', '_')}")
    else:
        object_uri = None
    
    # Convert timestamp to xsd:dateTime format
    start_time = Literal(row['timestamp'].replace(' ', 'T'), datatype=XSD.dateTime)
    end_time = Literal(calculate_end_time(row['timestamp'], row['duration']), datatype=XSD.dateTime)
    
    # Add Action instance and properties
    if row['activity_type'] == 'movement':
        g.add((action_uri, RDF.type, EX.Movement))
        g.add((action_uri, EX.has_room, room_uri))
    elif row['activity_type'] == 'interaction' and object_uri:
        g.add((action_uri, RDF.type, EX.Interaction))
        g.add((action_uri, EX.has_object, object_uri))
    
    g.add((action_uri, EX.actionStartTime, start_time))
    g.add((action_uri, EX.actionEndTime, end_time))
    g.add((student_uri, EX.has_action, action_uri))
    
    # Add Student, Room, and Object instances if they don't already exist
    g.add((student_uri, RDF.type, EX.Student))
    g.add((student_uri, EX.id, Literal(row['username'], datatype=XSD.string)))
    # g.add((student_uri, EX.description, Literal(row['details'], datatype=XSD.string)))
    
    g.add((room_uri, RDF.type, EX.Room))
    g.add((room_uri, EX.id, Literal(row['room'], datatype=XSD.string)))
    
    if object_uri:
        g.add((object_uri, RDF.type, EX.interactableObject))
        g.add((object_uri, EX.id, Literal(row['object'], datatype=XSD.string)))

# Save the updated ontology with instances
output_path = 'ontology/ontologia_avia_with_instances_copy.ttl'
g.serialize(output_path, format='turtle')
print(f"Updated ontology with instances saved to {output_path}")
