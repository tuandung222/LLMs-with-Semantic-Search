from typing import List, Dict

# Sample articles about various topics (10-20 words each)
SAMPLE_ARTICLES = [
    # Technology
    {
        "title": "Cloud Computing",
        "field": "Technology",
        "text": "Cloud computing enables businesses to store and process data remotely through internet-connected servers."
    },
    {
        "title": "5G Networks",
        "field": "Technology",
        "text": "5G networks provide faster mobile internet speeds and lower latency for better connected devices."
    },
    {
        "title": "Cybersecurity",
        "field": "Technology",
        "text": "Strong passwords and two-factor authentication help protect accounts from unauthorized access and cyber threats."
    },
    {
        "title": "Blockchain",
        "field": "Technology",
        "text": "Blockchain technology creates secure, decentralized records of transactions without needing intermediary verification."
    },
    # Science
    {
        "title": "Quantum Physics",
        "field": "Science",
        "text": "Quantum entanglement allows particles to instantly influence each other regardless of physical distance."
    },
    {
        "title": "Climate Change",
        "field": "Science",
        "text": "Rising global temperatures cause extreme weather events and affect ecosystems worldwide."
    },
    {
        "title": "DNA Structure",
        "field": "Science",
        "text": "DNA's double helix structure contains genetic instructions for development and functioning of organisms."
    },
    {
        "title": "Space Exploration",
        "field": "Science",
        "text": "Mars rovers collect soil samples and capture images to study the red planet's geology."
    },
    # Business
    {
        "title": "Digital Marketing",
        "field": "Business",
        "text": "Social media advertising helps businesses reach targeted audiences and increase brand awareness effectively."
    },
    {
        "title": "Remote Work",
        "field": "Business",
        "text": "Companies adopt hybrid work models combining office and remote work for better work-life balance."
    },
    {
        "title": "Cryptocurrency",
        "field": "Business",
        "text": "Bitcoin and other digital currencies offer decentralized alternatives to traditional banking systems."
    },
    {
        "title": "Startup Funding",
        "field": "Business",
        "text": "Venture capital firms invest in promising startups in exchange for equity ownership."
    },
    # Healthcare
    {
        "title": "Vaccination",
        "field": "Healthcare",
        "text": "Vaccines train the immune system to recognize and fight specific infectious diseases effectively."
    },
    {
        "title": "Mental Health",
        "field": "Healthcare",
        "text": "Regular exercise and meditation can help reduce stress and improve mental well-being."
    },
    {
        "title": "Telemedicine",
        "field": "Healthcare",
        "text": "Virtual doctor consultations provide convenient healthcare access through video calls and mobile apps."
    },
    {
        "title": "Nutrition",
        "field": "Healthcare",
        "text": "A balanced diet rich in fruits and vegetables supports overall health and immune function."
    },
    # Environment
    {
        "title": "Renewable Energy",
        "field": "Environment",
        "text": "Solar and wind power provide clean, sustainable alternatives to fossil fuel energy sources."
    },
    {
        "title": "Ocean Conservation",
        "field": "Environment",
        "text": "Reducing plastic waste helps protect marine life and preserve ocean ecosystem health."
    },
    {
        "title": "Sustainable Agriculture",
        "field": "Environment",
        "text": "Organic farming practices minimize chemical pesticides and promote soil health naturally."
    },
    {
        "title": "Air Quality",
        "field": "Environment",
        "text": "Electric vehicles and emission controls help reduce air pollution in urban areas."
    }
]

# More detailed example texts (50-100 words each)
EXAMPLE_TEXTS = [
    {
        "title": "Quantum Computing",
        "field": "Technology",
        "text": "Quantum computing leverages principles of quantum mechanics to perform calculations. Unlike classical computers using bits, quantum computers use qubits that can exist in multiple states simultaneously, enabling them to solve certain problems much faster."
    },
    {
        "title": "Climate Change",
        "field": "Environment",
        "text": "Climate change refers to long-term shifts in temperatures and weather patterns. Human activities have been the main driver since the 1800s, primarily due to burning fossil fuels like coal, oil, and gas, which produces heat-trapping gases."
    },
    {
        "title": "Artificial Intelligence",
        "field": "Technology",
        "text": "Artificial intelligence encompasses computer systems designed to mimic human intelligence. Machine learning, a subset of AI, enables systems to learn from data and improve without explicit programming, driving innovations across industries."
    },
    {
        "title": "Mediterranean Diet",
        "field": "Healthcare",
        "text": "The Mediterranean diet emphasizes plant-based foods, healthy fats, and moderate consumption of fish and poultry. Research shows it reduces risk of heart disease, stroke, and certain cancers while promoting longevity and cognitive health."
    },
    {
        "title": "Space Exploration",
        "field": "Science",
        "text": "Space exploration has evolved from early rocket launches to sophisticated missions including the International Space Station and Mars rovers. Private companies like SpaceX now complement government agencies, expanding possibilities for future missions."
    },
    {
        "title": "Renewable Energy",
        "field": "Environment",
        "text": "Renewable energy sources like solar, wind, and hydroelectric power provide sustainable alternatives to fossil fuels. Their decreasing costs and increasing efficiency make them crucial for addressing global energy needs while reducing carbon emissions."
    },
    {
        "title": "Blockchain Technology",
        "field": "Technology",
        "text": "Blockchain technology creates secure, decentralized digital ledgers for recording transactions. Beyond cryptocurrencies, applications include supply chain management, voting systems, and digital identity verification to enhance transparency and reduce fraud."
    },
    {
        "title": "Mindfulness Meditation",
        "field": "Healthcare",
        "text": "Mindfulness meditation involves focusing attention on the present moment without judgment. Regular practice can reduce stress, anxiety, and depression while improving concentration, emotional regulation, and overall well-being."
    },
    {
        "title": "Urban Agriculture",
        "field": "Environment",
        "text": "Urban agriculture transforms city spaces into productive growing areas. From rooftop gardens to vertical farms, these initiatives increase access to fresh food, reduce food miles, create community connections, and improve urban environmental quality."
    },
    {
        "title": "Biodiversity",
        "field": "Environment",
        "text": "Biodiversity refers to the variety of life forms within ecosystems. It provides essential services including clean air, water filtration, and crop pollination. Conservation efforts aim to protect this diversity threatened by habitat loss and climate change."
    },
    {
        "title": "History of Jazz",
        "field": "Arts",
        "text": "The history of jazz spans blues, ragtime, swing, bebop, and fusion. Originating in New Orleans among African American communities, this improvisational music form has influenced countless genres while reflecting American social and cultural developments."
    },
    {
        "title": "Virtual Reality",
        "field": "Technology",
        "text": "Virtual reality creates immersive digital experiences through specialized headsets and controllers. Applications extend beyond gaming to education, healthcare, architecture, and therapeutic interventions, transforming how we interact with digital content."
    },
    {
        "title": "Ocean Plastic Pollution",
        "field": "Environment",
        "text": "Ocean plastic pollution threatens marine ecosystems worldwide. Approximately 8 million metric tons enter oceans annually, harming wildlife and entering food chains. Solutions include reducing plastic use, improving waste management, and developing alternatives."
    },
    {
        "title": "Ancient Egyptian Civilization",
        "field": "History",
        "text": "Ancient Egyptian civilization flourished along the Nile River for over 3,000 years. Their remarkable achievements in architecture, art, mathematics, and medicine continue to fascinate scholars, while hieroglyphics provide insights into their complex society."
    },
    {
        "title": "Genetic Engineering",
        "field": "Science",
        "text": "Genetic engineering involves directly manipulating an organism's genes using biotechnology. Applications include creating disease-resistant crops, developing new medications, and treating genetic disorders, raising both promising possibilities and ethical questions."
    },
    {
        "title": "Japanese Gardens",
        "field": "Arts",
        "text": "Traditional Japanese gardens emphasize harmony with nature through careful design elements. Rocks, water, plants, and ornaments are arranged to create miniature idealized landscapes that encourage contemplation and represent philosophical concepts."
    },
    {
        "title": "Psychology of Decision-Making",
        "field": "Psychology",
        "text": "The psychology of decision-making examines how people make choices and judgments. Cognitive biases like anchoring, confirmation bias, and loss aversion often lead to irrational decisions, affecting everything from personal finance to business strategy."
    },
    {
        "title": "Modern Photography",
        "field": "Arts",
        "text": "Modern photography combines artistic vision with technical skill. Digital cameras and editing software have democratized the medium, while principles of composition, lighting, and timing remain essential for creating compelling visual narratives."
    },
    {
        "title": "Sustainable Fashion",
        "field": "Environment",
        "text": "Sustainable fashion addresses environmental and ethical concerns in the clothing industry. Approaches include using eco-friendly materials, ensuring fair labor practices, designing for longevity, and implementing circular production models to reduce waste."
    },
    {
        "title": "Deep Sea Ecosystems",
        "field": "Science",
        "text": "Deep sea ecosystems remain among Earth's least explored environments. Despite extreme pressure, cold, and darkness, these habitats support remarkable biodiversity, including bioluminescent organisms and extremophiles that have adapted to harsh conditions."
    }
]

# Recommended sample queries for users
SAMPLE_QUERIES = [
    "What are some recent technological advancements?",
    "How can businesses adapt to remote work?",
    "What are effective cybersecurity practices?",
    "Tell me about sustainable energy solutions.",
    "What are the benefits of telemedicine?",
    "How does climate change affect the environment?",
    "What are modern marketing strategies?",
    "Explain the importance of mental health.",
    "How do vaccines work?",
    "What are the advantages of blockchain technology?"
]

def get_sample_texts() -> List[str]:
    """
    Get a list of sample texts for populating the vector database.
    
    Returns:
        List of text strings
    """
    return [article["text"] for article in SAMPLE_ARTICLES]

def get_all_sample_data() -> List[Dict]:
    """
    Get all sample data including titles and fields.
    
    Returns:
        List of dictionaries containing text, title, and field
    """
    return SAMPLE_ARTICLES + EXAMPLE_TEXTS

def get_sample_queries() -> List[str]:
    """
    Get list of recommended sample queries.
    
    Returns:
        List of query strings
    """
    return SAMPLE_QUERIES