from medgemma.medgemmaClient import MedGemmaClient


def nutritionalAgent(nutrition):
    """agent to watch daily nutritions data"""

    meals_db = {
        # --- Grains & Starches ---
        "oatmeal_cooked": {
            "sodium_g": 0.002, "sugar_g": 0.5, "carbs_g": 12.0, 
            "protein_g": 2.5, "fat_g": 1.4, "fiber_g": 1.7
        },
        "white_rice_cooked": {
            "sodium_g": 0.001, "sugar_g": 0.1, "carbs_g": 28.0, 
            "protein_g": 2.7, "fat_g": 0.3, "fiber_g": 0.4
        },
        "whole_wheat_toast": {
            "sodium_g": 0.45, "sugar_g": 4.3, "carbs_g": 41.0, 
            "protein_g": 13.0, "fat_g": 3.4, "fiber_g": 7.0
        },
        "pasta_cooked": {
            "sodium_g": 0.001, "sugar_g": 0.6, "carbs_g": 25.0, 
            "protein_g": 5.0, "fat_g": 1.1, "fiber_g": 1.8
        },

        # --- Proteins ---
        "egg_boiled": {
            "sodium_g": 0.12, "sugar_g": 1.1, "carbs_g": 1.1, 
            "protein_g": 13.0, "fat_g": 11.0, "fiber_g": 0.0
        },
        "chicken_breast_roasted": {
            "sodium_g": 0.07, "sugar_g": 0.0, "carbs_g": 0.0, 
            "protein_g": 31.0, "fat_g": 3.6, "fiber_g": 0.0
        },
        "salmon_fillet_baked": {
            "sodium_g": 0.06, "sugar_g": 0.0, "carbs_g": 0.0, 
            "protein_g": 25.0, "fat_g": 13.0, "fiber_g": 0.0
        },
        "chickpeas_canned": {
            "sodium_g": 0.24, "sugar_g": 4.8, "carbs_g": 27.0, 
            "protein_g": 8.9, "fat_g": 2.6, "fiber_g": 7.6
        },

        # --- Fruits & Vegetables ---
        "banana": {
            "sodium_g": 0.001, "sugar_g": 12.2, "carbs_g": 23.0, 
            "protein_g": 1.1, "fat_g": 0.3, "fiber_g": 2.6
        },
        "apple_with_skin": {
            "sodium_g": 0.001, "sugar_g": 10.4, "carbs_g": 14.0, 
            "protein_g": 0.3, "fat_g": 0.2, "fiber_g": 2.4
        },
        "broccoli_steamed": {
            "sodium_g": 0.03, "sugar_g": 1.4, "carbs_g": 7.0, 
            "protein_g": 2.8, "fat_g": 0.4, "fiber_g": 3.3
        },
        "spinach_raw": {
            "sodium_g": 0.08, "sugar_g": 0.4, "carbs_g": 3.6, 
            "protein_g": 2.9, "fat_g": 0.4, "fiber_g": 2.2
        },

        # --- Fats & Others ---
        "avocado": {
            "sodium_g": 0.007, "sugar_g": 0.7, "carbs_g": 8.5, 
            "protein_g": 2.0, "fat_g": 15.0, "fiber_g": 6.7
        },
        "greek_yogurt_plain": {
            "sodium_g": 0.04, "sugar_g": 3.2, "carbs_g": 3.6, 
            "protein_g": 10.0, "fat_g": 0.4, "fiber_g": 0.0
        },
        "almonds_dry_roasted": {
            "sodium_g": 0.001, "sugar_g": 4.4, "carbs_g": 22.0, 
            "protein_g": 21.0, "fat_g": 50.0, "fiber_g": 12.5
        }
    }
    
    system_prompt = f"""
        ROLE: You are a Professional Clinical Nutritionist AI.
        TASK: Analyze the user's daily food intake and provide a precise nutritional breakdown in JSON format.
        
        REFERENCE DATA (per 100g):
        {meals_db}

        STRICT GUIDELINES:
        1. CALCULATION LOGIC: 
        - If a portion size is mentioned (e.g., "200g"), scale the reference data accordingly.
        - If no portion is mentioned, assume a standard serving size (e.g., 150g for meals, 50g for snacks).
        - SALT CALCULATION: Total Salt (NaCl) = Sodium (g) * 2.5.
        
        2. UNKNOWN ITEMS: 
        - For items not in the reference DB, use high-fidelity clinical estimates based on standard nutritional databases (USDA/FDC).
        
        3. OUTPUT FORMAT: Return ONLY a valid JSON object. No conversational filler.
        
        JSON STRUCTURE:
        {{
            "analysis_meta": {{ "status": "complete", "unit": "grams" }},
            "diet": {{
                "morning": {{ "sodium": 0.0, "carbs": 0.0, "salt": 0.0, "sugar": 0.0 }},
                "lunch": {{ "sodium": 0.0, "carbs": 0.0, "salt": 0.0, "sugar": 0.0 }},
                "dinner": {{ "sodium": 0.0, "carbs": 0.0, "salt": 0.0, "sugar": 0.0 }}
            }},
            "nutritional_summary": "Short clinical observation of the day's intake."
        }}
        """

    user_prompt = f"Analyze the following nutritional intake data: {nutrition}"
    
    client = MedGemmaClient(system_prompt)
    response = client.respond(user_prompt)

    return response