import networkx as nx
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Sample sentences about climate change
sentences = [
    "Climate change is causing more frequent extreme weather events.",
    "The polar ice caps are melting at an alarming rate.",
    "Rising sea levels threaten coastal communities worldwide.",
    "Deforestation contributes significantly to climate change.",
    "Renewable energy sources can help mitigate climate change.",
    "Global warming is a key driver of climate change."
]

# Step 2: Generate sentence embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
embeddings = model.encode(sentences)

# Step 3: Create a similarity graph
similarity_matrix = cosine_similarity(embeddings)
threshold = 0.1  # Define a similarity threshold for creating edges

G = nx.Graph()

# Add nodes with sentences as labels
for i, sentence in enumerate(sentences):
    G.add_node(i, sentence=sentence)

# Add edges based on similarity
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        if similarity_matrix[i][j] > threshold:
            G.add_edge(i, j, weight=similarity_matrix[i][j])

# Step 4: Visualize the graph
plt.figure(figsize=(10, 8))

# Use spring layout for better visualization
pos = nx.spring_layout(G, seed=42)

# Draw nodes with labels
nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=3000)
nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.6)
nx.draw_networkx_labels(G, pos, {i: f"Sentence {i+1}" for i in G.nodes}, font_size=10)

# Display edge labels (weights)
edge_labels = {(i, j): f"{similarity_matrix[i][j]:.2f}" for i, j in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

plt.title("Sentence Similarity Graph", fontsize=16)
plt.show()
