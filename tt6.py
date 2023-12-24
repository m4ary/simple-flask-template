from datetime import datetime, timedelta
def calculate_bmr_mifflin_st_jeor(gender, age, weight, height):
    """Calculate BMR using Mifflin St Jeor equation."""
    if gender.lower() == "male":
        return (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height) - (5 * age) - 161

def calculate_tdee(BMR, activity_level):
    """Calculate TDEE using the activity multiplier."""
    return BMR * activity_level

def calculate_macronutrients(caloric_intake_for_loss, weight_to_use_to_calc_protien, protein_intake_g_per_kg,fat_intake):
    """Calculate macronutrient intake (fat, protein, carb) in grams."""
    # Fat calculation
    fat_calories = fat_intake * caloric_intake_for_loss
    fat_g = fat_calories / 9  # Since there are 9 calories per gram of fat
    
    # Protein calculation
    protein_g = protein_intake_g_per_kg * weight_to_use_to_calc_protien
    protein_calories = protein_g * 4  # 4 calories per gram of protein
    
    # Carb calculation
    carb_calories = caloric_intake_for_loss - (fat_calories + protein_calories)
    carb_g = carb_calories / 4  # 4 calories per gram of carbohydrate
    
    return fat_g, protein_g, carb_g

def estimate_weight_loss_goals(weight, lean_body_mass, lean_mass_retention, rate_of_weight_loss, goal_bodyfat_percentage):
    """Estimate weight loss goals and timelines."""
    
    desired_lean_body_mass = lean_body_mass * (1-lean_mass_retention)
    goal_weight = desired_lean_body_mass / (1 - goal_bodyfat_percentage / 100)
    kg_lose_per_week = weight * rate_of_weight_loss
    total_kg_to_lose = weight - goal_weight
    estimated_weeks = total_kg_to_lose / kg_lose_per_week

 
    


    return desired_lean_body_mass, goal_weight, round(estimated_weeks,2)

def date_after_weeks(weeks):
    today = datetime.today()
    date_after = today + timedelta(weeks=weeks)
    return date_after.date()


def mifflin_st_jeor_calculate_nutrition_corrected_split(gender, age, weight, height, bodyfat_percentage, 
                                                  lean_mass_retention, rate_of_weight_loss, activity_level,
                                                  protein_intake_g_per_kg, caloric_deficit_percentage, goal_bodyfat,custom_caloric_deficit,fat_intake,protein_intake_method):
    
    BMR = calculate_bmr_mifflin_st_jeor(gender, age, weight, height)
    TDEE = calculate_tdee(BMR, activity_level)
    
    
    
    
    if(caloric_deficit_percentage != 0.404):
        caloric_deficit = TDEE * (1-caloric_deficit_percentage)
    else:
        caloric_deficit = TDEE - custom_caloric_deficit


    
    lean_body_mass = weight * (1 - bodyfat_percentage / 100)
    
    if(protein_intake_method == 1.0):
        weight_to_use_to_calc_protien = lean_body_mass
    else:
        weight_to_use_to_calc_protien=weight

    
    fat_g, protein_g, carb_g = calculate_macronutrients(caloric_deficit, weight_to_use_to_calc_protien, protein_intake_g_per_kg,fat_intake)
    
    desired_lean_body_mass, goal_weight, estimated_weeks = estimate_weight_loss_goals(weight, lean_body_mass, lean_mass_retention, rate_of_weight_loss, goal_bodyfat)
    date=date_after_weeks(estimated_weeks)
    return {
         "BMR": int(BMR),
    "TDEE":  int(TDEE),
    "CaloricIntake": int(caloric_deficit),
    "Macros": {
        "Fat": int(fat_g),
        "Protein":  int(protein_g),
        "Carbs": int(carb_g)
    },
    "Goals": {
        "LeanMass": round(desired_lean_body_mass,2),
        "GoalWeight": round(goal_weight,2),
        "Weeks":  estimated_weeks,
        "date":  date
    
        }
    }
