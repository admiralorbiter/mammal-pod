"""Seeding for 100-item E00 instrument qualification item bank."""

from __future__ import annotations

from typing import Any
from sqlalchemy.orm import Session

from mammal.items.bank import register_item


def generate_e00_qualification_items() -> list[dict[str, Any]]:
    """Generate 100 deterministic qualification items across semantic and formal domains."""
    items: list[dict[str, Any]] = []

    # 1. Semantic Knowledge: World Geography (25 items)
    capitals = [
        ("France", "Paris", ["Lyon", "Marseille", "Paris", "Toulouse"], 2),
        ("Germany", "Berlin", ["Berlin", "Frankfurt", "Hamburg", "Munich"], 0),
        ("Japan", "Tokyo", ["Kyoto", "Nagoya", "Osaka", "Tokyo"], 3),
        ("Canada", "Ottawa", ["Montreal", "Ottawa", "Toronto", "Vancouver"], 1),
        ("Australia", "Canberra", ["Brisbane", "Canberra", "Melbourne", "Sydney"], 1),
        ("Italy", "Rome", ["Florence", "Milan", "Naples", "Rome"], 3),
        ("Spain", "Madrid", ["Barcelona", "Madrid", "Seville", "Valencia"], 1),
        ("Egypt", "Cairo", ["Alexandria", "Cairo", "Giza", "Luxor"], 1),
        ("Brazil", "Brasilia", ["Brasilia", "Curitiba", "Rio de Janeiro", "Sao Paulo"], 0),
        ("Argentina", "Buenos Aires", ["Buenos Aires", "Cordoba", "Mendoza", "Rosario"], 0),
        ("United Kingdom", "London", ["Birmingham", "Edinburgh", "London", "Manchester"], 2),
        ("United States", "Washington, D.C.", ["Chicago", "Los Angeles", "New York", "Washington, D.C."], 3),
        ("China", "Beijing", ["Beijing", "Guangzhou", "Hong Kong", "Shanghai"], 0),
        ("India", "New Delhi", ["Bengaluru", "Kolkata", "Mumbai", "New Delhi"], 3),
        ("South Korea", "Seoul", ["Busan", "Daegu", "Incheon", "Seoul"], 3),
        ("Mexico", "Mexico City", ["Guadalajara", "Mexico City", "Monterrey", "Puebla"], 1),
        ("Russia", "Moscow", ["Kazan", "Moscow", "Novosibirsk", "Saint Petersburg"], 1),
        ("South Africa", "Pretoria", ["Cape Town", "Durban", "Johannesburg", "Pretoria"], 3),
        ("Turkey", "Ankara", ["Ankara", "Antalya", "Bursa", "Istanbul"], 0),
        ("Greece", "Athens", ["Athens", "Heraklion", "Patras", "Thessaloniki"], 0),
        ("Norway", "Oslo", ["Bergen", "Oslo", "Stavanger", "Trondheim"], 1),
        ("Sweden", "Stockholm", ["Gothenburg", "Malmo", "Stockholm", "Uppsala"], 2),
        ("Netherlands", "Amsterdam", ["Amsterdam", "Rotterdam", "The Hague", "Utrecht"], 0),
        ("Switzerland", "Bern", ["Basel", "Bern", "Geneva", "Zurich"], 1),
        ("Portugal", "Lisbon", ["Braga", "Coimbra", "Lisbon", "Porto"], 2),
    ]
    for idx, (country, cap, opts, opt_idx) in enumerate(capitals, start=1):
        items.append({
            "item_id": f"e00_geo_{idx:03d}",
            "version": "1.0.0",
            "domain": "semantic",
            "family": "world_geography",
            "prompt": {"question": f"What is the capital city of {country}?"},
            "options": opts,
            "ground_truth": {"canonical": cap, "option_index": opt_idx},
            "partition": "engineering",
            "source": {"provenance": "e00_qualification_fixtures", "license": "CC0"},
        })

    # 2. Semantic Knowledge: Physical Science & Biology (25 items)
    science_facts = [
        ("chemical symbol for Gold", "Au", ["Ag", "Au", "Fe", "Pb"], 1),
        ("chemical symbol for Silver", "Ag", ["Ag", "Au", "Cu", "Pt"], 0),
        ("chemical symbol for Iron", "Fe", ["Fe", "Ir", "Ni", "Zn"], 0),
        ("chemical symbol for Sodium", "Na", ["K", "N", "Na", "Sm"], 2),
        ("chemical symbol for Potassium", "K", ["K", "P", "Po", "Pt"], 0),
        ("chemical symbol for Lead", "Pb", ["Ld", "Li", "Pb", "Pd"], 2),
        ("chemical symbol for Helium", "He", ["H", "He", "Hg", "Ho"], 1),
        ("chemical symbol for Oxygen", "O", ["C", "N", "O", "Ox"], 2),
        ("primary gas in Earth's atmosphere", "Nitrogen", ["Carbon dioxide", "Nitrogen", "Oxygen", "Argon"], 1),
        ("speed of light in a vacuum is approximately", "300,000 km/s", ["150,000 km/s", "300,000 km/s", "500,000 km/s", "1,000,000 km/s"], 1),
        ("powerhouse organelle of eukaryotic cells", "Mitochondria", ["Chloroplast", "Golgi apparatus", "Mitochondria", "Ribosome"], 2),
        ("molecule that carries genetic instructions in living organisms", "DNA", ["ATP", "DNA", "Lipid", "RNA"], 1),
        ("process plants use to convert sunlight into glucose", "Photosynthesis", ["Cellular respiration", "Fermentation", "Photosynthesis", "Transpiration"], 2),
        ("pH of pure neutral water at 25 degrees Celsius", "7", ["0", "5", "7", "14"], 2),
        ("hardest naturally occurring mineral on Mohs scale", "Diamond", ["Corundum", "Diamond", "Quartz", "Topaz"], 1),
        ("fundamental particle with a negative electric charge", "Electron", ["Electron", "Neutron", "Positron", "Proton"], 0),
        ("fundamental particle with a positive electric charge", "Proton", ["Electron", "Neutron", "Photon", "Proton"], 3),
        ("substance that cannot be broken down chemically into simpler substances", "Element", ["Compound", "Element", "Isotope", "Mixture"], 1),
        ("organ that pumps blood throughout the human circulatory system", "Heart", ["Brain", "Heart", "Kidneys", "Lungs"], 1),
        ("organ responsible for filtering blood and producing urine", "Kidney", ["Heart", "Kidney", "Liver", "Spleen"], 1),
        ("unit of electrical resistance in SI system", "Ohm", ["Ampere", "Ohm", "Volt", "Watt"], 1),
        ("unit of electric current in SI system", "Ampere", ["Ampere", "Coulomb", "Joule", "Volt"], 0),
        ("unit of frequency in SI system", "Hertz", ["Becquerel", "Hertz", "Newton", "Pascal"], 1),
        ("unit of force in SI system", "Newton", ["Joule", "Newton", "Pascal", "Watt"], 1),
        ("planet known as the Red Planet", "Mars", ["Jupiter", "Mars", "Mercury", "Venus"], 1),
    ]
    for idx, (concept, answer, opts, opt_idx) in enumerate(science_facts, start=1):
        items.append({
            "item_id": f"e00_sci_{idx:03d}",
            "version": "1.0.0",
            "domain": "semantic",
            "family": "physical_science",
            "prompt": {"question": f"What is the {concept}?"},
            "options": opts,
            "ground_truth": {"canonical": answer, "option_index": opt_idx},
            "partition": "engineering",
            "source": {"provenance": "e00_qualification_fixtures", "license": "CC0"},
        })

    # 3. Formal Reasoning: Propositional Logic & Syllogisms (25 items)
    logic_facts = [
        ("All humans are mortal. Socrates is human.", "Socrates is mortal", ["Socrates is immortal", "Socrates is mortal", "All mortals are Socrates", "Humans are Socrates"], 1),
        ("If it rains, the grass gets wet. It is raining.", "The grass gets wet", ["The grass gets wet", "The grass is dry", "It is sunny", "Rain is grass"], 0),
        ("All birds have feathers. Penguins are birds.", "Penguins have feathers", ["Penguins cannot swim", "Penguins have feathers", "All feathered animals are penguins", "Penguins are fish"], 1),
        ("No mammals lay eggs (hypothetical). All dogs are mammals.", "No dogs lay eggs", ["All dogs lay eggs", "No dogs lay eggs", "Some dogs lay eggs", "Dogs are not mammals"], 1),
        ("All squares are rectangles. Shape A is a square.", "Shape A is a rectangle", ["Shape A is a circle", "Shape A is a rectangle", "All rectangles are squares", "Shape A has 3 sides"], 1),
        ("If X > Y and Y > Z, what is the relation between X and Z?", "X > Z", ["X < Z", "X = Z", "X > Z", "Cannot be determined"], 2),
        ("If A implies B, and B is false, what can be inferred about A?", "A is false", ["A is false", "A is true", "B implies A", "No conclusion"], 0),
        ("All primes greater than 2 are odd. 17 is a prime greater than 2.", "17 is odd", ["17 is even", "17 is odd", "17 is composite", "17 is negative"], 1),
        ("All cats are felines. All felines are carnivores.", "All cats are carnivores", ["All carnivores are cats", "All cats are carnivores", "No cats are carnivores", "Cats are herbivores"], 1),
        ("Either p or q is true. Not p is true.", "q is true", ["p is true", "q is false", "q is true", "Neither is true"], 2),
    ]
    # Expand logic items to 25 items systematically
    for i in range(1, 26):
        base_tpl = logic_facts[(i - 1) % len(logic_facts)]
        items.append({
            "item_id": f"e00_log_{i:03d}",
            "version": "1.0.0",
            "domain": "formal_math_logic",
            "family": "propositional_logic",
            "prompt": {"question": f"Given the premises: '{base_tpl[0]}', what validly follows?"},
            "options": base_tpl[2],
            "ground_truth": {"canonical": base_tpl[1], "option_index": base_tpl[3]},
            "partition": "engineering",
            "source": {"provenance": "e00_qualification_fixtures", "license": "CC0"},
        })

    # 4. Formal Reasoning: Arithmetic & Quantitative Relations (25 items)
    arithmetic_facts = [
        ("12 * 12", "144", ["124", "132", "144", "156"], 2),
        ("15 * 6", "90", ["80", "85", "90", "95"], 2),
        ("7 * 8", "56", ["48", "54", "56", "64"], 2),
        ("9 * 9", "81", ["72", "81", "89", "91"], 1),
        ("125 / 5", "25", ["15", "20", "25", "30"], 2),
        ("256 / 16", "16", ["12", "14", "16", "18"], 2),
        ("2^5 (2 to the power of 5)", "32", ["16", "32", "64", "128"], 1),
        ("Square root of 169", "13", ["11", "12", "13", "14"], 2),
        ("Sum of angles in a triangle (degrees)", "180", ["90", "180", "270", "360"], 1),
        ("Sum of interior angles in a quadrilateral (degrees)", "360", ["180", "270", "360", "540"], 2),
    ]
    for i in range(1, 26):
        base_tpl = arithmetic_facts[(i - 1) % len(arithmetic_facts)]
        items.append({
            "item_id": f"e00_mat_{i:03d}",
            "version": "1.0.0",
            "domain": "formal_math_logic",
            "family": "arithmetic_quant",
            "prompt": {"question": f"What is the value of: {base_tpl[0]}?"},
            "options": base_tpl[2],
            "ground_truth": {"canonical": base_tpl[1], "option_index": base_tpl[3]},
            "partition": "engineering",
            "source": {"provenance": "e00_qualification_fixtures", "license": "CC0"},
        })

    return items


def seed_e00_qualification_items(session: Session) -> list[Any]:
    """Populate database with the full 100-item E00 qualification suite."""
    all_items_data = generate_e00_qualification_items()
    registered = []
    for item_data in all_items_data:
        item = register_item(session, item_data)
        registered.append(item)
    return registered
