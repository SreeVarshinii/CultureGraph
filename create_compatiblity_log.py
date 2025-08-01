import csv
import ast
from compatiblity import compute_compatibility

def batch_compatibility_check(der_entity_ids, output_csv_path, input_csv_path="logs/master_entity_log.csv"):
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

            try:
                entity_ids_b = ast.literal_eval(raw_ids)
                if not isinstance(entity_ids_b, list):
                    raise ValueError("full_entity_ids is not a list")
            except Exception as e:
                print(f"⛔ Skipping {filename} due to parsing error:", e)
                continue

            try:
                result = compute_compatibility(der_entity_ids, entity_ids_b)
                results.append({
                    "filename": filename,
                    "score": result["score"],
                    "summary": "; ".join(result["summary"])
                })
                print(f"✔ {filename} → Score: {result['score']}, Summary: {result['summary']}")
            except Exception as e:
                print(f"❌ Compatibility computation failed for {filename}:", e)

    # Write to output CSV
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=["filename", "score", "summary"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ All results saved to `{output_csv_path}`")
