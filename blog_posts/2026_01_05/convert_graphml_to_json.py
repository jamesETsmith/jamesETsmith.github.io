import xml.etree.ElementTree as ET
import json
import random
import os

def parse_categories(md_file):
    categories = {}
    current_category = "Uncategorized"
    
    if not os.path.exists(md_file):
        return categories

    with open(md_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('###'):
                current_category = line.replace('###', '').strip()
            elif line.startswith('-'):
                item = line.lstrip('- ').strip()
                categories[item] = current_category
    return categories

def get_category_color(category):
    colors = {
        "Models & Architectures": "#E6194B", # Red
        "Companies & Labs": "#3CB44B",       # Green
        "Concepts & Techniques": "#4363D8",  # Blue
        "Hardware & Infrastructure": "#911EB4", # Purple
        "Business & Finance": "#FFE119",     # Yellow
        "Benchmarks & Evaluation": "#42D4F4", # Cyan
        "Safety & Ethics": "#F58231",        # Orange
        "Future Concepts": "#F032E6",        # Magenta
        "Other": "#A9A9A9",                  # Dark Grey
        "Uncategorized": "#D3D3D3"           # Light Grey
    }
    return colors.get(category, "#D3D3D3")

def convert_graphml_to_json(graphml_file, json_file, categories_file):
    tree = ET.parse(graphml_file)
    root = tree.getroot()

    # Parse categories
    node_categories = parse_categories(categories_file)

    # Define the namespace dictionary to find elements correctly
    ns = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

    nodes_data = []
    edges_data = []

    # Extract nodes
    for node in root.findall('.//graphml:node', ns):
        node_id = node.get('id')
        category = node_categories.get(node_id, "Uncategorized")
        color = get_category_color(category)
        
        nodes_data.append({
            'id': node_id,
            'label': node_id, 
            'x': random.random(),
            'y': random.random(),
            'size': 1, 
            'color': color,
            'category': category
        })

    # Extract edges
    for edge in root.findall('.//graphml:edge', ns):
        source = edge.get('source')
        target = edge.get('target')
        edge_id = edge.get('id') if edge.get('id') else f"{source}-{target}"

        tweet_link = None
        for data_elem in edge.findall('graphml:data', ns):
            if data_elem.get('key') == 'd0': 
                tweet_link = data_elem.text
                break
        
        # Determine edge color based on categories
        source_cat = node_categories.get(source, "Uncategorized")
        target_cat = node_categories.get(target, "Uncategorized")
        
        edge_color = '#e0e0e0' # Default light grey
        if source_cat == target_cat and source_cat != "Uncategorized":
             edge_color = get_category_color(source_cat)

        edges_data.append({
            'id': edge_id,
            'source': source,
            'target': target,
            'tweet_link': tweet_link,
            'size': 0.5, 
            'color': edge_color
        })

    graph_json = {
        'nodes': nodes_data,
        'edges': edges_data
    }

    with open(json_file, 'w') as f:
        json.dump(graph_json, f, indent=4)

if __name__ == '__main__':
    base_dir = '/home/james/projects/jamesETsmith.github.io/blog_posts/2026_01_05/'
    graphml_input_file = os.path.join(base_dir, 'tags_with_links.graphml')
    json_output_file = os.path.join(base_dir, 'graph_data.json')
    categories_file = os.path.join(base_dir, 'categories.md')
    
    convert_graphml_to_json(graphml_input_file, json_output_file, categories_file)
