import requests
import time
from typing import List

# Example texts on diverse topics
EXAMPLE_TEXTS = [
    "Quantum computing leverages principles of quantum mechanics to perform calculations. Unlike classical computers using bits, quantum computers use qubits that can exist in multiple states simultaneously, enabling them to solve certain problems much faster.",
    "Climate change refers to long-term shifts in temperatures and weather patterns. Human activities have been the main driver since the 1800s, primarily due to burning fossil fuels like coal, oil, and gas, which produces heat-trapping gases.",
    "Artificial intelligence encompasses computer systems designed to mimic human intelligence. Machine learning, a subset of AI, enables systems to learn from data and improve without explicit programming, driving innovations across industries.",
    "The Mediterranean diet emphasizes plant-based foods, healthy fats, and moderate consumption of fish and poultry. Research shows it reduces risk of heart disease, stroke, and certain cancers while promoting longevity and cognitive health.",
    "Space exploration has evolved from early rocket launches to sophisticated missions including the International Space Station and Mars rovers. Private companies like SpaceX now complement government agencies, expanding possibilities for future missions.",
    "Renewable energy sources like solar, wind, and hydroelectric power provide sustainable alternatives to fossil fuels. Their decreasing costs and increasing efficiency make them crucial for addressing global energy needs while reducing carbon emissions.",
    "Blockchain technology creates secure, decentralized digital ledgers for recording transactions. Beyond cryptocurrencies, applications include supply chain management, voting systems, and digital identity verification to enhance transparency and reduce fraud.",
    "Mindfulness meditation involves focusing attention on the present moment without judgment. Regular practice can reduce stress, anxiety, and depression while improving concentration, emotional regulation, and overall well-being.",
    "Urban agriculture transforms city spaces into productive growing areas. From rooftop gardens to vertical farms, these initiatives increase access to fresh food, reduce food miles, create community connections, and improve urban environmental quality.",
    "Biodiversity refers to the variety of life forms within ecosystems. It provides essential services including clean air, water filtration, and crop pollination. Conservation efforts aim to protect this diversity threatened by habitat loss and climate change.",
    "The history of jazz spans blues, ragtime, swing, bebop, and fusion. Originating in New Orleans among African American communities, this improvisational music form has influenced countless genres while reflecting American social and cultural developments.",
    "Virtual reality creates immersive digital experiences through specialized headsets and controllers. Applications extend beyond gaming to education, healthcare, architecture, and therapeutic interventions, transforming how we interact with digital content.",
    "Ocean plastic pollution threatens marine ecosystems worldwide. Approximately 8 million metric tons enter oceans annually, harming wildlife and entering food chains. Solutions include reducing plastic use, improving waste management, and developing alternatives.",
    "Ancient Egyptian civilization flourished along the Nile River for over 3,000 years. Their remarkable achievements in architecture, art, mathematics, and medicine continue to fascinate scholars, while hieroglyphics provide insights into their complex society.",
    "Genetic engineering involves directly manipulating an organism's genes using biotechnology. Applications include creating disease-resistant crops, developing new medications, and treating genetic disorders, raising both promising possibilities and ethical questions.",
    "Traditional Japanese gardens emphasize harmony with nature through careful design elements. Rocks, water, plants, and ornaments are arranged to create miniature idealized landscapes that encourage contemplation and represent philosophical concepts.",
    "The psychology of decision-making examines how people make choices and judgments. Cognitive biases like anchoring, confirmation bias, and loss aversion often lead to irrational decisions, affecting everything from personal finance to business strategy.",
    "Modern photography combines artistic vision with technical skill. Digital cameras and editing software have democratized the medium, while principles of composition, lighting, and timing remain essential for creating compelling visual narratives.",
    "Sustainable fashion addresses environmental and ethical concerns in the clothing industry. Approaches include using eco-friendly materials, ensuring fair labor practices, designing for longevity, and implementing circular production models to reduce waste.",
    "Deep sea ecosystems remain among Earth's least explored environments. Despite extreme pressure, cold, and darkness, these habitats support remarkable biodiversity, including bioluminescent organisms and extremophiles that have adapted to harsh conditions."
]

def load_example_texts(api_url: str = "http://localhost:8000") -> None:
    """
    Load example texts into the database via the API
    
    Args:
        api_url: Base URL for the API
    """
    process_text_endpoint = f"{api_url}/process-text"
    
    print(f"Loading {len(EXAMPLE_TEXTS)} example texts into the database...")
    
    for i, text in enumerate(EXAMPLE_TEXTS, 1):
        try:
            response = requests.post(
                process_text_endpoint,
                json={"text": text}
            )
            if response.status_code == 200:
                print(f"[{i}/{len(EXAMPLE_TEXTS)}] Added: {text[:40]}...")
            else:
                print(f"[{i}/{len(EXAMPLE_TEXTS)}] Failed to add text. Status code: {response.status_code}")
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"[{i}/{len(EXAMPLE_TEXTS)}] Error: {str(e)}")
        
        # Sleep briefly to avoid overwhelming the API
        time.sleep(0.5)
    
    print("Finished loading example texts")

if __name__ == "__main__":
    # When running in the Docker container, the search server is on the same host
    load_example_texts(api_url="http://localhost:8000") 