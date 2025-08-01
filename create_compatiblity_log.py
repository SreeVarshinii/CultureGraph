import csv
import ast
import pandas as pd
from compatiblity import compute_compatibility,compute_nlp_similarity,get_gemini_score

def batch_compatibility_check(der_entity_ids, output_csv_path,scenario_answers, input_csv_path="logs/master_entity_log.csv"):
    """
    Compares a fixed list of entity_ids (`der_entity_ids`) to each row of entity_ids in a CSV,
    computes compatibility, and writes the results (filename, score, summary) to a new CSV.

    Parameters:
    - der_entity_ids: list of UUIDs for reference (entity_ids_a)
    - output_csv_path: where to save the results CSV
    - input_csv_path: source CSV with filename and full_entity_ids (default: logs/master_entity_log.csv)
    """
    results = []

    with open(input_csv_path, mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            filename = row.get("filename")
            raw_ids = row.get("full_entity_ids")
            row_scenario_answers=row.get("scenario_answers")

            try:
                entity_ids_b = ast.literal_eval(raw_ids)
                if not isinstance(entity_ids_b, list):
                    raise ValueError("full_entity_ids is not a list")
            except Exception as e:
                print(f"⛔ Skipping {filename} due to parsing error:", e)
                continue
            try:
                row_scenario_answers_b = ast.literal_eval(row_scenario_answers)
                if not isinstance(row_scenario_answers_b, list):
                    raise ValueError("full_entity_ids is not a list")
            except Exception as e:
                print(f"⛔ Skipping {filename} due to parsing error:", e)
                continue

            try:
                result = compute_compatibility(der_entity_ids, entity_ids_b)
                nlp_result=compute_nlp_similarity(scenario_answers,row_scenario_answers_b)
                gemini=get_gemini_score(scenario_answers,row_scenario_answers)
                print(nlp_result,gemini)
                results.append({
                    "filename": filename,
                    "score": result["score"],
                    "nlp_score":int(nlp_result),
                    "gemini_score":gemini["score"],
                    "Gemini_reasoning":gemini["reasoning"],
                    "summary": "; ".join(result["summary"]),
                    "mean": (result["score"]+gemini["score"]+int(nlp_result))/3
                })
                print(f"✔ {filename} → {results}")
            except Exception as e:
                print(f"❌ Compatibility computation failed for {filename}:", e)

    # Write to output CSV
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["filename", "score", "summary","nlp_score","gemini_score","Gemini_reasoning","summary","mean"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ All results saved to `{output_csv_path}`")


def row_with_highest_mean(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Find the row with the highest value in the 'mean' column
    max_row = df.loc[df['mean'].idxmax()]

    return max_row
